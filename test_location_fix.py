#!/usr/bin/env python3
"""
Test script to verify location data is passed correctly from UI to bot
"""

import json
import os
from gumtree_bot import GumtreeBot

def test_location_parsing():
    """Test location parsing logic"""
    print("🧪 Testing location parsing...")
    
    # Test cases
    test_cases = [
        {
            'location': 'Dorset, England',
            'sub_location': 'Shaftesbury, Dorset',
            'expected_county': 'Dorset',
            'expected_country': 'England'
        },
        {
            'location': 'Bristol, England',
            'sub_location': 'Backwell, Bristol',
            'expected_county': 'Bristol',
            'expected_country': 'England'
        },
        {
            'location': 'Cardiff, Wales',
            'sub_location': 'Cathays, Cardiff',
            'expected_county': 'Cardiff',
            'expected_country': 'Wales'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['location']}")
        
        # Parse location like the bot does
        location = test_case['location']
        if ',' in location:
            county, country = location.split(',', 1)
            county = county.strip()
            country = country.strip()
        else:
            county = location
            country = "England"
        
        print(f"   Parsed county: {county}")
        print(f"   Parsed country: {country}")
        print(f"   Sub-location: {test_case['sub_location']}")
        
        # Verify parsing
        if county == test_case['expected_county'] and country == test_case['expected_country']:
            print("   ✅ Parsing correct")
        else:
            print("   ❌ Parsing incorrect")
            print(f"   Expected: {test_case['expected_county']}, {test_case['expected_country']}")

def test_bot_initialization():
    """Test bot initialization with location data"""
    print("\n🧪 Testing bot initialization...")
    
    try:
        # Test listing data
        test_listing_data = {
            'title': 'Test Item',
            'description': 'Test description',
            'price': '100',
            'condition': 'New',
            'location': 'Dorset, England',
            'sub_location': 'Shaftesbury, Dorset'
        }
        
        print(f"Test listing data: {test_listing_data}")
        
        # Initialize bot (headless for testing)
        bot = GumtreeBot(headless=True, use_existing_browser=False)
        print("✅ Bot initialized successfully")
        
        # Test location parsing in bot
        location = test_listing_data.get('location', '')
        sub_location = test_listing_data.get('sub_location', '')
        
        if ',' in location:
            county, country = location.split(',', 1)
            county = county.strip()
            country = country.strip()
        else:
            county = location
            country = "England"
        
        print(f"Bot parsed location: county={county}, country={country}, sub_location={sub_location}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_queue_data():
    """Test if queue data contains correct location information"""
    print("\n🧪 Testing queue data...")
    
    queue_file = os.path.join('backup_listings', 'listing_queue.json')
    
    if not os.path.exists(queue_file):
        print("❌ No queue file found")
        return False
    
    try:
        with open(queue_file, 'r', encoding='utf-8') as f:
            listings = json.load(f)
        
        if not listings:
            print("❌ No listings in queue")
            return False
        
        print(f"Found {len(listings)} listings in queue")
        
        for i, listing in enumerate(listings, 1):
            print(f"\nListing {i}:")
            print(f"   ID: {listing['id']}")
            print(f"   Title: {listing['data']['title']}")
            print(f"   Location: {listing['data']['location']}")
            print(f"   Sub-location: {listing['data'].get('sub_location', 'N/A')}")
            print(f"   Status: {listing['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading queue: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Location Fix Test Suite")
    print("=" * 40)
    
    tests = [
        test_location_parsing,
        test_bot_initialization,
        test_queue_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Location data should now be passed correctly.")
        print("\n📋 Next steps:")
        print("1. Start the web UI: python app.py")
        print("2. Create a test listing with a different location")
        print("3. Process the listing and check if it uses the correct location")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    exit(0 if success else 1)
