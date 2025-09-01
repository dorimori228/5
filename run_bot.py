#!/usr/bin/env python3
"""
Gumtree Auto Lister - Example Usage

This script demonstrates how to use the Gumtree bot to automatically list items.
"""

import json
import logging
from gumtree_bot import GumtreeBot

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_listing_config(config_file: str = "listing_config.json") -> dict:
    """Load listing configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file {config_file} not found")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in configuration file {config_file}")
        return {}


def main():
    """Main function to run the Gumtree bot"""
    
    # Load configuration
    listing_data = load_listing_config()
    if not listing_data:
        logger.error("Failed to load listing configuration")
        return
    
    # Validate required fields
    required_fields = ['title', 'description', 'price']
    missing_fields = [field for field in required_fields if not listing_data.get(field)]
    if missing_fields:
        logger.error(f"Missing required fields in configuration: {missing_fields}")
        return
    
    print("Gumtree Auto Lister Bot")
    print("=======================")
    print(f"Title: {listing_data.get('title')}")
    print(f"Description: {listing_data.get('description')[:50]}...")
    print(f"Price: £{listing_data.get('price')}")
    print(f"Category Search: {listing_data.get('category_search')}")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed with this listing? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Listing cancelled.")
        return
    
    # Run the bot
    try:
        print("Starting Gumtree bot...")
        print("Note: On first run, you'll need to manually log in to Gumtree.")
        print("The bot will save your login cookies for future automatic logins.")
        print()
        
        # Initialize bot (try to use existing browser first)
        bot = GumtreeBot(headless=False, use_existing_browser=True)
        
        # Run the listing process
        success = bot.run(listing_data)
        
        if success:
            print("✅ Item listed successfully!")
        else:
            print("❌ Failed to list item. Check the logs for details.")
            
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()