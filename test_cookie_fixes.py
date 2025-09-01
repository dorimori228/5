#!/usr/bin/env python3
"""
Test script to verify the cookie fixes work properly
"""

import json
import os
import time
import logging
from gumtree_bot import GumtreeBot

# Set up detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_cookie_persistence():
    """Test the improved cookie saving and loading"""
    
    print("🧪 Testing Cookie Persistence Fixes")
    print("=" * 50)
    
    # Clean up any existing cookies for a fresh test
    cookies_file = "gumtree_cookies.json"
    if os.path.exists(cookies_file):
        print(f"📁 Found existing cookies file, backing up...")
        backup_file = f"{cookies_file}.backup"
        os.rename(cookies_file, backup_file)
        print(f"   Backed up to: {backup_file}")
    
    bot = None
    
    try:
        # Initialize bot
        print("\n1️⃣ Initializing bot...")
        bot = GumtreeBot(headless=False, use_existing_browser=False)
        bot.setup_driver()
        
        # Navigate to Gumtree
        print("\n2️⃣ Navigating to Gumtree...")
        bot.navigate_to_gumtree()
        
        # Check initial login status
        print("\n3️⃣ Checking initial login status...")
        is_logged_in = bot.is_logged_in()
        print(f"   Status: {'✅ Logged in' if is_logged_in else '❌ Not logged in'}")
        
        if not is_logged_in:
            print("\n4️⃣ Manual login required...")
            print("   Please log in to Gumtree in the browser window")
            print("   Make sure you can see your account menu or profile")
            input("   Press Enter after logging in...")
            
            # Check if login worked
            is_logged_in = bot.is_logged_in()
            if is_logged_in:
                print("   ✅ Login successful!")
                
                # Save cookies
                print("\n5️⃣ Saving cookies...")
                bot.save_cookies()
                
                # Verify cookies were saved
                if os.path.exists(cookies_file):
                    file_size = os.path.getsize(cookies_file)
                    print(f"   ✅ Cookies saved successfully ({file_size} bytes)")
                    
                    # Show cookie info
                    with open(cookies_file, 'r') as f:
                        cookies = json.load(f)
                    print(f"   📊 Saved {len(cookies)} cookies")
                    
                    # Show domain distribution
                    domains = {}
                    for cookie in cookies:
                        domain = cookie.get('domain', 'unknown')
                        domains[domain] = domains.get(domain, 0) + 1
                    
                    print("   🌐 Domain distribution:")
                    for domain, count in domains.items():
                        print(f"      {domain}: {count} cookies")
                else:
                    print("   ❌ Cookie file was not created!")
                    return False
            else:
                print("   ❌ Login not detected!")
                return False
        else:
            print("\n4️⃣ Already logged in, saving current session...")
            bot.save_cookies()
        
        # Now test loading cookies in a new session
        print("\n6️⃣ Testing cookie loading in new session...")
        print("   Closing current browser...")
        bot.driver.quit()
        
        # Start new bot instance
        print("   Starting new bot instance...")
        bot2 = GumtreeBot(headless=False, use_existing_browser=False)
        bot2.setup_driver()
        
        # Navigate to Gumtree
        print("   Navigating to Gumtree...")
        bot2.navigate_to_gumtree()
        
        # Check login status before loading cookies
        print("   Checking login status before loading cookies...")
        is_logged_in_before = bot2.is_logged_in()
        print(f"   Status: {'✅ Logged in' if is_logged_in_before else '❌ Not logged in'}")
        
        # Load cookies
        print("   Loading saved cookies...")
        cookies_loaded = bot2.load_cookies()
        
        if cookies_loaded:
            print("   ✅ Cookies loaded successfully!")
            
            # Check login status after loading cookies
            print("   Checking login status after loading cookies...")
            is_logged_in_after = bot2.is_logged_in()
            print(f"   Status: {'✅ Logged in' if is_logged_in_after else '❌ Still not logged in'}")
            
            if is_logged_in_after:
                print("\n🎉 SUCCESS: Cookie persistence is working!")
                print("   ✅ Cookies were saved and loaded successfully")
                print("   ✅ Auto-login is working")
                return True
            else:
                print("\n⚠️  PARTIAL SUCCESS: Cookies loaded but login not detected")
                print("   This might be due to:")
                print("   - Session cookies that expired")
                print("   - Additional authentication required")
                print("   - Gumtree's security measures")
                return False
        else:
            print("   ❌ Failed to load cookies!")
            return False
            
    except Exception as e:
        print(f"\n💥 Error during test: {e}")
        import traceback
        print(traceback.format_exc())
        return False
    
    finally:
        # Cleanup
        if bot and bot.driver:
            try:
                bot.driver.quit()
            except:
                pass
        
        # Restore backup if it exists
        backup_file = f"{cookies_file}.backup"
        if os.path.exists(backup_file):
            if os.path.exists(cookies_file):
                os.remove(cookies_file)
            os.rename(backup_file, cookies_file)
            print(f"\n🔄 Restored original cookies file from backup")

def main():
    """Main test function"""
    print("Gumtree Bot Cookie Fix Test")
    print("=" * 40)
    print("This test will verify that the cookie saving/loading fixes work properly.")
    print("You may need to log in manually during the test.")
    print()
    
    response = input("Do you want to run the test? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Test cancelled.")
        return
    
    success = test_cookie_persistence()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST PASSED: Cookie persistence is working correctly!")
        print("Your bot should now automatically log in using saved cookies.")
    else:
        print("❌ TEST FAILED: Cookie persistence needs more work.")
        print("Check the logs above for specific issues.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
