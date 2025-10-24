#!/bin/bash

# Screenshot Organizer - Easy Installer
# This script handles all setup including macOS security permissions

echo "🖼️  Screenshot Organizer - Easy Installer"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Working directory: $SCRIPT_DIR"
echo ""

# Remove quarantine attributes from all files (fixes macOS Gatekeeper issues)
echo "🔓 Removing macOS quarantine attributes..."
xattr -d com.apple.quarantine * 2>/dev/null
xattr -dr com.apple.quarantine . 2>/dev/null
echo "✅ Security attributes cleared"
echo ""

# Make command files executable
echo "🔧 Setting up executable permissions..."
chmod +x StartScreenshotOrganizer.command 2>/dev/null
chmod +x StopScreenshotOrganizer.command 2>/dev/null
chmod +x install.sh 2>/dev/null
echo "✅ Permissions configured"
echo ""

# Check if Python 3 is available
echo "🐍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo ""
    echo "Please install Python 3 from https://python.org"
    echo "Then run this installer again."
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"
echo ""

# Check and install watchdog if needed
echo "📦 Checking required packages..."
python3 -c "import watchdog" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required package (watchdog)..."
    echo "   This may take a moment..."
    python3 -m pip install --user watchdog --quiet
    if [ $? -ne 0 ]; then
        echo ""
        echo "⚠️  Automatic installation failed. Trying alternative method..."
        pip3 install --user watchdog
        if [ $? -ne 0 ]; then
            echo ""
            echo "❌ Failed to install watchdog package."
            echo "Please try manually running: pip3 install watchdog"
            echo ""
            echo "Press any key to exit..."
            read -n 1
            exit 1
        fi
    fi
    echo "✅ Successfully installed watchdog"
else
    echo "✅ All required packages installed"
fi
echo ""

# Run configuration
echo "⚙️  Time to configure your screenshot organizer!"
echo ""
python3 main.py --config

# Check if configuration was completed
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Configuration was cancelled or failed."
    echo "Run this installer again when you're ready."
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Ask about background service installation
echo ""
echo "🚀 Would you like to install this as a background service?"
echo "   This will make it run automatically (even after restarts)."
echo ""
read -p "Install background service? (y/n) [y]: " install_choice

if [[ "$install_choice" =~ ^[Yy]$ ]] || [[ "$install_choice" == "" ]]; then
    echo ""
    echo "📦 Installing background service..."
    python3 main.py --install
    echo ""
    echo "✅ INSTALLATION COMPLETE!"
    echo ""
    echo "Your Screenshot Organizer is now running in the background."
    echo "It will automatically start when you log in to your Mac."
    echo ""
    echo "Take a screenshot (Cmd+Shift+3 or Cmd+Shift+4) to see it in action!"
else
    echo ""
    echo "✅ INSTALLATION COMPLETE!"
    echo ""
    echo "Configuration saved! You can now:"
    echo "  • Double-click 'StartScreenshotOrganizer.command' to start organizing"
    echo "  • Run this installer again to enable background service"
fi

echo ""
echo "📝 Useful commands:"
echo "  • Stop service: Double-click 'StopScreenshotOrganizer.command'"
echo "  • View logs: ~/Library/Logs/screenshot-organizer.log"
echo "  • Reconfigure: Run this installer again"
echo ""
echo "Press any key to close..."
read -n 1
