

# TODO:
# - task runner
# -  create a script command 'python reset_settings.py' for a user to run initiate get_user_config to allow a user to reset their settings?
# - error handling
# - gracefully stop runner and cleanup the loop instead of force quit via ctrl+c or program shut down (i.e turning off computer)

import asyncio
import sys
from pathlib import Path
from cleanup_screenshots import cleanup_screenshots_task
from screenshot_organizer import detect_screenshots
from config.config_loader import CONFIG


def is_first_run():
    """Check if this is the first time running the script"""
    config_file = Path(__file__).parent / "config" / "config.json"
    return not config_file.exists()


def install_launchagent():
    """Install the LaunchAgent to run the service in background"""
    import os
    import json
    from pathlib import Path
    
    # Get absolute paths
    script_dir = Path(__file__).parent.absolute()
    python_executable = sys.executable
    main_script = script_dir / "main.py"
    
    # Create plist content
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.screenshot-organizer</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_executable}</string>
        <string>{main_script}</string>
        <string>--service</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{Path.home()}/Library/Logs/screenshot-organizer.log</string>
    <key>StandardErrorPath</key>
    <string>{Path.home()}/Library/Logs/screenshot-organizer-error.log</string>
    <key>WorkingDirectory</key>
    <string>{script_dir}</string>
</dict>
</plist>"""

    # Create LaunchAgents directory if it doesn't exist
    launchagents_dir = Path.home() / "Library" / "LaunchAgents"
    launchagents_dir.mkdir(exist_ok=True)
    
    # Write plist file
    plist_file = launchagents_dir / "com.screenshot-organizer.plist"
    plist_file.write_text(plist_content)
    
    # Load the LaunchAgent
    os.system(f'launchctl load "{plist_file}"')
    
    print(f"✅ Background service installed and started")
    print(f"📝 Logs will be written to: {Path.home()}/Library/Logs/screenshot-organizer.log")


def uninstall_launchagent():
    """Remove the LaunchAgent"""
    import os
    from pathlib import Path
    
    plist_file = Path.home() / "Library" / "LaunchAgents" / "com.screenshot-organizer.plist"
    
    if plist_file.exists():
        # Unload the service
        os.system(f'launchctl unload "{plist_file}"')
        # Remove the plist file
        plist_file.unlink()
        print("✅ Screenshot Organizer service stopped and removed")
    else:
        print("❌ Service not found")


def show_status():
    """Show the current status of the service"""
    import subprocess
    from pathlib import Path
    
    plist_file = Path.home() / "Library" / "LaunchAgents" / "com.screenshot-organizer.plist"
    
    if not plist_file.exists():
        print("❌ Screenshot Organizer is not installed")
        return
    
    # Check if service is loaded
    try:
        result = subprocess.run(['launchctl', 'list', 'com.screenshot-organizer'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Screenshot Organizer is running in the background")
            
            # Show current config
            print(f"\n📋 Current Configuration:")
            print(f"   • Main folder: {CONFIG['screenshots_main_directory_name']}")
            print(f"   • Location: {'Desktop' if CONFIG['use_desktop_pathway'] else 'Home directory'}")
            print(f"   • Auto naming: {'Enabled' if CONFIG['use_auto_screenshot_naming'] else 'Disabled'}")
            print(f"   • Auto deletion: {'Enabled' if CONFIG.get('auto_delete_directories', False) else 'Disabled'}")
            if CONFIG.get('auto_delete_directories', False):
                print(f"   • Delete after: {CONFIG.get('delete_after_days', 'N/A')} days")
            
            # Show log location
            log_file = Path.home() / "Library" / "Logs" / "screenshot-organizer.log"
            if log_file.exists():
                print(f"\n📝 Recent log entries:")
                # Show last few lines of log
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        for line in lines[-3:]:  # Show last 3 lines
                            print(f"   {line.strip()}")
                except:
                    print("   (Unable to read log file)")
        else:
            print("⚠️  Screenshot Organizer is installed but not running")
    except FileNotFoundError:
        print("❌ Unable to check service status")


async def main():
    """Main entry point - handles different modes based on arguments"""
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "--setup":
            # First time setup mode
            from config.get_user_config import get_user_config
            
            if is_first_run():
                print("👋 Welcome to Screenshot Organizer!")
                print("Let's configure your screenshot organization settings...\n")
            else:
                print("🔧 Screenshot Organizer is already set up.")
                reconfigure = input("Would you like to reconfigure your settings? (y/n) [n]: ").strip().lower()
                if reconfigure not in ('y', 'yes'):
                    show_status()
                    return
            
            # Run configuration
            get_user_config()
            
            # Install/reinstall the service
            uninstall_launchagent()  # Remove existing if any
            install_launchagent()    # Install fresh
            
            return
            
        elif mode == "--config-only":
            # Just reconfigure, don't reinstall service
            from config.get_user_config import get_user_config
            get_user_config()
            print("✅ Configuration updated")
            return
            
        elif mode == "--status":
            show_status()
            return
            
        elif mode == "--stop":
            uninstall_launchagent()
            return
            
        elif mode == "--service":
            # This is the background service mode - run the actual organizer
            print(f"Screenshot Organizer service starting... (PID: {os.getpid()})")
            pass  # Continue to main service loop below
        
        else:
            print(f"Unknown option: {mode}")
            print("Available options: --setup, --config-only, --status, --stop")
            return
    else:
        # No arguments - show help
        print("Screenshot Organizer")
        print("===================")
        print("")
        print("To set up: Double-click ScreenshotOrganizer.command")
        print("Or run: python3 main.py --setup")
        print("")
        print("Other commands:")
        print("  --status     Show current status")
        print("  --config     Reconfigure settings only")
        print("  --stop       Stop the background service")
        return
    
    # Service mode - run the main screenshot organizer
    try:
        # blocking screenshot task runs in its own thread
        watcher_task = asyncio.to_thread(detect_screenshots)
        # async cleanup loop
        cleanup_task = asyncio.create_task(cleanup_screenshots_task())
        await asyncio.gather(watcher_task, cleanup_task)
    except KeyboardInterrupt:
        print("Screenshot Organizer service stopped")


if __name__ == "__main__":
    import os
    asyncio.run(main())

# async def main():
#     if input("Configure settings? (y/n) [n]: ").strip().lower() in ("y", "yes"):
#         from config.get_user_config import get_user_config

#         get_user_config()

#     # blocking screenshot task runs in its own thread
#     watcher_task = asyncio.to_thread(detect_screenshots)
#     # async cleanup loop
#     cleanup_task = asyncio.create_task(cleanup_screenshots_task())
#     await asyncio.gather(watcher_task, cleanup_task)


# if __name__ == "__main__":
#     asyncio.run(main())
