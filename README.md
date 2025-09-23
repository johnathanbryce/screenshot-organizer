# Screenshot Organizer

Automatically organize your macOS screenshots into date-based folders with customizable naming and cleanup options.

A lightweight macOS automation tool that automatically organizes screenshots into date-based folders with customizable naming conventions. Features one-click setup, persistent background operation via LaunchAgent, configurable storage locations, and optional auto-cleanup. Designed for non-technical users with simple .command file installation while maintaining full source transparency.

## What It Does

- **Auto-organizes screenshots** into folders by date (e.g., `Screenshots/23 September 2025/`)
- **Custom naming** with timestamps (e.g., `01 - 03:45 PM.png`)
- **Configurable storage** location (Desktop or Home directory)
- **Auto-cleanup** old screenshots after specified days
- **Runs in background** - works even when you close Terminal

## Requirements

- **macOS** (tested on macOS 10.14+)
- **Python 3** (comes pre-installed on modern Macs)
- **Internet connection** (for automatic dependency installation)

## Quick Start

1. **Download** this folder to your Mac
2. **Double-click** `StartScreenshotOrganizer.command`
3. **Follow the setup prompts** to configure your preferences
4. **Choose "yes"** when asked to install as background service
5. **Done!** Take a screenshot to see it in action

## Usage

### First Time Setup

- Double-click `StartScreenshotOrganizer.command`
- Configure your folder name, location, and cleanup preferences
- The script will automatically install required dependencies
- Choose to install as background service for continuous operation

### Managing the Service

- **Stop:** Double-click `StopScreenshotOrganizer.command`
- **Reconfigure:** Run the start command again

## Configuration Options

- **Folder name:** Customize your main screenshots folder name
- **Location:** Save to Desktop or Home directory
- **Auto-naming:** Enable numbered timestamps for screenshots
- **Auto-cleanup:** Automatically delete screenshots after X days
- **Custom timing:** Set how many days to keep screenshots (0-365)

## How It Works

The script monitors your Desktop for new screenshots and automatically:

1. Creates organized date-based folders
2. Renames files with clean timestamps
3. Moves screenshots to the appropriate folder
4. Optionally cleans up old screenshots

## Troubleshooting

### Permission Errors

If you see "could not be executed because you do not have appropriate access privileges":

```bash
chmod +x StartScreenshotOrganizer.command
chmod +x StopScreenshotOrganizer.command
```

### Python Not Found

Install Python 3 from [python.org](https://python.org) (though most modern Macs include it).

### Screenshots Not Being Organized

1. Make sure the background service is running
2. Check that you're taking screenshots (Cmd+Shift+3 or Cmd+Shift+4)
3. Verify the service is installed: look for organized folders after taking a screenshot

## Files Overview

- `StartScreenshotOrganizer.command` - Setup and start the organizer
- `StopScreenshotOrganizer.command` - Stop the background service
- `main.py` - Core application logic
- `config/` - Configuration files and user settings
- `screenshot_organizer.py` - Screenshot detection and organization
- `cleanup_screenshots.py` - Automatic cleanup functionality

## Logs

Service logs are stored at:

- `~/Library/Logs/screenshot-organizer.log`
- `~/Library/Logs/screenshot-organizer-error.log`

## Uninstalling

Run `StopScreenshotOrganizer.command` to stop and remove the background service. Then delete this folder.

---

**Note:** This tool only works with macOS screenshots taken via keyboard shortcuts (Cmd+Shift+3, Cmd+Shift+4, etc.). Screenshots from other applications are not automatically organized.
