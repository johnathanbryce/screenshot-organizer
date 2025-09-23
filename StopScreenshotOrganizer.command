echo "🛑 Stopping Screenshot Organizer..."
echo "==================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Stop the background service
python3 main.py --uninstall

echo ""
echo "Press any key to close..."
read -n 1