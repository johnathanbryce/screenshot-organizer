# Screenshot Organizer

Automatically organize your macOS screenshots into date-based folders with customizable naming and cleanup options.

A lightweight macOS automation tool that automatically organizes screenshots into date-based folders with customizable naming conventions. Features easy setup, persistent background operation via LaunchAgent, configurable storage locations, and optional auto-cleanup. Designed for non-technical users with simple installation while maintaining full source transparency.

> **Quick Start:** Download this folder → Right-click `install.command` → Select "Open" → Follow prompts

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

### Step 1: Download
Download this folder to your Mac (e.g., Downloads folder)

### Step 2: Install (Choose One Method)

#### Method A: Right-Click to Install (Recommended - Works for Everyone)

**IMPORTANT:** macOS security will block a normal double-click. Here's how to bypass it (one-time only):

1. **Right-click** (or hold Control and click) on `install.command`
2. Select **"Open"** from the menu
3. Click **"Open"** in the security dialog that appears
4. **Follow the prompts** in the Terminal window to configure your preferences
5. **Done!** Take a screenshot (Cmd+Shift+3 or Cmd+Shift+4) to see it in action

> After this first time, you can double-click `StartScreenshotOrganizer.command` normally - no more right-clicking needed!

#### Method B: Terminal One-Liner (For Advanced Users)

Open Terminal and paste this command:
```bash
cd ~/Downloads/screenshot-organizer && bash install.command
```

> Replace `~/Downloads/screenshot-organizer` with the actual path if you saved it elsewhere.

---

**That's it!** The installer automatically:
- ✅ Fixes macOS security permissions for all files
- ✅ Installs required dependencies (watchdog)
- ✅ Guides you through configuration
- ✅ Sets up the background service to run automatically

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

### "Cannot be opened because it is from an unidentified developer"

This is macOS Gatekeeper protecting your system. **Solution:**

**Right-click to bypass (One-time fix):**
1. **Right-click** (or Control+click) on `install.command`
2. Select **"Open"** from the menu
3. Click **"Open"** in the security dialog

This only needs to be done ONCE. After running the installer, all other files will work with normal double-clicks.

**Alternative - Terminal command:**
```bash
cd ~/Downloads/screenshot-organizer && bash install.command
```

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
