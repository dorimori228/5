"""
Gumtree Auto Lister Bot

A Selenium-based bot that automates the process of listing items on Gumtree.
Supports automatic login via saved cookies and step-by-step item listing.
"""

import json
import os
import time
import random
from typing import Dict, List, Optional, Any
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set specific loggers to WARNING level for speed
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('undetected_chromedriver').setLevel(logging.WARNING)


class GumtreeBot:
    """
    Gumtree Auto Lister Bot for automating item listings
    """
    
    def __init__(self, cookies_file: str = "gumtree_cookies.json", headless: bool = False, use_existing_browser: bool = True, user_data_dir: str = None):
        """
        Initialize the Gumtree bot
        
        Args:
            cookies_file (str): Path to the cookies file for auto-login
            headless (bool): Whether to run browser in headless mode
            use_existing_browser (bool): Whether to connect to existing browser session
            user_data_dir (str): Path to Chrome user data directory
        """
        self.cookies_file = cookies_file
        self.headless = headless
        self.use_existing_browser = use_existing_browser
        self.driver = None
        self.wait = None
        self.base_url = "https://www.gumtree.com/"
        
        # Set up user data directory
        if user_data_dir is None:
            self.user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
        else:
            self.user_data_dir = user_data_dir
        
    def setup_driver(self) -> None:
        """Set up the Chrome WebDriver with appropriate options"""
        chrome_options = uc.ChromeOptions()
        
        if self.use_existing_browser:
            # Try to connect to existing browser first
            if self.connect_to_existing_browser():
                return
            else:
                logger.info("No existing browser found, starting new instance...")
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Add debugging port for future connections
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Use persistent user data directory for better cookie persistence
        user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        logger.info(f"Using persistent user data directory: {user_data_dir}")
        
        # Add various Chrome options for better compatibility and reduced errors
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        
        # Advanced anti-detection measures to completely hide automation
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # Note: undetected-chromedriver handles automation hiding automatically
        
        # Additional stealth arguments for complete invisibility
        chrome_options.add_argument("--disable-automation")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-web-resources")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-infobars")  # Prevents "Chrome is being controlled by automated test software" message
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-gpu-logging")
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--log-level=3")
        
        # Remove automation indicators
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-extensions-with-background-pages")
        chrome_options.add_argument("--disable-domain-reliability")
        chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-web-resources")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-web-resources")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        
        # Set a realistic user agent and remove automation headers
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Additional stealth options
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-gpu-logging")
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-gpu-logging")
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--log-level=3")
        
        # Set window size to match the recorded viewport
        chrome_options.add_argument("--window-size=1184,729")
        
        # Suppress logging
        chrome_options.add_argument("--log-level=3")
        # Note: undetected-chromedriver handles logging suppression automatically
        
        try:
            # Initialize undetected Chrome driver for maximum stealth
            self.driver = uc.Chrome(
                options=chrome_options,
                version_main=None,  # Auto-detect Chrome version
                driver_executable_path=None,  # Auto-download chromedriver
                browser_executable_path=None,  # Use system Chrome
                user_data_dir=self.user_data_dir,
                headless=self.headless
            )
            
            # Advanced anti-detection JavaScript injection
            self.driver.execute_script("""
                // Safely remove webdriver property
                try {
                    delete navigator.webdriver;
                } catch(e) {}
                
                // Define webdriver property only if it doesn't exist
                if (!navigator.hasOwnProperty('webdriver')) {
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                        configurable: true
                    });
                }
                
                // Override the plugins property to use a custom getter
                if (!navigator.hasOwnProperty('plugins') || navigator.plugins.length === 0) {
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                        configurable: true
                    });
                }
                
                // Override the languages property to use a custom getter
                if (!navigator.hasOwnProperty('languages') || navigator.languages.length === 0) {
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en'],
                        configurable: true
                    });
                }
                
                // Override the permissions property
                if (window.navigator.permissions && window.navigator.permissions.query) {
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                    );
                }
                
                // Mock chrome runtime
                if (!window.chrome) {
                    window.chrome = {
                        runtime: {},
                    };
                }
                
                // Remove all automation indicators
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Reflect;
                
                // Mock realistic browser properties
                if (!navigator.hasOwnProperty('hardwareConcurrency') || navigator.hardwareConcurrency === 0) {
                    Object.defineProperty(navigator, 'hardwareConcurrency', {
                        get: () => 8,
                        configurable: true
                    });
                }
                
                if (!navigator.hasOwnProperty('deviceMemory') || navigator.deviceMemory === 0) {
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => 8,
                        configurable: true
                    });
                }
                
                // Remove automation from window object
                delete window.webdriver;
                delete window.domAutomation;
                delete window.domAutomationController;
                
                // Override toString methods safely
                try {
                    navigator.toString = function() { return '[object Navigator]'; };
                    window.toString = function() { return '[object Window]'; };
                } catch(e) {}
                
                // Additional stealth measures
                Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 0 });
                Object.defineProperty(navigator, 'vendor', { get: () => 'Google Inc.' });
                Object.defineProperty(navigator, 'vendorSub', { get: () => '' });
                Object.defineProperty(navigator, 'productSub', { get: () => '20030107' });
                Object.defineProperty(navigator, 'appName', { get: () => 'Netscape' });
                Object.defineProperty(navigator, 'appVersion', { get: () => '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' });
                Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
                Object.defineProperty(navigator, 'cookieEnabled', { get: () => true });
                Object.defineProperty(navigator, 'doNotTrack', { get: () => null });
                Object.defineProperty(navigator, 'onLine', { get: () => true });
                
                // Mock screen properties
                Object.defineProperty(screen, 'width', { get: () => 1920 });
                Object.defineProperty(screen, 'height', { get: () => 1080 });
                Object.defineProperty(screen, 'availWidth', { get: () => 1920 });
                Object.defineProperty(screen, 'availHeight', { get: () => 1040 });
                Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
                Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });
                
                // Mock timezone
                Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {
                    value: function() {
                        return { timeZone: 'Europe/London' };
                    }
                });
                
                // Remove automation detection methods
                delete window.callPhantom;
                delete window._phantom;
                delete window.__phantom;
                delete window.Buffer;
                delete window.emit;
                delete window.spawn;
                
                // Mock realistic timing
                const originalDate = Date;
                Date = class extends originalDate {
                    constructor(...args) {
                        if (args.length === 0) {
                            super(originalDate.now() + Math.random() * 1000);
                        } else {
                            super(...args);
                        }
                    }
                };
            """)
            
            self.wait = WebDriverWait(self.driver, 10)
            
            # Apply advanced stealth measures using CDP (Chrome DevTools Protocol)
            self._apply_stealth_measures()
            
            logger.info("Undetected Chrome WebDriver initialized successfully with maximum stealth")
        except Exception as e:
            logger.error(f"Failed to initialize undetected Chrome WebDriver: {e}")
            raise
    
    def _apply_stealth_measures(self) -> None:
        """
        Apply advanced stealth measures using Chrome DevTools Protocol
        
        This method uses CDP commands to inject stealth scripts before any page loads,
        making the browser completely undetectable by anti-bot systems.
        """
        try:
            # Override navigator.webdriver property before any page loads
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    // Remove webdriver property completely
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                        configurable: true
                    });
                    
                    // Override automation indicators
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-GB', 'en-US', 'en'],
                        configurable: true
                    });
                    
                    // Mock realistic browser properties for UK users
                    Object.defineProperty(navigator, 'hardwareConcurrency', {
                        get: () => 8,
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => 8,
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'maxTouchPoints', {
                        get: () => 0,
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'vendor', {
                        get: () => 'Google Inc.',
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'vendorSub', {
                        get: () => '',
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'productSub', {
                        get: () => '20030107',
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'appName', {
                        get: () => 'Netscape',
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'platform', {
                        get: () => 'Win32',
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'cookieEnabled', {
                        get: () => true,
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'doNotTrack', {
                        get: () => null,
                        configurable: true
                    });
                    
                    Object.defineProperty(navigator, 'onLine', {
                        get: () => true,
                        configurable: true
                    });
                    
                    // Mock screen properties
                    Object.defineProperty(screen, 'width', {
                        get: () => 1920,
                        configurable: true
                    });
                    
                    Object.defineProperty(screen, 'height', {
                        get: () => 1080,
                        configurable: true
                    });
                    
                    Object.defineProperty(screen, 'availWidth', {
                        get: () => 1920,
                        configurable: true
                    });
                    
                    Object.defineProperty(screen, 'availHeight', {
                        get: () => 1040,
                        configurable: true
                    });
                    
                    Object.defineProperty(screen, 'colorDepth', {
                        get: () => 24,
                        configurable: true
                    });
                    
                    Object.defineProperty(screen, 'pixelDepth', {
                        get: () => 24,
                        configurable: true
                    });
                    
                    // Mock timezone for UK
                    Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {
                        value: function() {
                            return { timeZone: 'Europe/London' };
                        }
                    });
                    
                    // Remove automation detection methods
                    delete window.callPhantom;
                    delete window._phantom;
                    delete window.__phantom;
                    delete window.Buffer;
                    delete window.emit;
                    delete window.spawn;
                    delete window.webdriver;
                    delete window.domAutomation;
                    delete window.domAutomationController;
                    
                    // Additional stealth measures for maximum undetectability
                    Object.defineProperty(navigator, 'permissions', {
                        get: () => ({
                            query: () => Promise.resolve({ state: 'granted' })
                        }),
                        configurable: true
                    });
                    
                    // Mock realistic connection properties
                    Object.defineProperty(navigator, 'connection', {
                        get: () => ({
                            effectiveType: '4g',
                            downlink: 10,
                            rtt: 50
                        }),
                        configurable: true
                    });
                    
                    // Override automation detection properties
                    Object.defineProperty(window, 'outerHeight', {
                        get: () => 1080,
                        configurable: true
                    });
                    
                    Object.defineProperty(window, 'outerWidth', {
                        get: () => 1920,
                        configurable: true
                    });
                    
                    // Mock realistic timing with slight randomization
                    const originalNow = Date.now;
                    Date.now = function() {
                        return originalNow() + Math.floor(Math.random() * 100);
                    };
                    
                    // Remove Chrome automation indicators
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Reflect;
                    
                    // Override toString methods
                    navigator.toString = function() { return '[object Navigator]'; };
                    window.toString = function() { return '[object Window]'; };
                    
                    // Mock chrome runtime
                    if (!window.chrome) {
                        window.chrome = {
                            runtime: {},
                        };
                    }
                    
                    // Override permissions API
                    if (window.navigator.permissions && window.navigator.permissions.query) {
                        const originalQuery = window.navigator.permissions.query;
                        window.navigator.permissions.query = (parameters) => (
                            parameters.name === 'notifications' ?
                                Promise.resolve({ state: Notification.permission }) :
                                originalQuery(parameters)
                        );
                    }
                """
            })
            
            logger.info("Advanced stealth measures applied via Chrome DevTools Protocol")
            
        except Exception as e:
            logger.warning(f"Could not apply all stealth measures: {e}")
            # Fallback to basic stealth injection
            self._apply_basic_stealth()
    
    def _apply_basic_stealth(self) -> None:
        """
        Fallback stealth measures using execute_script
        """
        try:
            self.driver.execute_script("""
                // Basic stealth injection as fallback
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true
                });
                
                delete window.webdriver;
                delete window.domAutomation;
                delete window.domAutomationController;
            """)
            logger.info("Basic stealth measures applied as fallback")
        except Exception as e:
            logger.warning(f"Could not apply basic stealth measures: {e}")
    
    def upload_image(self, image_path: str) -> bool:
        """Force upload image and confirm it appears in the preview"""
        try:
            file_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][accept*='image']"))
            )
            # Make sure input is visible
            self.driver.execute_script("arguments[0].style.display = 'block';", file_input)
            file_input.send_keys(image_path)
            logger.info(f"Uploaded image: {image_path}")

            # Wait for preview/thumbnail to appear
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='thumbnail'] img"))
                )
                logger.info("✓ Image preview detected, upload confirmed")
                return True
            except TimeoutException:
                logger.warning("⚠ No thumbnail preview detected, upload may have failed")
                return False

        except Exception as e:
            logger.error(f"Image upload failed for {image_path}: {e}")
            return False
    
    def connect_to_existing_browser(self) -> bool:
        """Try to connect to an existing Chrome browser with debugging enabled"""
        try:
            import requests
            
            # Check if there's a browser running on the debugging port
            try:
                response = requests.get("http://localhost:9222/json", timeout=2)
                tabs = response.json()
                
                if tabs:
                    logger.info(f"Found {len(tabs)} existing browser tabs")
                    
                    # Look for a Gumtree tab
                    gumtree_tab = None
                    for tab in tabs:
                        if 'gumtree.com' in tab.get('url', '').lower():
                            gumtree_tab = tab
                            break
                    
                    if gumtree_tab:
                        logger.info(f"Found existing Gumtree tab: {gumtree_tab['title']}")
                    else:
                        logger.info("No Gumtree tab found, will use first available tab")
                        gumtree_tab = tabs[0] if tabs else None
                    
                    if gumtree_tab:
                        # Connect to existing browser
                        chrome_options = uc.ChromeOptions()
                        chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
                        
                        try:
                            self.driver = uc.Chrome(options=chrome_options)
                            self.wait = WebDriverWait(self.driver, 10)
                            
                            # Navigate to Gumtree if not already there
                            current_url = self.driver.current_url
                            if 'gumtree.com' not in current_url.lower():
                                self.driver.get(self.base_url)
                                
                                # Wait for page to load instead of fixed sleep
                                try:
                                    self.wait.until(
                                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                                    )
                                except TimeoutException:
                                    logger.warning("Page didn't load as expected, continuing anyway")
                            
                            logger.info(f"Successfully connected to existing browser. Current URL: {current_url}")
                            return True
                            
                        except Exception as connect_error:
                            logger.warning(f"Failed to connect to existing browser: {connect_error}")
                            return False
                        
            except requests.exceptions.RequestException:
                logger.debug("No existing browser with debugging found")
                return False
                
        except ImportError:
            logger.info("requests module not available, cannot connect to existing browser")
            return False
        except Exception as e:
            logger.debug(f"Error connecting to existing browser: {e}")
            return False
        
        return False
    
    def save_cookies(self) -> None:
        """Save current browser cookies to file"""
        try:
            # Make sure we're on the right domain
            current_url = self.driver.current_url
            logger.info(f"Current URL when saving cookies: {current_url}")
            
            if 'gumtree.com' not in current_url:
                logger.warning(f"Not on Gumtree domain ({current_url}), navigating to homepage first")
                self.navigate_to_gumtree()
            
            # Get all cookies
            cookies = self.driver.get_cookies()
            logger.info(f"Found {len(cookies)} cookies to save")
            
            # Filter and clean cookies
            valid_cookies = []
            for cookie in cookies:
                # Ensure required fields are present
                if 'name' in cookie and 'value' in cookie:
                    # Create a clean cookie object with all necessary fields
                    clean_cookie = {
                        'name': cookie['name'],
                        'value': cookie['value']
                    }
                    
                    # Add optional fields if they exist
                    if 'domain' in cookie and cookie['domain']:
                        clean_cookie['domain'] = cookie['domain']
                    if 'path' in cookie:
                        clean_cookie['path'] = cookie['path']
                    if 'secure' in cookie:
                        clean_cookie['secure'] = cookie['secure']
                    if 'httpOnly' in cookie:
                        clean_cookie['httpOnly'] = cookie['httpOnly']
                    if 'sameSite' in cookie:
                        clean_cookie['sameSite'] = cookie['sameSite']
                    if 'expiry' in cookie:
                        clean_cookie['expiry'] = cookie['expiry']
                    
                    valid_cookies.append(clean_cookie)
                    logger.debug(f"Valid cookie: {cookie['name']} (domain: {cookie.get('domain', 'default')})")
                else:
                    logger.warning(f"Invalid cookie structure: {cookie}")
            
            # Save to file with proper formatting
            with open(self.cookies_file, 'w') as f:
                json.dump(valid_cookies, f, indent=2)
            
            logger.info(f"Successfully saved {len(valid_cookies)} cookies to {self.cookies_file}")
            
            # Verify file was created and show some stats
            if os.path.exists(self.cookies_file):
                file_size = os.path.getsize(self.cookies_file)
                logger.info(f"Cookie file created successfully, size: {file_size} bytes")
                
                # Show domain distribution
                domains = {}
                for cookie in valid_cookies:
                    domain = cookie.get('domain', 'unknown')
                    domains[domain] = domains.get(domain, 0) + 1
                
                logger.info("Cookie domain distribution:")
                for domain, count in domains.items():
                    logger.info(f"  {domain}: {count} cookies")
            else:
                logger.error("Cookie file was not created!")
                
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
    
    def load_cookies(self) -> bool:
        """
        Load cookies from file and apply them to the browser
        
        Returns:
            bool: True if cookies were loaded successfully, False otherwise
        """
        logger.info(f"Attempting to load cookies from: {self.cookies_file}")
        
        if not os.path.exists(self.cookies_file):
            logger.info(f"Cookies file {self.cookies_file} not found")
            return False
        
        try:
            file_size = os.path.getsize(self.cookies_file)
            logger.info(f"Found cookie file, size: {file_size} bytes")
            
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
            
            if not cookies:
                logger.info("No cookies found in file")
                return False
            
            logger.info(f"Loaded {len(cookies)} cookies from file")
            
            # First navigate to the domain and wait for it to fully load
            logger.info("Navigating to Gumtree to set up cookie domain...")
            self.driver.get(self.base_url)
            time.sleep(3)  # Give more time for page to load
            
            # Clear existing cookies first to avoid conflicts
            logger.info("Clearing existing cookies...")
            self.driver.delete_all_cookies()
            
            # Add each cookie with proper domain handling
            loaded_count = 0
            failed_count = 0
            
            for cookie in cookies:
                try:
                    # Ensure cookie has required fields
                    if 'name' in cookie and 'value' in cookie:
                        # Create clean cookie object
                        clean_cookie = {
                            'name': cookie['name'],
                            'value': cookie['value']
                        }
                        
                        # Handle domain - normalize to work with both .gumtree.com and www.gumtree.com
                        if 'domain' in cookie and cookie['domain']:
                            domain = cookie['domain']
                            # If domain starts with .gumtree.com, use it as is
                            # If domain is www.gumtree.com, convert to .gumtree.com for broader scope
                            if domain == 'www.gumtree.com':
                                clean_cookie['domain'] = '.gumtree.com'
                            else:
                                clean_cookie['domain'] = domain
                        else:
                            # Default to .gumtree.com if no domain specified
                            clean_cookie['domain'] = '.gumtree.com'
                        
                        # Add other optional fields
                        if 'path' in cookie:
                            clean_cookie['path'] = cookie['path']
                        if 'secure' in cookie:
                            clean_cookie['secure'] = cookie['secure']
                        if 'httpOnly' in cookie:
                            clean_cookie['httpOnly'] = cookie['httpOnly']
                        if 'sameSite' in cookie:
                            clean_cookie['sameSite'] = cookie['sameSite']
                        
                        # Try to add the cookie
                        self.driver.add_cookie(clean_cookie)
                        loaded_count += 1
                        logger.debug(f"Loaded cookie: {cookie['name']} (domain: {clean_cookie.get('domain', 'default')})")
                        
                except Exception as e:
                    failed_count += 1
                    logger.warning(f"Failed to add cookie {cookie.get('name', 'unknown')}: {e}")
                    continue
            
            logger.info(f"Successfully loaded {loaded_count}/{len(cookies)} cookies ({failed_count} failed)")
            
            # Refresh the page to apply the cookies
            logger.info("Refreshing page to apply loaded cookies...")
            self.driver.refresh()
            
            # Wait for page to reload instead of fixed sleep
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                logger.warning("Page didn't reload as expected, continuing anyway")
            
            return loaded_count > 0
            
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def wait_for_manual_login(self) -> None:
        """Wait for user to manually log in and then save cookies"""
        logger.info("="*50)
        logger.info("MANUAL LOGIN REQUIRED")
        logger.info("="*50)
        logger.info("1. Please log in manually in the browser window")
        logger.info("2. After logging in, make sure you're on the Gumtree homepage")
        logger.info("3. You should see your account menu or 'Post an ad' button")
        logger.info("4. Press Enter in this console when login is complete")
        logger.info("="*50)
        
        max_attempts = 3
        attempt = 1
        
        while attempt <= max_attempts:
            logger.info(f"\nAttempt {attempt}/{max_attempts}")
            input(f"Press Enter after completing login (attempt {attempt})...")
            
            # Give the page a moment to settle
            logger.info("Checking login status...")
            time.sleep(2)
            
            # Check if user is actually logged in
            if self.is_logged_in():
                logger.info("✓ Login successful! Saving cookies...")
                self.save_cookies()
                
                # Verify cookies were saved
                if os.path.exists(self.cookies_file):
                    logger.info("✓ Cookies saved successfully for future automatic login!")
                else:
                    logger.warning("⚠ Cookies might not have been saved properly")
                
                break
            else:
                logger.warning(f"✗ Login not detected (attempt {attempt}/{max_attempts})")
                logger.info("Please ensure you:")
                logger.info("  - Are logged into Gumtree")
                logger.info("  - Are on the Gumtree homepage (https://www.gumtree.com/)")
                logger.info("  - Can see your account menu or profile")
                
                if attempt < max_attempts:
                    retry = input("\nPress Enter to try again, or type 'skip' to continue anyway: ").lower().strip()
                    if retry == 'skip':
                        logger.warning("Proceeding without confirmed login - saving cookies anyway")
                        self.save_cookies()
                        break
                else:
                    logger.warning("Max attempts reached. Proceeding without confirmed login.")
                    self.save_cookies()  # Save anyway in case detection failed
                
                attempt += 1
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in to Gumtree"""
        try:
            logger.info("Checking login status...")
            
            # First check if driver session is still valid
            try:
                current_url = self.driver.current_url
                logger.debug(f"Current URL: {current_url}")
            except Exception as e:
                logger.error(f"Driver session invalid: {e}")
                return False
            
            # Wait a moment for page to load
            time.sleep(2)
            
            # Multiple indicators that user is logged in
            login_indicators = [
                # Look for user account elements (most reliable)
                "[data-testid='user-menu']",
                "[data-testid='account-menu']",
                "[data-testid='my-account']",
                # Look for account-related links
                "a[href*='/my-account']",
                "a[href*='/my-gumtree']",
                "a[href*='/account']",
                # Look for logout links (strong indicator of being logged in)
                "a[href*='logout']",
                "a[href*='sign-out']",
                # Look for profile/avatar elements
                ".user-avatar",
                ".profile-menu",
                # General account text indicators
                "text/My account",
                "text/My Gumtree",
                "text/Sign out",
                "text/Log out"
            ]
            
            logger.debug("Checking for login indicators...")
            for indicator in login_indicators:
                try:
                    if indicator.startswith("text/"):
                        text = indicator.replace("text/", "")
                        element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
                        logger.info(f"✓ Login detected via text: '{text}'")
                        return True
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, indicator)
                        logger.info(f"✓ Login detected via selector: {indicator}")
                        return True
                except NoSuchElementException:
                    logger.debug(f"Indicator not found: {indicator}")
                    continue
                except Exception as e:
                    logger.debug(f"Error checking indicator {indicator}: {e}")
                    continue
            
            # Check for login/register buttons (indicates NOT logged in)
            logger.debug("Checking for login/register buttons...")
            logout_indicators = [
                "text/Log in",
                "text/Sign in",
                "text/Login", 
                "text/Register",
                "text/Sign up",
                "a[href*='login']",
                "a[href*='signin']",
                "a[href*='register']",
                "[data-testid='login-button']",
                "[data-testid='signin-button']"
            ]
            
            for button in logout_indicators:
                try:
                    if button.startswith("text/"):
                        text = button.replace("text/", "")
                        element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
                        logger.info(f"✗ Not logged in - found login text: '{text}'")
                        return False
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, button)
                        logger.info(f"✗ Not logged in - found login element: {button}")
                        return False
                except NoSuchElementException:
                    logger.debug(f"Login button not found: {button}")
                    continue
                except Exception as e:
                    logger.debug(f"Error checking login button {button}: {e}")
                    continue
            
            # Additional check: look for post ad button (usually requires login)
            try:
                post_ad = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='post-ad-button']")
                if post_ad.is_displayed():
                    logger.info("✓ Post ad button visible - likely logged in")
                    return True
            except NoSuchElementException:
                logger.debug("Post ad button not found")
            except Exception as e:
                logger.debug(f"Error checking post ad button: {e}")
            
            # If we can't determine either way, let's check the page source for clues
            try:
                page_source = self.driver.page_source.lower()
                if 'my account' in page_source or 'logout' in page_source or 'sign out' in page_source:
                    logger.info("✓ Login detected via page source analysis")
                    return True
                elif 'log in' in page_source or 'login' in page_source or 'sign in' in page_source:
                    logger.info("✗ Not logged in - detected via page source analysis")
                    return False
            except Exception as e:
                logger.warning(f"Could not analyze page source: {e}")
            
            # Final fallback
            logger.warning("Could not determine login status definitively - assuming not logged in")
            return False
            
        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    def apply_anti_detection(self) -> None:
        """Apply anti-detection measures to the current page"""
        try:
            self.driver.execute_script("""
                // Safely remove webdriver property
                try {
                    delete navigator.webdriver;
                } catch(e) {}
                
                // Define webdriver property only if it doesn't exist
                if (!navigator.hasOwnProperty('webdriver')) {
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                        configurable: true
                    });
                }
                
                // Override the plugins property to use a custom getter
                if (!navigator.hasOwnProperty('plugins') || navigator.plugins.length === 0) {
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                        configurable: true
                    });
                }
                
                // Override the languages property to use a custom getter
                if (!navigator.hasOwnProperty('languages') || navigator.languages.length === 0) {
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en'],
                        configurable: true
                    });
                }
                
                // Mock chrome runtime
                if (!window.chrome) {
                    window.chrome = {
                        runtime: {},
                    };
                }
                
                // Remove all automation indicators
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Reflect;
                
                // Mock realistic browser properties
                if (!navigator.hasOwnProperty('hardwareConcurrency') || navigator.hardwareConcurrency === 0) {
                    Object.defineProperty(navigator, 'hardwareConcurrency', {
                        get: () => 8,
                        configurable: true
                    });
                }
                
                if (!navigator.hasOwnProperty('deviceMemory') || navigator.deviceMemory === 0) {
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => 8,
                        configurable: true
                    });
                }
                
                // Remove automation from window object
                delete window.webdriver;
                delete window.domAutomation;
                delete window.domAutomationController;
                
                // Override toString methods safely
                try {
                    navigator.toString = function() { return '[object Navigator]'; };
                    window.toString = function() { return '[object Window]'; };
                } catch(e) {}
                
                // Additional stealth measures
                Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 0 });
                Object.defineProperty(navigator, 'vendor', { get: () => 'Google Inc.' });
                Object.defineProperty(navigator, 'vendorSub', { get: () => '' });
                Object.defineProperty(navigator, 'productSub', { get: () => '20030107' });
                Object.defineProperty(navigator, 'appName', { get: () => 'Netscape' });
                Object.defineProperty(navigator, 'appVersion', { get: () => '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' });
                Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
                Object.defineProperty(navigator, 'cookieEnabled', { get: () => true });
                Object.defineProperty(navigator, 'doNotTrack', { get: () => null });
                Object.defineProperty(navigator, 'onLine', { get: () => true });
                
                // Mock screen properties
                Object.defineProperty(screen, 'width', { get: () => 1920 });
                Object.defineProperty(screen, 'height', { get: () => 1080 });
                Object.defineProperty(screen, 'availWidth', { get: () => 1920 });
                Object.defineProperty(screen, 'availHeight', { get: () => 1040 });
                Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
                Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });
                
                // Mock timezone
                Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {
                    value: function() {
                        return { timeZone: 'Europe/London' };
                    }
                });
                
                // Remove automation detection methods
                delete window.callPhantom;
                delete window._phantom;
                delete window.__phantom;
                delete window.Buffer;
                delete window.emit;
                delete window.spawn;
                
                // Mock realistic timing
                const originalDate = Date;
                Date = class extends originalDate {
                    constructor(...args) {
                        if (args.length === 0) {
                            super(originalDate.now() + Math.random() * 1000);
                        } else {
                            super(...args);
                        }
                    }
                };
            """)
            logger.debug("Applied anti-detection measures")
        except Exception as e:
            logger.debug(f"Could not apply anti-detection measures: {e}")

    def human_type(self, element, text: str, clear_first: bool = True) -> None:
        """
        Type text with human-like behavior including random delays and occasional mistakes
        
        Args:
            element: WebElement to type into
            text (str): Text to type
            clear_first (bool): Whether to clear the field first
        """
        try:
            # Clear the field if requested
            if clear_first:
                element.clear()
                time.sleep(random.uniform(0.1, 0.3))
            
            # Click on the element to focus it
            element.click()
            time.sleep(random.uniform(0.2, 0.5))
            
            # Type each character with human-like delays
            for i, char in enumerate(text):
                # Random typing speed (50-150ms per character)
                delay = random.uniform(0.05, 0.15)
                
                # Occasionally pause longer (thinking pause)
                if random.random() < 0.1:  # 10% chance
                    delay += random.uniform(0.3, 0.8)
                
                # Occasionally make a typo and correct it
                if random.random() < 0.05 and i > 0:  # 5% chance, not on first character
                    # Type wrong character
                    wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                    element.send_keys(wrong_char)
                    time.sleep(random.uniform(0.1, 0.3))
                    
                    # Backspace to correct
                    element.send_keys(Keys.BACKSPACE)
                    time.sleep(random.uniform(0.1, 0.2))
                
                # Type the correct character
                element.send_keys(char)
                time.sleep(delay)
            
            # Final pause after typing
            time.sleep(random.uniform(0.2, 0.5))
            
            logger.debug(f"Human-typed text: {text[:50]}{'...' if len(text) > 50 else ''}")
            
        except Exception as e:
            logger.error(f"Error in human typing: {e}")
            # Fallback to normal typing
            if clear_first:
                element.clear()
            element.send_keys(text)

    def navigate_to_gumtree(self) -> None:
        """Navigate to Gumtree homepage"""
        logger.info("Navigating to Gumtree...")
        self.driver.get(self.base_url)
        
        # Wait for page to load instead of fixed sleep
        try:
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            logger.warning("Page didn't load as expected, continuing anyway")
        
        # Apply anti-detection measures after page load
        self.apply_anti_detection()
    
    def ensure_logged_in(self) -> bool:
        """Ensure user is logged in, handling both cookie loading and manual login"""
        logger.info("Ensuring user is logged in...")
        
        # First navigate to Gumtree to check current status
        self.navigate_to_gumtree()
        
        # Check if already logged in (maybe from previous session)
        if self.is_logged_in():
            logger.info("✓ Already logged in! Saving current session cookies...")
            self.save_cookies()
            return True
        
        # Try to load existing cookies if not already logged in
        if self.load_cookies():
            logger.info("Cookies loaded, refreshing page to apply them...")
            self.navigate_to_gumtree()
            
            # Check if cookies worked and we're logged in
            if self.is_logged_in():
                logger.info("✓ Successfully authenticated using saved cookies!")
                return True
            else:
                logger.warning("✗ Saved cookies didn't work or have expired")
                # Delete invalid cookies
                try:
                    os.remove(self.cookies_file)
                    logger.info("Removed expired cookie file")
                except:
                    pass
        else:
            logger.info("No existing cookies found")
        
        # If we're still not logged in, prompt for manual login
        if not self.is_logged_in():
            logger.info("Manual login required")
            self.wait_for_manual_login()
            return True
        
        return True
    
    def click_location_element(self, selectors: List[List[str]], timeout: int = 15) -> bool:
        """
        Enhanced click method specifically for location selection with scrolling and visibility checks
        
        Args:
            selectors (List[List[str]]): List of selector lists to try
            timeout (int): Timeout in seconds
            
        Returns:
            bool: True if element was clicked successfully, False otherwise
        """
        logger.debug(f"Attempting to click location element with {len(selectors)} selector groups...")
        
        for i, selector_list in enumerate(selectors):
            logger.debug(f"Trying selector group {i+1}: {selector_list}")
            for j, selector in enumerate(selector_list):
                logger.debug(f"  Trying selector {j+1}: {selector}")
                try:
                    element = None
                    
                    # Try to find element with extended timeout for location elements
                    if selector.startswith("text/"):
                        text = selector.replace("text/", "")
                        # Enhanced text search for location elements
                        xpath_options = [
                            f"//button[contains(text(), '{text}')]",
                            f"//div[contains(text(), '{text}')]",
                            f"//li[contains(text(), '{text}')]",
                            f"//span[contains(text(), '{text}')]",
                            f"//a[contains(text(), '{text}')]",
                            f"//*[contains(text(), '{text}') and (self::button or self::a or self::div or self::li or self::span)]",
                            f"//*[normalize-space(text())='{text}']",
                            f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
                        ]
                        for xpath in xpath_options:
                            try:
                                element = WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, xpath))
                                )
                                break
                            except (TimeoutException, NoSuchElementException):
                                continue
                    elif selector.startswith("li:nth-of-type"):
                        # Handle nth-of-type selectors
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    else:
                        # Try as CSS selector first
                        try:
                            element = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                        except (TimeoutException, NoSuchElementException):
                            # Try as XPath
                            element = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, selector))
                            )
                    
                    if element:
                        # Scroll element into view
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                        
                        # Wait for element to be clickable
                        element = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(element)
                        )
                        
                        # Try multiple click methods
                        click_success = False
                        
                        # Method 1: JavaScript click
                        try:
                            self.driver.execute_script("arguments[0].click();", element)
                            click_success = True
                        except Exception as e:
                            logger.debug(f"JS click failed: {e}")
                        
                        # Method 2: Regular click
                        if not click_success:
                            try:
                                element.click()
                                click_success = True
                            except Exception as e:
                                logger.debug(f"Regular click failed: {e}")
                        
                        # Method 3: ActionChains click
                        if not click_success:
                            try:
                                ActionChains(self.driver).move_to_element(element).click().perform()
                                click_success = True
                            except Exception as e:
                                logger.debug(f"ActionChains click failed: {e}")
                        
                        if click_success:
                            logger.info(f"✓ Successfully clicked location element with selector: {selector}")
                            return True
                        else:
                            logger.warning(f"All click methods failed for selector: {selector}")
                            continue
                    
                except (TimeoutException, NoSuchElementException) as e:
                    logger.debug(f"    Selector failed: {selector} - {type(e).__name__}")
                    continue
                except Exception as e:
                    logger.warning(f"    Error with selector {selector}: {e}")
                    continue
        
        logger.error(f"✗ Failed to click location element with any of the provided selectors")
        return False

    def click_element_by_selectors(self, selectors: List[List[str]], timeout: int = 10) -> bool:
        """
        Try to click an element using multiple selector strategies
        
        Args:
            selectors (List[List[str]]): List of selector lists to try
            timeout (int): Timeout in seconds
            
        Returns:
            bool: True if element was clicked successfully, False otherwise
        """
        logger.debug(f"Attempting to click element with {len(selectors)} selector groups...")
        
        for i, selector_list in enumerate(selectors):
            logger.debug(f"Trying selector group {i+1}: {selector_list}")
            for j, selector in enumerate(selector_list):
                logger.debug(f"  Trying selector {j+1}: {selector}")
                try:
                    element = None
                    if selector.startswith("aria/"):
                        # Handle ARIA selectors
                        aria_text = selector.replace("aria/", "")
                        if "[role=" in aria_text:
                            # Extract role and text
                            continue  # Skip complex ARIA selectors for now
                        else:
                            # Simple ARIA text
                            element = self.wait.until(
                                EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{aria_text}')]"))
                            )
                    elif selector.startswith("xpath") or selector.startswith("//"):
                        xpath = selector.replace("xpath", "") if selector.startswith("xpath") else selector
                        # Fix common XPath syntax issues
                        if xpath.startswith("///*"):
                            xpath = xpath.replace("///*", "//*")
                        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    elif selector.startswith("#"):
                        element = self.wait.until(EC.element_to_be_clickable((By.ID, selector[1:])))
                    elif selector.startswith("["):
                        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    elif selector.startswith("text/"):
                        text = selector.replace("text/", "")
                        # Try multiple XPath strategies for text
                        xpath_options = [
                            f"//button[contains(text(), '{text}')]",
                            f"//*[contains(text(), '{text}') and (self::button or self::a)]",
                            f"//*[normalize-space(text())='{text}']"
                        ]
                        for xpath in xpath_options:
                            try:
                                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                                break
                            except (TimeoutException, NoSuchElementException):
                                continue
                    elif ":contains(" in selector:
                        # Handle CSS :contains pseudo-selector (not standard, convert to XPath)
                        if "button:contains('" in selector:
                            text = selector.split("'")[1]
                            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{text}')]")))
                    else:
                        # Try as CSS selector
                        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    
                    if element:
                        # Try multiple click methods - short-circuit on success
                        try:
                            # Method 1: JavaScript click
                            self.driver.execute_script("arguments[0].click();", element)
                            
                            # Check if URL changed
                            current_url = self.driver.current_url
                            if 'postad' in current_url or 'category' in current_url:
                                logger.info(f"✓ Successfully clicked element with selector: {selector} (JS click)")
                                return True
                            
                            # Method 2: Regular click if JS click didn't work
                            element.click()
                            
                            # Check URL again
                            current_url = self.driver.current_url
                            if 'postad' in current_url or 'category' in current_url:
                                logger.info(f"✓ Successfully clicked element with selector: {selector} (regular click)")
                                return True
                                
                            # Method 3: ActionChains click
                            ActionChains(self.driver).move_to_element(element).click().perform()
                            
                            # Final URL check
                            current_url = self.driver.current_url
                            if 'postad' in current_url or 'category' in current_url:
                                logger.info(f"✓ Successfully clicked element with selector: {selector} (ActionChains click)")
                                return True
                            else:
                                logger.warning(f"Clicked element but URL didn't change as expected. Current URL: {current_url}")
                                # Still return True as the click succeeded, URL change might be delayed
                                return True
                                
                        except Exception as click_error:
                            logger.warning(f"Click failed for {selector}: {click_error}")
                            continue
                    
                except (TimeoutException, NoSuchElementException) as e:
                    logger.debug(f"    Selector failed: {selector} - {type(e).__name__}")
                    continue
                except Exception as e:
                    logger.warning(f"    Error with selector {selector}: {e}")
                    continue
        
        logger.error(f"✗ Failed to click element with any of the provided selectors")
        
        # Additional debugging: show what elements are available
        try:
            # Try to find any clickable elements on the page
            clickable_elements = self.driver.find_elements(By.XPATH, "//button | //a | //input[@type='submit'] | //*[@onclick]")
            logger.info(f"Found {len(clickable_elements)} clickable elements on page")
            if clickable_elements:
                logger.info("Sample clickable elements:")
                for i, elem in enumerate(clickable_elements[:5]):
                    try:
                        tag = elem.tag_name
                        text = elem.text[:50] if elem.text else "(no text)"
                        classes = elem.get_attribute("class") or "(no class)"
                        logger.info(f"  {i+1}. <{tag}> text='{text}' class='{classes}'")
                    except:
                        continue
        except Exception as e:
            logger.debug(f"Error listing clickable elements: {e}")
        
        return False
    
    def set_input_value(self, selectors: List[List[str]], value: str, timeout: int = 10) -> bool:
        """
        Set value for an input element using multiple selector strategies
        
        Args:
            selectors (List[List[str]]): List of selector lists to try
            value (str): Value to set
            timeout (int): Timeout in seconds
            
        Returns:
            bool: True if value was set successfully, False otherwise
        """
        for selector_list in selectors:
            for selector in selector_list:
                try:
                    if selector.startswith("aria/"):
                        aria_text = selector.replace("aria/", "")
                        element = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, f"//*[@aria-label='{aria_text}' or @placeholder='{aria_text}']"))
                        )
                    elif selector.startswith("xpath"):
                        xpath = selector.replace("xpath", "")
                        element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    elif selector.startswith("#"):
                        element = self.wait.until(EC.presence_of_element_located((By.ID, selector[1:])))
                    elif selector.startswith("["):
                        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    else:
                        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    
                    # Check if this is a file input
                    if element.get_attribute("type") == "file":
                        # Handle file input specially
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                        
                        try:
                            # Method 1: Direct send_keys for file input
                            element.send_keys(value)
                            logger.info(f"Successfully set file path '{value}' for element with selector: {selector}")
                            return True
                        except Exception as e1:
                            logger.debug(f"Direct send_keys failed: {e1}")
                            
                            try:
                                # Method 2: JavaScript for file input
                                self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
                                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", element)
                                logger.info(f"Successfully set file path via JavaScript '{value}' for element with selector: {selector}")
                                return True
                            except Exception as e2:
                                logger.warning(f"All file input methods failed: {e2}")
                                continue
                    else:
                        # Use human-like typing for regular inputs
                        self.human_type(element, value)
                        logger.info(f"Successfully set value '{value}' for element with selector: {selector}")
                        return True
                    
                except (TimeoutException, NoSuchElementException):
                    continue
                except Exception as e:
                    logger.warning(f"Error with selector {selector}: {e}")
                    continue
        
        logger.error(f"Failed to set value for element with any of the provided selectors")
        return False
    
    def check_session_health(self) -> bool:
        """Check if the browser session is still healthy"""
        try:
            # Try to get current URL to check session
            current_url = self.driver.current_url
            return True
        except Exception as e:
            logger.warning(f"Session health check failed: {e}")
            return False
    
    def recover_session(self) -> bool:
        """Attempt to recover from session issues"""
        try:
            logger.info("Attempting to recover session...")
            # Try to navigate to a simple page
            self.driver.get("https://www.gumtree.com")
            
            # Wait for page to load instead of fixed sleep
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                logger.warning("Page didn't load during recovery, continuing anyway")
            
            return True
        except Exception as e:
            logger.error(f"Session recovery failed: {e}")
            return False
    
    def list_item(self, listing_data: Dict[str, Any]) -> bool:
        """
        List an item on Gumtree using the provided listing data
        
        Args:
            listing_data (Dict[str, Any]): Dictionary containing listing information
            
        Returns:
            bool: True if listing was successful, False otherwise
        """
        try:
            logger.info("Starting item listing process...")
            logger.info(f"Listing data received: {listing_data}")
            
            # Check session health before starting
            if not self.check_session_health():
                logger.warning("Session not healthy, attempting recovery...")
                if not self.recover_session():
                    logger.error("Failed to recover session")
                    return False
            
            # Make sure we're on the homepage and logged in
            self.navigate_to_gumtree()
            
            # Double-check login status before proceeding
            if not self.is_logged_in():
                logger.error("Not logged in. Cannot proceed with listing.")
                return False
            
            # Step 1: Navigate to category selection page (no direct URL navigation)
            logger.info("Navigating to category selection page...")
            # We'll use the standard category selection flow instead of direct URLs
            
            logger.info("Confirmed: User is logged in. Proceeding with listing...")
            
            # Step 2: Click "Post an ad" button
            logger.info("Step 1: Clicking 'Post an ad' button...")
            
            # First, try to close any popups or overlays that might be blocking
            try:
                # Look for common popup/overlay close buttons - batch operation
                close_selectors = [
                    "[data-testid='close-button']",
                    "[data-testid='modal-close']",
                    ".dialog-close",
                    ".modal-close",
                    "button[aria-label='Close']",
                    "[class*='close']",
                    "[aria-label*='close']"
                ]
                
                # Find all close elements at once and act on visible ones
                all_close_elements = []
                for close_selector in close_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, close_selector)
                        all_close_elements.extend(elements)
                    except:
                        continue
                
                # Close visible popups
                for close_element in all_close_elements:
                    try:
                        if close_element.is_displayed():
                            close_element.click()
                            logger.info(f"Closed popup/overlay")
                            break
                    except:
                        continue
                        
                # Also try pressing Escape key to close any modals
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                
            except Exception as e:
                logger.debug(f"Error trying to close popups: {e}")
            
            post_ad_selectors = [[
                "button:contains('Post an ad')",
                "//button[contains(text(), 'Post an ad')]",
                "[data-testid='post-ad-button']",
                "button[class*='nav-bar'][text*='Post']",
                "text/Post an ad"
            ]]
            if not self.click_element_by_selectors(post_ad_selectors):
                logger.error("Failed to click 'Post an ad' button")
                return False
            
            # Wait for category page to load instead of fixed sleep
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#post-ad_title-suggestion"))
                )
            except TimeoutException:
                logger.warning("Category page didn't load as expected, continuing anyway")
            
            # Check if we're on the category page
            current_url = self.driver.current_url
            logger.info(f"Current URL after clicking Post an ad: {current_url}")
            
            # Step 3: Enter category search
            logger.info("Step 2: Entering category search...")
            category_selectors = [[
                "#post-ad_title-suggestion",
                "xpath///*[@id='post-ad_title-suggestion']"
            ]]
            
            # Use the actual category from the UI instead of hardcoded value
            category = listing_data.get('category', 'Artificial Grass')
            logger.info(f"Using category from UI: {category}")
            
            if not self.set_input_value(category_selectors, category):
                logger.error(f"Failed to enter category search: {category}")
                return False
            
            # Wait for category suggestions to appear
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='category-display-name']"))
                )
            except TimeoutException:
                logger.warning("Category suggestions didn't appear, continuing anyway")
            
            # Step 4: Select suggested category
            logger.info("Step 3: Selecting first category result...")
            category_btn_selectors = [[
                "button:nth-of-type(1) [data-testid='category-display-name']",
                "button[data-testid='category-display-name']:first-of-type",
                "button:first-of-type [data-testid='category-display-name']",
                "button[data-testid='category-display-name']",
                ".category-suggestion:first-child button",
                ".suggestion-item:first-child button",
                "xpath///*[@data-testid='category-display-name']",
                "[data-testid='category-display-name']"
            ]]
            if not self.click_element_by_selectors(category_btn_selectors):
                logger.error("Failed to select category")
                return False
            
            # Wait for next step to load instead of fixed sleep
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Select your location') or contains(text(), 'Select location')]"))
                )
            except TimeoutException:
                logger.warning("Next step didn't load as expected, continuing anyway")
            
            # Check URL again
            current_url = self.driver.current_url
            logger.info(f"Current URL after selecting category: {current_url}")
            
            # Step 5: Select location from UI data - simplified and robust
            logger.info("Setting up location...")
            
            # Click location button - simple approach
            location_btn_selectors = [
                ["button", "text/Select your location"],
                ["text/Select your location"],
                ["text/Select location"]
            ]
            
            location_clicked = False
            for selectors in location_btn_selectors:
                if self.click_element_by_selectors([selectors]):
                    logger.info(f"Successfully clicked location button")
                    location_clicked = True
                    break
            
            if not location_clicked:
                logger.error("Could not find or click location selection button")
                return False
            
            # Wait for location modal to load instead of fixed sleep
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'England') or contains(text(), 'Wales')]"))
                )
            except TimeoutException:
                logger.warning("Location modal didn't load as expected, continuing anyway")
            
            # Get location data from listing_data
            location = listing_data.get('location', '')
            sub_location = listing_data.get('sub_location', '')
            
            logger.info(f"Using location: {location}, sub-location: {sub_location}")
            
            # Parse location to get county and country
            if ',' in location:
                county, country = location.split(',', 1)
                county = county.strip()
                country = country.strip()
            else:
                county = location
                country = "England"  # Default
            
            # Select country (England/Wales) - simple approach
            if country.lower() == "england":
                country_selector = ["text/England"]
            elif country.lower() == "wales":
                country_selector = ["text/Wales"]
            else:
                country_selector = ["text/England"]  # Default
            
            if not self.click_element_by_selectors([country_selector]):
                logger.error(f"Could not select country: {country}")
                return False
            
            logger.info(f"Successfully selected country: {country}")
            
            # Wait for counties to load instead of fixed sleep
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{county}')]"))
                )
            except TimeoutException:
                logger.warning("Counties didn't load as expected, continuing anyway")
            
            # Select county - simple approach
            county_selector = [f"text/{county}"]
            if not self.click_element_by_selectors([county_selector]):
                logger.error(f"Could not select county: {county}")
                return False
            
            logger.info(f"Successfully selected county: {county}")
            
            # Wait for sub-locations to load instead of fixed sleep
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{sub_location}')]"))
                )
            except TimeoutException:
                logger.warning("Sub-locations didn't load as expected, continuing anyway")
            
            # Select sub-location if provided - simple approach
            if sub_location:
                sub_location_selector = [f"text/{sub_location}"]
                if self.click_element_by_selectors([sub_location_selector]):
                    logger.info(f"Successfully selected sub-location: {sub_location}")
                    
                    # Wait for third location options to load instead of fixed sleep
                    try:
                        self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "li, div, button"))
                        )
                    except TimeoutException:
                        logger.warning("Third location options didn't load as expected")
                    
                    # Check for third location (random selection) - simplified
                    try:
                        # Look for clickable location elements
                        third_location_elements = self.driver.find_elements("css selector", "li, div, button")
                        third_location_options = []
                        
                        for element in third_location_elements:
                            try:
                                text = element.text.strip()
                                if (text and len(text) > 2 and 
                                    text not in [sub_location, county, country] and
                                    any(char.isalpha() for char in text) and 
                                    text.lower() not in ['continue', 'next', 'back', 'cancel', 'select']):
                                    third_location_options.append(text)
                            except:
                                continue
                        
                        if third_location_options:
                            import random
                            random_third_location = random.choice(third_location_options)
                            logger.info(f"Found third location options: {third_location_options}")
                            logger.info(f"Randomly selecting third location: {random_third_location}")
                            
                            # Click the random third location
                            third_location_selector = [f"text/{random_third_location}"]
                            if self.click_element_by_selectors([third_location_selector]):
                                logger.info(f"Successfully selected third location: {random_third_location}")
                            else:
                                logger.warning(f"Could not select third location: {random_third_location}")
                        else:
                            logger.info("No third location options found")
                            
                    except Exception as e:
                        logger.warning(f"Error checking for third location: {e}")
                else:
                    logger.warning(f"Could not select sub-location: {sub_location} - continuing anyway")
            
            # Click continue button - target the specific locationIdBtn element
            logger.info("Clicking continue button...")
            continue_clicked = False
            
            # Target the specific continue button with id="locationIdBtn"
            continue_selectors = [
                ["#locationIdBtn"],  # Primary selector - exact ID
                ["a[id='locationIdBtn']"],  # Alternative ID selector
                ["a[data-q='location-browser-continue-btn']"],  # Data attribute
                ["a.btn-primary", "text/Continue"],  # Class + text
                ["a", "text/Continue"],  # Fallback to any link with Continue text
                ["text/Continue"]  # Final fallback
            ]
            
            for selectors in continue_selectors:
                if self.click_element_by_selectors([selectors]):
                    logger.info(f"Successfully clicked continue button with selector: {selectors}")
                    continue_clicked = True
                    break
            
            if not continue_clicked:
                logger.error("Could not find or click continue button")
                return False
            
            # Wait for next step to load instead of fixed sleep
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='ad-title-input'], #price"))
                )
            except TimeoutException:
                logger.warning("Next step didn't load as expected, continuing anyway")
            
            # Step 6: Upload images (if provided) - using robust upload method
            listing_id = listing_data.get('listing_id', '')
            if listing_id:
                backup_path = os.path.join('backup_listings', listing_id)
                if os.path.exists(backup_path):
                    # Find all image files in the backup folder
                    image_files = []
                    for file in os.listdir(backup_path):
                        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                            image_files.append(os.path.join(backup_path, file))
                    
                    if image_files:
                        logger.info(f"Found {len(image_files)} images to upload")
                        for i, image_path in enumerate(image_files):
                            logger.info(f"Uploading image {i+1}: {os.path.basename(image_path)}")
                            if not self.upload_image(image_path):
                                logger.warning(f"Failed to upload image: {os.path.basename(image_path)}")
                    else:
                        logger.info("No images found in backup folder")
                else:
                    logger.warning(f"Backup folder not found: {backup_path}")
            elif listing_data.get('image_path'):
                # Fallback for direct image path
                logger.info("Uploading single image...")
                if not self.upload_image(listing_data['image_path']):
                    logger.warning("Failed to upload image")
            
            # Check session health before critical operations
            if not self.check_session_health():
                logger.warning("Session lost during listing, attempting recovery...")
                if not self.recover_session():
                    logger.error("Failed to recover session during listing")
                    return False
            
            # Step 7: Set title
            logger.info("Setting title...")
            title_selectors = [[
                "[data-testid='ad-title-input']"
            ]]
            if not self.set_input_value(title_selectors, listing_data.get('title', 'Default Title')):
                return False
            
            # Step 8: Set description
            logger.info("Setting description...")
            desc_selectors = [[
                "[data-testid='description-textarea']"
            ]]
            if not self.set_input_value(desc_selectors, listing_data.get('description', 'Default Description')):
                return False
            
            # Step 9: Set price
            logger.info("Setting price...")
            price_selectors = [[
                "#price"
            ]]
            if not self.set_input_value(price_selectors, str(listing_data.get('price', '1'))):
                return False
            
            # Step 10: Select condition
            logger.info("Setting condition...")
            condition_btn_selectors = [[
                "text/Select your Condition"
            ]]
            if not self.click_element_by_selectors(condition_btn_selectors):
                return False
            
            # Wait for condition options to appear
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'New') or contains(text(), 'Used') or contains(text(), 'Refurbished')]"))
                )
            except TimeoutException:
                logger.warning("Condition options didn't appear, continuing anyway")
            
            # Select condition from UI data (default to "New")
            condition = listing_data.get('condition', 'New')
            logger.info(f"Selecting condition: {condition}")
            
            condition_selectors = [[
                f"text/{condition}"
            ]]
            if not self.click_element_by_selectors(condition_selectors):
                logger.warning(f"Could not select condition: {condition}, trying 'New'")
                # Fallback to "New"
                new_condition_selectors = [[
                    "text/New"
                ]]
                if not self.click_element_by_selectors(new_condition_selectors):
                    return False
            
            # Wait for save button to appear
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Save')]"))
                )
            except TimeoutException:
                logger.warning("Save button didn't appear, continuing anyway")
            
            # Save condition
            save_selectors = [[
                "text/Save"
            ]]
            if not self.click_element_by_selectors(save_selectors):
                return False
            
            # Step 11: Select phone contact option
            logger.info("Setting contact preferences...")
            phone_selectors = [[
                "text/Phone:"
            ]]
            if not self.click_element_by_selectors(phone_selectors):
                logger.warning("Failed to select phone option")
            
            # Step 12: Submit the ad
            logger.info("Submitting the ad...")
            submit_selectors = [[
                "#submit-button-2",
                "text/Post my Ad"
            ]]
            if not self.click_element_by_selectors(submit_selectors):
                return False
            
            logger.info("Item listing completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error during listing process: {e}")
            return False
    
    def run(self, listing_data: Dict[str, Any]) -> bool:
        """
        Main method to run the bot
        
        Args:
            listing_data (Dict[str, Any]): Dictionary containing listing information
            
        Returns:
            bool: True if process completed successfully, False otherwise
        """
        try:
            # Setup WebDriver
            self.setup_driver()
            
            # Ensure we're logged in (handles both cookie loading and manual login)
            if not self.ensure_logged_in():
                logger.error("Failed to establish login")
                return False
            
            # Proceed with listing
            success = self.list_item(listing_data)
            
            return success
            
        except Exception as e:
            logger.error(f"Error in main run method: {e}")
            return False
        finally:
            if self.driver:
                logger.info("Closing browser...")
                self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()