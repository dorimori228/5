#!/usr/bin/env python3
"""
Test script to verify anti-detection measures work
"""

import time
import logging
from gumtree_bot import GumtreeBot

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_anti_detection():
    """Test if the bot can avoid detection"""
    
    print("🕵️ Testing Anti-Detection Measures")
    print("=" * 50)
    print("This test will check if the bot can avoid Chrome automation detection.")
    print()
    
    bot = None
    
    try:
        # Initialize bot
        print("1️⃣ Starting bot with anti-detection measures...")
        bot = GumtreeBot(headless=False, use_existing_browser=False)
        bot.setup_driver()
        
        # Navigate to a test site that detects automation
        print("2️⃣ Navigating to bot detection test site...")
        bot.driver.get("https://bot.sannysoft.com/")
        time.sleep(5)
        
        # Check for automation indicators
        print("3️⃣ Checking for automation indicators...")
        
        # Test webdriver property
        webdriver_detected = bot.driver.execute_script("return navigator.webdriver")
        print(f"   Webdriver property: {'❌ DETECTED' if webdriver_detected else '✅ HIDDEN'}")
        
        # Test plugins
        plugins = bot.driver.execute_script("return navigator.plugins.length")
        print(f"   Plugins count: {plugins} {'✅ REALISTIC' if plugins > 0 else '❌ SUSPICIOUS'}")
        
        # Test languages
        languages = bot.driver.execute_script("return navigator.languages")
        print(f"   Languages: {languages} {'✅ REALISTIC' if languages else '❌ SUSPICIOUS'}")
        
        # Test chrome runtime
        chrome_runtime = bot.driver.execute_script("return typeof window.chrome")
        print(f"   Chrome runtime: {'✅ PRESENT' if chrome_runtime == 'object' else '❌ MISSING'}")
        
        # Test automation indicators
        automation_indicators = bot.driver.execute_script("""
            return {
                cdc_Array: typeof window.cdc_adoQpoasnfa76pfcZLmcfl_Array,
                cdc_Promise: typeof window.cdc_adoQpoasnfa76pfcZLmcfl_Promise,
                cdc_Symbol: typeof window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol
            }
        """)
        
        print("   Automation indicators:")
        for key, value in automation_indicators.items():
            status = "✅ REMOVED" if value == "undefined" else "❌ PRESENT"
            print(f"      {key}: {status}")
        
        # Test user agent
        user_agent = bot.driver.execute_script("return navigator.userAgent")
        print(f"   User Agent: {user_agent[:50]}...")
        
        # Overall assessment
        print("\n4️⃣ Overall Assessment:")
        
        issues = []
        if webdriver_detected:
            issues.append("Webdriver property detected")
        if plugins == 0:
            issues.append("No plugins detected")
        if not languages:
            issues.append("No languages detected")
        if chrome_runtime != 'object':
            issues.append("Chrome runtime missing")
        
        for key, value in automation_indicators.items():
            if value != "undefined":
                issues.append(f"{key} still present")
        
        if not issues:
            print("   🎉 SUCCESS: All anti-detection measures working!")
            print("   ✅ Bot should not be detected as automated")
            return True
        else:
            print("   ⚠️  ISSUES FOUND:")
            for issue in issues:
                print(f"      - {issue}")
            print("   ❌ Bot may still be detectable")
            return False
            
    except Exception as e:
        print(f"\n💥 Error during test: {e}")
        import traceback
        print(traceback.format_exc())
        return False
    
    finally:
        if bot and bot.driver:
            input("\nPress Enter to close browser...")
            bot.driver.quit()

def main():
    """Main test function"""
    print("Anti-Detection Test for Gumtree Bot")
    print("=" * 40)
    print("This test checks if the bot can avoid Chrome automation detection.")
    print("The bot will open a browser and navigate to a detection test site.")
    print()
    
    response = input("Do you want to run the anti-detection test? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Test cancelled.")
        return
    
    success = test_anti_detection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ANTI-DETECTION TEST PASSED!")
        print("Your bot should now avoid Chrome automation warnings.")
    else:
        print("❌ ANTI-DETECTION TEST FAILED!")
        print("The bot may still be detectable. Check the issues above.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
