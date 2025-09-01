#!/usr/bin/env python3
"""
Test script for the Gumtree Auto Lister Web UI
"""

import os
import json
import time
from app import load_locations, parse_locations

def test_location_loading():
    """Test location data loading"""
    print("🧪 Testing location data loading...")
    
    try:
        locations = load_locations()
        
        if not locations:
            print("❌ No locations loaded")
            return False
        
        print(f"✅ Loaded {len(locations)} countries")
        
        for country, counties in locations.items():
            print(f"   {country}: {len(counties)} counties")
            if counties:
                first_county = list(counties.keys())[0]
                sub_locations = counties[first_county]
                print(f"      Example: {first_county} has {len(sub_locations)} sub-locations")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading locations: {e}")
        return False

def test_directory_structure():
    """Test required directories exist"""
    print("\n🧪 Testing directory structure...")
    
    required_dirs = [
        'templates',
        'static/uploads',
        'backup_listings'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} exists")
        else:
            print(f"❌ {dir_path} missing")
            all_exist = False
    
    return all_exist

def test_template_files():
    """Test template files exist"""
    print("\n🧪 Testing template files...")
    
    required_templates = [
        'templates/base.html',
        'templates/index.html',
        'templates/create_listing.html',
        'templates/manage_listings.html'
    ]
    
    all_exist = True
    for template in required_templates:
        if os.path.exists(template):
            print(f"✅ {template} exists")
        else:
            print(f"❌ {template} missing")
            all_exist = False
    
    return all_exist

def test_bot_import():
    """Test bot import"""
    print("\n🧪 Testing bot import...")
    
    try:
        from gumtree_bot import GumtreeBot
        print("✅ GumtreeBot imported successfully")
        
        # Test bot initialization
        bot = GumtreeBot(headless=True, use_existing_browser=False)
        print("✅ GumtreeBot initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing GumtreeBot: {e}")
        return False

def test_flask_import():
    """Test Flask import"""
    print("\n🧪 Testing Flask import...")
    
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error importing Flask: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Gumtree Auto Lister Web UI Test Suite")
    print("=" * 50)
    
    tests = [
        test_directory_structure,
        test_template_files,
        test_flask_import,
        test_bot_import,
        test_location_loading
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The web UI should work correctly.")
        print("\n📋 Next steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Create your first listing")
        print("4. Test the bot functionality")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    exit(0 if success else 1)
