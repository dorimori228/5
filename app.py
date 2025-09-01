#!/usr/bin/env python3
"""
Gumtree Auto Lister Web UI

A Flask web application for managing Gumtree listings with automated posting capabilities.
"""

import os
import json
import shutil
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import logging
from gumtree_bot import GumtreeBot

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
BACKUP_FOLDER = 'backup_listings'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# Load location data
def load_locations():
    """Load location data from files"""
    locations = {}
    
    # Load England locations
    try:
        with open('gumtree england locations.txt', 'r', encoding='utf-8') as f:
            england_data = f.read()
            locations['England'] = parse_locations(england_data)
    except FileNotFoundError:
        logger.warning("England locations file not found")
        locations['England'] = {}
    
    # Load Wales locations
    try:
        with open('gumtree wales locations.txt', 'r', encoding='utf-8') as f:
            wales_data = f.read()
            locations['Wales'] = parse_locations(wales_data)
    except FileNotFoundError:
        logger.warning("Wales locations file not found")
        locations['Wales'] = {}
    
    return locations

def parse_locations(data):
    """Parse location data from text file"""
    locations = {}
    current_county = None
    
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a county (no comma)
        if ',' not in line and line not in ['ENGLAND', 'WALES']:
            current_county = line
            locations[current_county] = []
        elif ',' in line and current_county:
            # It's a location within a county
            locations[current_county].append(line)
    
    return locations

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_listing_backup(listing_data, photos):
    """Save listing data and photos to backup folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    listing_id = f"listing_{timestamp}"
    backup_path = os.path.join(BACKUP_FOLDER, listing_id)
    
    os.makedirs(backup_path, exist_ok=True)
    
    # Save listing data
    with open(os.path.join(backup_path, 'listing_data.txt'), 'w', encoding='utf-8') as f:
        f.write(f"Title: {listing_data['title']}\n")
        f.write(f"Description: {listing_data['description']}\n")
        f.write(f"Price: {listing_data['price']}\n")
        f.write(f"Condition: {listing_data['condition']}\n")
        f.write(f"Location: {listing_data['location']}\n")
        f.write(f"Sub-location: {listing_data.get('sub_location', 'N/A')}\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Save photos
    if photos:
        for i, photo in enumerate(photos):
            if photo and allowed_file(photo.filename):
                filename = secure_filename(f"photo_{i+1}_{photo.filename}")
                photo.save(os.path.join(backup_path, filename))
    
    return listing_id

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/create_listing')
def create_listing():
    """Create new listing page"""
    locations = load_locations()
    return render_template('create_listing.html', locations=locations)

@app.route('/api/locations/<country>')
def get_locations(country):
    """Get locations for a specific country"""
    locations = load_locations()
    return jsonify(locations.get(country, {}))

@app.route('/api/sub_locations/<country>/<county>')
def get_sub_locations(country, county):
    """Get sub-locations for a specific county"""
    locations = load_locations()
    country_locations = locations.get(country, {})
    sub_locations = country_locations.get(county, [])
    
    # If there are sub-locations, return them; otherwise return empty list
    return jsonify(sub_locations)

@app.route('/submit_listing', methods=['POST'])
def submit_listing():
    """Submit a new listing"""
    try:
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '').strip()
        condition = request.form.get('condition', 'New')
        category = request.form.get('category', '').strip()
        country = request.form.get('country', '')
        county = request.form.get('county', '')
        sub_location = request.form.get('sub_location', '')
        
        # Get uploaded photos
        photos = request.files.getlist('photos')
        
        # Validate required fields
        if not all([title, description, price, category, country, county]):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('create_listing'))
        
        # Validate price
        try:
            float(price.replace('£', '').replace(',', ''))
        except ValueError:
            flash('Please enter a valid price', 'error')
            return redirect(url_for('create_listing'))
        
        # Prepare listing data
        listing_data = {
            'title': title,
            'description': description,
            'price': price,
            'condition': condition,
            'category': category,
            'location': f"{county}, {country}",
            'sub_location': sub_location,
            'country': country,
            'county': county
        }
        
        # Save backup
        listing_id = save_listing_backup(listing_data, photos)
        
        # Save to queue for processing
        queue_file = os.path.join(BACKUP_FOLDER, 'listing_queue.json')
        queue_data = []
        
        if os.path.exists(queue_file):
            with open(queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)
        
        queue_data.append({
            'id': listing_id,
            'data': listing_data,
            'status': 'pending',
            'created': datetime.now().isoformat()
        })
        
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue_data, f, indent=2, ensure_ascii=False)
        
        flash(f'Listing created successfully! ID: {listing_id}', 'success')
        return redirect(url_for('manage_listings'))
        
    except Exception as e:
        logger.error(f"Error creating listing: {e}")
        flash('Error creating listing. Please try again.', 'error')
        return redirect(url_for('create_listing'))

@app.route('/manage_listings')
def manage_listings():
    """Manage existing listings"""
    queue_file = os.path.join(BACKUP_FOLDER, 'listing_queue.json')
    listings = []
    
    if os.path.exists(queue_file):
        with open(queue_file, 'r', encoding='utf-8') as f:
            listings = json.load(f)
    
    return render_template('manage_listings.html', listings=listings)

@app.route('/api/process_listing/<listing_id>', methods=['POST'])
def process_listing(listing_id):
    """Process a single listing with the bot"""
    try:
        # Load listing data
        queue_file = os.path.join(BACKUP_FOLDER, 'listing_queue.json')
        if not os.path.exists(queue_file):
            return jsonify({'success': False, 'error': 'No listings found'})
        
        with open(queue_file, 'r', encoding='utf-8') as f:
            listings = json.load(f)
        
        # Find the listing
        listing = None
        for item in listings:
            if item['id'] == listing_id:
                listing = item
                break
        
        if not listing:
            return jsonify({'success': False, 'error': 'Listing not found'})
        
        # Update status to processing
        listing['status'] = 'processing'
        listing['started'] = datetime.now().isoformat()
        
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(listings, f, indent=2, ensure_ascii=False)
        
        # Initialize bot and process listing
        bot = GumtreeBot(headless=False, use_existing_browser=False)
        bot.setup_driver()
        
        # Prepare listing data for bot
        bot_listing_data = {
            'title': listing['data']['title'],
            'description': listing['data']['description'],
            'price': listing['data']['price'],
            'condition': listing['data']['condition'],
            'category': listing['data'].get('category', ''),
            'location': listing['data']['location'],
            'sub_location': listing['data'].get('sub_location', ''),
            'listing_id': listing['id']  # Add listing ID for photo access
        }
        
        logger.info(f"Prepared bot listing data: {bot_listing_data}")
        
        # Process the listing
        success = bot.list_item(bot_listing_data)
        
        # Update status
        listing['status'] = 'completed' if success else 'failed'
        listing['completed'] = datetime.now().isoformat()
        listing['success'] = success
        
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(listings, f, indent=2, ensure_ascii=False)
        
        # Close bot
        if bot.driver:
            bot.driver.quit()
        
        return jsonify({'success': success, 'message': 'Listing processed successfully' if success else 'Listing failed'})
        
    except Exception as e:
        logger.error(f"Error processing listing {listing_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/process_all', methods=['POST'])
def process_all_listings():
    """Process all pending listings"""
    try:
        queue_file = os.path.join(BACKUP_FOLDER, 'listing_queue.json')
        if not os.path.exists(queue_file):
            return jsonify({'success': False, 'error': 'No listings found'})
        
        with open(queue_file, 'r', encoding='utf-8') as f:
            listings = json.load(f)
        
        pending_listings = [l for l in listings if l['status'] == 'pending']
        
        if not pending_listings:
            return jsonify({'success': True, 'message': 'No pending listings to process'})
        
        # Initialize bot once for all listings
        bot = GumtreeBot(headless=False, use_existing_browser=False)
        bot.setup_driver()
        
        processed = 0
        failed = 0
        
        for listing in pending_listings:
            try:
                # Update status to processing
                listing['status'] = 'processing'
                listing['started'] = datetime.now().isoformat()
                
                # Prepare listing data for bot
                bot_listing_data = {
                    'title': listing['data']['title'],
                    'description': listing['data']['description'],
                    'price': listing['data']['price'],
                    'condition': listing['data']['condition'],
                    'category': listing['data'].get('category', ''),
                    'location': listing['data']['location'],
                    'sub_location': listing['data'].get('sub_location', ''),
                    'listing_id': listing['id']  # Add listing ID for photo access
                }
                
                logger.info(f"Processing listing {listing['id']} with data: {bot_listing_data}")
                
                # Process the listing
                success = bot.list_item(bot_listing_data)
                
                # Update status
                listing['status'] = 'completed' if success else 'failed'
                listing['completed'] = datetime.now().isoformat()
                listing['success'] = success
                
                if success:
                    processed += 1
                else:
                    failed += 1
                
                # Add delay between listings
                import time
                time.sleep(random.uniform(30, 60))  # 30-60 second delay
                
            except Exception as e:
                logger.error(f"Error processing listing {listing['id']}: {e}")
                listing['status'] = 'failed'
                listing['error'] = str(e)
                failed += 1
        
        # Save updated queue
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(listings, f, indent=2, ensure_ascii=False)
        
        # Close bot
        if bot.driver:
            bot.driver.quit()
        
        return jsonify({
            'success': True, 
            'message': f'Processed {processed} listings successfully, {failed} failed'
        })
        
    except Exception as e:
        logger.error(f"Error processing all listings: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
