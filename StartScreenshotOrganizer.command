# Screenshot Organizer Setup & Install
echo "🖼️ Screenshot Organizer Setup"
echo "============================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "Please install Python 3 from https://python.org"
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Check and install watchdog if needed
echo "🔍 Checking required packages..."
python3 -c "import watchdog" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required package (watchdog)..."
    python3 -m pip install watchdog
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install watchdog. You may need to run:"
        echo "pip3 install watchdog"
        echo ""
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
    echo "✅ Successfully installed watchdog"
fi
echo ""

# Step 1: Run config ONLY (don't start the service)
python3 main.py --config

echo ""
echo "📦 Would you like to install this as a background service?"
echo "This will make it run automatically even when you close this window."
echo ""
read -p "Install background service? (y/n) [y]: " install_choice

if [[ "$install_choice" =~ ^[Yy]$ ]] || [[ "$install_choice" == "" ]]; then
    echo ""
    echo "Installing background service..."
    python3 main.py --install
    echo ""
    echo "✅ Setup complete! Your Screenshot Organizer is now running in the background."
    echo "It will automatically start when you log in to your Mac."
else
    echo ""
    echo "✅ Configuration saved! Run this script again anytime to start organizing screenshots."
fi

echo ""
echo "Press any key to close..."
read -n 1