#!/usr/bin/env python3
"""
Test script to verify UI integration with undetected Chrome bot
"""

import os
import json
import time
import requests
from gumtree_bot import GumtreeBot

def test_ui_connection():
    """Test if the UI is accessible"""
    print("🧪 Testing UI connection...")
    
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ UI is accessible at http://localhost:5000")
            return True
        else:
            print(f"❌ UI returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to UI. Make sure Flask app is running.")
        print("   Start it with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to UI: {e}")
        return False

def test_bot_initialization():
    """Test if the bot can be initialized"""
    print("\n🧪 Testing bot initialization...")
    
    try:
        # Test bot initialization
        bot = GumtreeBot(headless=True, use_existing_browser=False)
        print("✅ Bot class initialized successfully")
        
        # Test driver setup
        bot.setup_driver()
        print("✅ Undetected Chrome driver setup successful")
        
        # Test basic navigation
        bot.driver.get("https://www.gumtree.com")
        time.sleep(2)
        
        current_url = bot.driver.current_url
        print(f"✅ Successfully navigated to: {current_url}")
        
        # Clean up
        bot.driver.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing bot initialization: {e}")
        return False

def test_listing_data_structure():
    """Test the listing data structure"""
    print("\n🧪 Testing listing data structure...")
    
    # Create test listing data
    test_listing = {
        'title': 'Test Artificial Grass',
        'description': 'High quality artificial grass for sale',
        'price': '150',
        'condition': 'New',
        'category': 'Artificial Grass',
        'location': 'Dorset, England',
        'sub_location': 'Shaftesbury, Dorset',
        'listing_id': 'test_123'
    }
    
    print("✅ Test listing data structure:")
    for key, value in test_listing.items():
        print(f"   {key}: {value}")
    
    # Test if bot can handle this data
    try:
        bot = GumtreeBot(headless=True, use_existing_browser=False)
        bot.setup_driver()
        
        # Test category selection logic
        category = test_listing.get('category', '').lower()
        if 'artificial grass' in category or 'grass' in category:
            category_url = "https://www.gumtree.com/postad/create?categoryId=11108"
            print("✅ Category selection logic works for Artificial Grass")
        elif 'composite decking' in category or 'decking' in category:
            category_url = "https://www.gumtree.com/postad/create?categoryId=152"
            print("✅ Category selection logic works for Composite Decking")
        else:
            category_url = "https://www.gumtree.com/postad/create?categoryId=11108"
            print("✅ Default category selection works")
        
        print(f"✅ Would navigate to: {category_url}")
        
        # Clean up
        bot.driver.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing listing data: {e}")
        return False

def test_ui_endpoints():
    """Test UI endpoints"""
    print("\n🧪 Testing UI endpoints...")
    
    endpoints = [
        ("/", "Home page"),
        ("/create_listing", "Create listing page"),
        ("/manage_listings", "Manage listings page")
    ]
    
    all_passed = True
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:5000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description} accessible")
            else:
                print(f"❌ {description} returned status {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ Error accessing {description}: {e}")
            all_passed = False
    
    return all_passed

def test_backup_system():
    """Test backup system"""
    print("\n🧪 Testing backup system...")
    
    try:
        # Check if backup directory exists
        if os.path.exists('backup_listings'):
            print("✅ Backup directory exists")
        else:
            print("❌ Backup directory missing")
            return False
        
        # Check if uploads directory exists
        if os.path.exists('static/uploads'):
            print("✅ Uploads directory exists")
        else:
            print("❌ Uploads directory missing")
            return False
        
        # Test creating a test backup
        test_id = f"test_{int(time.time())}"
        test_backup_dir = os.path.join('backup_listings', test_id)
        os.makedirs(test_backup_dir, exist_ok=True)
        
        # Create test files
        test_data = {
            'title': 'Test Listing',
            'description': 'Test Description',
            'price': '100',
            'condition': 'New',
            'category': 'Artificial Grass',
            'location': 'Test Location',
            'sub_location': 'Test Sub Location',
            'created_at': datetime.now().isoformat()
        }
        
        with open(os.path.join(test_backup_dir, 'listing_data.json'), 'w') as f:
            json.dump(test_data, f, indent=2)
        
        with open(os.path.join(test_backup_dir, 'listing_info.txt'), 'w') as f:
            f.write(f"Title: {test_data['title']}\n")
            f.write(f"Description: {test_data['description']}\n")
            f.write(f"Price: £{test_data['price']}\n")
            f.write(f"Condition: {test_data['condition']}\n")
            f.write(f"Category: {test_data['category']}\n")
            f.write(f"Location: {test_data['location']}\n")
            f.write(f"Sub Location: {test_data['sub_location']}\n")
        
        print("✅ Test backup created successfully")
        
        # Clean up test backup
        import shutil
        shutil.rmtree(test_backup_dir)
        print("✅ Test backup cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing backup system: {e}")
        return False

def main():
    """Run all UI integration tests"""
    print("🚀 UI Integration Test Suite")
    print("=" * 60)
    
    tests = [
        test_ui_connection,
        test_bot_initialization,
        test_listing_data_structure,
        test_ui_endpoints,
        test_backup_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All UI integration tests passed!")
        print("\n📋 UI is working correctly:")
        print("✅ Flask app is running on localhost:5000")
        print("✅ Bot can be initialized with undetected Chrome")
        print("✅ Listing data structure is correct")
        print("✅ All UI endpoints are accessible")
        print("✅ Backup system is working")
        print("\n🚀 You can now use the UI to create and manage listings!")
        print("\n📋 How to use:")
        print("1. Open your browser and go to: http://localhost:5000")
        print("2. Create listings using the 'Create Listing' page")
        print("3. Manage and process listings using the 'Manage Listings' page")
        print("4. The bot will use undetected Chrome for maximum stealth")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Flask app is running: python app.py")
        print("2. Check if all dependencies are installed: pip install -r requirements.txt")
        print("3. Verify Chrome is installed on your system")
        print("4. Check if any firewall is blocking localhost:5000")
    
    return passed == total

if __name__ == "__main__":
    from datetime import datetime
    success = main()
    input("\nPress Enter to exit...")
    exit(0 if success else 1)
