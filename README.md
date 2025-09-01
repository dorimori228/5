# Gumtree Auto Lister Bot

A comprehensive automation system for creating and managing Gumtree listings with a web-based interface and intelligent bot capabilities.

## 🚀 Features

### 🤖 Advanced Bot Capabilities
- **Human-like Typing**: Realistic typing behavior with random delays and occasional typos
- **Anti-Detection**: Advanced measures to avoid automation detection
- **Cookie Management**: Automatic login persistence with saved cookies
- **Stealth Mode**: Complete automation hiding with JavaScript injection

### 🌐 Web Interface
- **Modern UI**: Clean, responsive web interface built with Flask and Bootstrap
- **Listing Creation**: Easy-to-use form for creating new listings
- **Photo Upload**: Support for multiple image uploads
- **Location Selection**: Dynamic location selection for England and Wales
- **Batch Processing**: Process multiple listings automatically

### 📁 Data Management
- **Backup System**: Automatic backup of all listings and photos
- **Queue Management**: Track listing status and processing
- **Real-time Updates**: Live status updates during processing

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser
- ChromeDriver (automatically managed by Selenium)

### Setup
1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web interface**:
   ```bash
   python app.py
   ```
   Or use the batch file:
   ```bash
   start_web_ui.bat
   ```

4. **Access the web UI**:
   Open your browser and go to: `http://localhost:5000`

## 📖 Usage

### Creating Listings
1. **Access the Web UI**: Go to `http://localhost:5000`
2. **Create New Listing**: Click "Create Listing" button
3. **Fill in Details**:
   - Title and description
   - Price and condition (defaults to "New")
   - Location (Country → County → Sub-location)
   - Upload photos (optional)
4. **Save**: Click "Create Listing" to save

### Processing Listings
1. **Manage Listings**: Go to "Manage Listings" page
2. **Individual Processing**: Click "Process" on any pending listing
3. **Batch Processing**: Click "Process All Pending" to process all at once
4. **Monitor Progress**: Watch real-time status updates

### Bot Features
- **Automatic Login**: Bot saves cookies for persistent login
- **Human Behavior**: Realistic typing with delays and corrections
- **Anti-Detection**: Advanced measures to avoid detection
- **Location Handling**: Automatic location selection and navigation

## 📁 File Structure

```
gumtree-auto-lister/
├── app.py                          # Flask web application
├── gumtree_bot.py                  # Main bot class with automation
├── requirements.txt                # Python dependencies
├── start_web_ui.bat               # Windows batch file to start UI
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Home page
│   ├── create_listing.html        # Listing creation form
│   └── manage_listings.html       # Listing management
├── static/uploads/                # Photo uploads
├── backup_listings/               # Listing backups
│   ├── listing_queue.json         # Processing queue
│   └── listing_*/                 # Individual listing folders
├── gumtree england locations.txt  # England location data
├── gumtree wales locations.txt    # Wales location data
└── chrome_user_data/              # Chrome profile data
```

## 🔧 Configuration

### Bot Settings
- **Headless Mode**: Set `headless=True` in `GumtreeBot()` for background operation
- **Browser Profile**: Uses persistent Chrome profile for cookie storage
- **Anti-Detection**: Automatically applied on every page load

### Web UI Settings
- **Port**: Default port 5000 (change in `app.py`)
- **Upload Folder**: `static/uploads/` for photos
- **Backup Folder**: `backup_listings/` for listing data

## 🎯 Workflow

### For 600 Listings Goal
1. **Create Listings**: Use the web UI to create all 600 listings
2. **Organize**: Each listing is automatically backed up with photos
3. **Process**: Use batch processing to automatically post all listings
4. **Monitor**: Track progress through the web interface
5. **Manage**: Retry failed listings or create new ones as needed

### Recommended Process
1. **Start Small**: Test with 5-10 listings first
2. **Verify Login**: Ensure bot can log in automatically
3. **Check Locations**: Verify location selection works correctly
4. **Scale Up**: Gradually increase to larger batches
5. **Monitor**: Watch for any issues or failed listings

## 🛡️ Anti-Detection Features

### Chrome Arguments
- Disabled automation indicators
- Custom user agent
- Disabled logging and debugging
- Removed automation switches

### JavaScript Injection
- Removed `navigator.webdriver` property
- Mocked browser plugins and languages
- Deleted automation-specific properties
- Overridden toString methods

### Human Behavior
- Random typing delays (50-150ms per character)
- Occasional thinking pauses
- Typo simulation with corrections
- Realistic mouse movements

## 📊 Status Tracking

### Listing States
- **Pending**: Created but not processed
- **Processing**: Currently being posted
- **Completed**: Successfully posted
- **Failed**: Error during posting

### Monitoring
- Real-time status updates
- Processing timestamps
- Error logging and reporting
- Success/failure statistics

## 🔍 Troubleshooting

### Common Issues
1. **Chrome Detection**: Ensure anti-detection measures are working
2. **Login Issues**: Check cookie persistence and login status
3. **Location Errors**: Verify location data files are present
4. **Photo Upload**: Check file permissions and formats

### Debug Mode
- Set `headless=False` to see browser actions
- Check browser console for JavaScript errors
- Review Flask logs for server issues
- Monitor backup folder for data integrity

## 📝 Notes

- **Rate Limiting**: Built-in delays between listings (30-60 seconds)
- **Error Handling**: Comprehensive error catching and reporting
- **Data Backup**: All listings and photos are automatically backed up
- **Scalability**: Designed to handle hundreds of listings efficiently

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please ensure you comply with Gumtree's terms of service and use responsibly. The developers are not responsible for any misuse of this software.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure all dependencies are installed
4. Verify Chrome and ChromeDriver compatibility

---

**Happy Listing! 🎉**