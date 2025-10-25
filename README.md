# Screenshot Organizer

Automatically organize your macOS screenshots into date-based folders with customizable naming and cleanup options.

A lightweight macOS automation tool that automatically organizes screenshots into date-based folders with customizable naming conventions. Features easy setup, persistent background operation via LaunchAgent, configurable storage locations, and optional auto-cleanup. Designed for non-technical users with simple installation while maintaining full source transparency.

> **⚠️ IMPORTANT:** You CANNOT double-click to install. macOS will block it for security.
>
> **Quick Start:** Download → Right-click `install.command` → Select "Open" → Follow prompts

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

## Installation

### ⚠️ Why You Can't Double-Click

macOS Gatekeeper blocks unknown `.command` files from running to protect your computer. **Double-clicking will NOT work.** You must right-click to open it the first time. This is normal macOS security behavior, not a bug.

### Step 1: Download
Download this folder to your Mac (e.g., Downloads folder)

### Step 2: Install (Choose One Method)

#### Option A: Right-Click to Install (Recommended)

**DO NOT double-click** - it will be blocked by macOS security.

1. **Right-click** (or Control + click) on `install.command`
2. Select **"Open"** from the menu
3. Click **"Open"** in the security dialog
4. **Follow the prompts** in Terminal to configure your preferences
5. **Done!** Take a screenshot (Cmd+Shift+3 or Cmd+Shift+4) to see it work

> **Note:** After the installer runs once, it removes the security blocks from all files. You may be able to double-click the other `.command` files normally after that.

#### Option B: Terminal Command (Alternative)

Open Terminal and paste:
```bash
cd ~/Downloads/screenshot-organizer && bash install.command
```

> Replace `~/Downloads/screenshot-organizer` with your actual folder path.

---

**The installer automatically:**
- ✅ Removes macOS security blocks from all files
- ✅ Installs required dependencies (watchdog)
- ✅ Guides you through configuration
- ✅ Sets up background service to run automatically

## Usage

### After Installation

Once installed, the organizer runs automatically in the background. Just take screenshots normally (Cmd+Shift+3 or Cmd+Shift+4) and they'll be organized automatically.

### Managing the Service

- **Reconfigure settings:** Right-click (or double-click) `StartScreenshotOrganizer.command`
- **Stop the service:** Right-click (or double-click) `StopScreenshotOrganizer.command`

> If you get security warnings on these files, use right-click → Open (same as installation)

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

### "Cannot be opened because it is from an unidentified developer"

**This is completely normal.** macOS Gatekeeper blocks all unknown `.command` files to protect your system. This script is safe (all code is visible and open source), but macOS doesn't know that without an Apple Developer signature ($99/year).

**Solution - Right-click to bypass:**
1. **Right-click** (or Control+click) on `install.command`
2. Select **"Open"** from the menu
3. Click **"Open"** again in the security dialog

This is a one-time step. The installer removes security attributes from all project files.

**Alternative - Terminal command:**
```bash
cd ~/Downloads/screenshot-organizer && bash install.command
```

### Permission Errors

If you see "could not be executed because you do not have appropriate access privileges," try right-clicking and selecting "Open" instead of double-clicking.

If that doesn't work, run in Terminal:
```bash
chmod +x install.command StartScreenshotOrganizer.command StopScreenshotOrganizer.command
```
Then right-click to open.

### Python Not Found

Install Python 3 from [python.org](https://python.org) (though most modern Macs include it).

### Screenshots Not Being Organized

1. Make sure the background service is running
2. Check that you're taking screenshots (Cmd+Shift+3 or Cmd+Shift+4)
3. Verify the service is installed: look for organized folders after taking a screenshot

### Still Having Issues?

Check the logs for error messages:
```bash
tail -f ~/Library/Logs/screenshot-organizer.log
tail -f ~/Library/Logs/screenshot-organizer-error.log
```

## Files Overview

- `install.command` - Easy installer that handles all setup (START HERE)
- `StartScreenshotOrganizer.command` - Restart or reconfigure the organizer
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

1. Stop the background service:
   - Double-click `StopScreenshotOrganizer.command`, OR
   - Run in Terminal: `python3 main.py --uninstall`
2. Delete the screenshot-organizer folder

That's it! Your screenshots will return to the default Desktop location.

---

**Note:** This tool only works with macOS screenshots taken via keyboard shortcuts (Cmd+Shift+3, Cmd+Shift+4, etc.). Screenshots from other applications are not automatically organized.
