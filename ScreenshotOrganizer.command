# Screenshot Organizer Launcher
# Double-click this file to set up and start the Screenshot Organizer

echo "🖼️  Screenshot Organizer Setup"
echo "================================"
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

# Check if this is first run or reconfiguration
if [ "$1" = "--config" ]; then
    echo "🔧 Reconfiguring Screenshot Organizer..."
    python3 main.py --config-only
    echo ""
    echo "Press any key to close..."
    read -n 1
    exit 0
fi

# Run the main setup
echo "🚀 Starting Screenshot Organizer setup..."
echo ""
python3 main.py --setup

echo ""
echo "✅ Setup complete!"
echo ""
echo "Your Screenshot Organizer is now running in the background."
echo "It will automatically start when you log in to your Mac."
echo ""
echo "📋 Useful commands:"
echo "   • To reconfigure: Double-click this file and it will detect existing setup"
echo "   • To check status: python3 main.py --status"
echo "   • To stop service: python3 main.py --stop"
echo ""
echo "🗂️  Screenshots will be organized in your configured folder."
echo ""
echo "Press any key to close this window..."
read -n 1