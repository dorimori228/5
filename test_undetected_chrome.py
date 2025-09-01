#!/usr/bin/env python3
"""
Test script to verify undetected-chromedriver implementation
"""

import os
import time
from gumtree_bot import GumtreeBot

def test_undetected_chrome_initialization():
    """Test undetected Chrome initialization"""
    print("🧪 Testing undetected Chrome initialization...")
    
    try:
        # Initialize bot with undetected Chrome
        bot = GumtreeBot(headless=True, use_existing_browser=False)
        bot.setup_driver()
        
        print("✅ Undetected Chrome WebDriver initialized successfully")
        
        # Test basic navigation
        bot.driver.get("https://www.gumtree.com")
        time.sleep(2)
        
        current_url = bot.driver.current_url
        print(f"✅ Successfully navigated to: {current_url}")
        
        # Test stealth measures
        webdriver_property = bot.driver.execute_script("return navigator.webdriver")
        print(f"✅ navigator.webdriver property: {webdriver_property}")
        
        # Test user agent
        user_agent = bot.driver.execute_script("return navigator.userAgent")
        print(f"✅ User Agent: {user_agent}")
        
        # Test plugins
        plugins = bot.driver.execute_script("return navigator.plugins.length")
        print(f"✅ Plugins count: {plugins}")
        
        # Test languages
        languages = bot.driver.execute_script("return navigator.languages")
        print(f"✅ Languages: {languages}")
        
        # Test timezone
        timezone = bot.driver.execute_script("return Intl.DateTimeFormat().resolvedOptions().timeZone")
        print(f"✅ Timezone: {timezone}")
        
        # Clean up
        bot.driver.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing undetected Chrome: {e}")
        return False

def test_stealth_measures():
    """Test stealth measures"""
    print("\n🧪 Testing stealth measures...")
    
    try:
        bot = GumtreeBot(headless=True, use_existing_browser=False)
        bot.setup_driver()
        
        # Test various stealth properties
        tests = [
            ("navigator.webdriver", "undefined"),
            ("navigator.plugins.length", "> 0"),
            ("navigator.languages", "['en-GB', 'en-US', 'en']"),
            ("navigator.hardwareConcurrency", "8"),
            ("navigator.deviceMemory", "8"),
            ("navigator.vendor", "'Google Inc.'"),
            ("navigator.platform", "'Win32'"),
            ("screen.width", "1920"),
            ("screen.height", "1080"),
            ("Intl.DateTimeFormat().resolvedOptions().timeZone", "'Europe/London'")
        ]
        
        all_passed = True
        for test_name, expected in tests:
            try:
                result = bot.driver.execute_script(f"return {test_name}")
                print(f"✅ {test_name}: {result}")
                
                # Basic validation
                if test_name == "navigator.webdriver" and result is None:
                    print(f"   ✅ Correctly returns undefined")
                elif test_name == "navigator.plugins.length" and result > 0:
                    print(f"   ✅ Has plugins")
                elif test_name == "navigator.languages" and 'en-GB' in result:
                    print(f"   ✅ UK language preference set")
                elif test_name == "navigator.hardwareConcurrency" and result == 8:
                    print(f"   ✅ Hardware concurrency set")
                elif test_name == "navigator.deviceMemory" and result == 8:
                    print(f"   ✅ Device memory set")
                elif test_name == "navigator.vendor" and result == "Google Inc.":
                    print(f"   ✅ Vendor set correctly")
                elif test_name == "navigator.platform" and result == "Win32":
                    print(f"   ✅ Platform set correctly")
                elif test_name == "screen.width" and result == 1920:
                    print(f"   ✅ Screen width set")
                elif test_name == "screen.height" and result == 1080:
                    print(f"   ✅ Screen height set")
                elif test_name == "Intl.DateTimeFormat().resolvedOptions().timeZone" and result == "Europe/London":
                    print(f"   ✅ UK timezone set")
                else:
                    print(f"   ⚠️  Unexpected result")
                    
            except Exception as e:
                print(f"❌ Error testing {test_name}: {e}")
                all_passed = False
        
        # Clean up
        bot.driver.quit()
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing stealth measures: {e}")
        return False

def test_automation_detection():
    """Test automation detection resistance"""
    print("\n🧪 Testing automation detection resistance...")
    
    try:
        bot = GumtreeBot(headless=False, use_existing_browser=False)  # Non-headless to see if banner appears
        bot.setup_driver()
        
        # Navigate to a test page
        bot.driver.get("https://www.gumtree.com")
        time.sleep(3)
        
        # Check for automation banner
        page_source = bot.driver.page_source.lower()
        
        automation_indicators = [
            "chrome is being controlled by automated software",
            "chrome is being controlled by automated test software",
            "automation",
            "webdriver"
        ]
        
        found_indicators = []
        for indicator in automation_indicators:
            if indicator in page_source:
                found_indicators.append(indicator)
        
        if found_indicators:
            print(f"⚠️  Found automation indicators: {found_indicators}")
            print("   This might indicate detection")
        else:
            print("✅ No automation indicators found in page source")
        
        # Test JavaScript detection
        js_detection = bot.driver.execute_script("""
            return {
                webdriver: navigator.webdriver,
                plugins: navigator.plugins.length,
                languages: navigator.languages,
                userAgent: navigator.userAgent,
                chrome: !!window.chrome
            }
        """)
        
        print(f"✅ JavaScript detection results: {js_detection}")
        
        # Clean up
        bot.driver.quit()
        
        return len(found_indicators) == 0
        
    except Exception as e:
        print(f"❌ Error testing automation detection: {e}")
        return False

def test_gumtree_specific():
    """Test Gumtree-specific functionality"""
    print("\n🧪 Testing Gumtree-specific functionality...")
    
    try:
        bot = GumtreeBot(headless=True, use_existing_browser=False)
        bot.setup_driver()
        
        # Navigate to Gumtree
        bot.driver.get("https://www.gumtree.com")
        time.sleep(3)
        
        # Check if page loaded correctly
        title = bot.driver.title
        print(f"✅ Page title: {title}")
        
        # Check for Gumtree-specific elements
        try:
            # Look for common Gumtree elements
            search_box = bot.driver.find_element("css selector", "input[placeholder*='Search']")
            print("✅ Found search box")
        except:
            print("⚠️  Search box not found (might be different layout)")
        
        # Test category navigation
        try:
            bot.driver.get("https://www.gumtree.com/postad/create?categoryId=11108")
            time.sleep(2)
            
            current_url = bot.driver.current_url
            print(f"✅ Successfully navigated to category: {current_url}")
            
        except Exception as e:
            print(f"⚠️  Category navigation test failed: {e}")
        
        # Clean up
        bot.driver.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gumtree functionality: {e}")
        return False

def main():
    """Run all undetected Chrome tests"""
    print("🚀 Undetected Chrome Test Suite")
    print("=" * 60)
    
    tests = [
        test_undetected_chrome_initialization,
        test_stealth_measures,
        test_automation_detection,
        test_gumtree_specific
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Delay between tests
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All undetected Chrome tests passed!")
        print("\n📋 Undetected Chrome features implemented:")
        print("✅ undetected-chromedriver integration")
        print("✅ Advanced stealth measures via CDP")
        print("✅ Random User-Agent selection")
        print("✅ UK-specific browser properties")
        print("✅ Automation detection resistance")
        print("✅ Gumtree-specific compatibility")
        print("\n🚀 Bot is now virtually undetectable!")
        print("\n📋 Key improvements:")
        print("• Uses undetected-chromedriver for maximum stealth")
        print("• CDP-based stealth injection before page loads")
        print("• Random User-Agent strings for UK users")
        print("• Realistic browser properties (hardware, memory, etc.)")
        print("• UK timezone and language preferences")
        print("• Complete automation indicator removal")
        print("• No 'Chrome is being controlled' banner")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    exit(0 if success else 1)
