

# TODO:
# - task runner
# -  create a script command 'python reset_settings.py' for a user to run initiate get_user_config to allow a user to reset their settings?
# - error handling
# - gracefully stop runner and cleanup the loop instead of force quit via ctrl+c or program shut down (i.e turning off computer)

import asyncio
import sys
from pathlib import Path


def install_background_service():
    """Install LaunchAgent to run this script in background"""
    import subprocess
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
    result = subprocess.run(['launchctl', 'load', str(plist_file)], capture_output=True, text=True)
    if result.returncode == 0:
        print("Background service installed and started!")
        print("Your screenshot organizer will now run automatically even when you close this window.")
        print(f"Logs: {Path.home()}/Library/Logs/screenshot-organizer.log")
    else:
        print(f"Service installed but may not have started: {result.stderr}")


def uninstall_background_service():
    """Remove the background service"""
    import subprocess
    from pathlib import Path
    
    plist_file = Path.home() / "Library" / "LaunchAgents" / "com.screenshot-organizer.plist"
    
    if plist_file.exists():
        # Unload the service
        subprocess.run(['launchctl', 'unload', str(plist_file)], capture_output=True)
        # Remove the plist file  
        plist_file.unlink()
        print("Background service stopped and removed")
    else:
        print("No background service found")


async def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "--config":
            # Just run configuration, don't start the service
            if input("Configure settings? (y/n) [n]: ").strip().lower() in ("y", "yes"):
                from config.get_user_config import get_user_config
                get_user_config()
            return  # Exit after config
            
        elif mode == "--install":
            print("Installing background service...")
            install_background_service()
            return
            
        elif mode == "--uninstall":
            print("Removing background service...")
            uninstall_background_service()
            return
            
        elif mode == "--service":
            # Import watchdog modules only when needed for service
            try:
                from cleanup_screenshots import cleanup_screenshots_task
                from screenshot_organizer import detect_screenshots
                from config.config_loader import CONFIG
            except ImportError as e:
                print(f"Import error: {e}")
                print("Make sure watchdog is installed: pip install watchdog")
                return
                
            import os
            print(f"Screenshot Organizer background service started (PID: {os.getpid()})")
            print(f"Working directory: {os.getcwd()}")
            print(f"Script location: {Path(__file__).parent.absolute()}")
            
            # Check if config file exists and show its contents
            config_file = Path(__file__).parent / "config" / "config.json"
            print(f"Looking for config at: {config_file}")
            print(f"Config file exists: {config_file.exists()}")
            
            if config_file.exists():
                import json
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                print(f"Config contents: {config_data}")
            
            # Continue to main loop below
            pass
        
        else:
            print(f"Unknown option: {mode}")
            print("Available options: --config, --install, --uninstall")
            return
    else:
        # Normal interactive mode
        if input("Configure settings? (y/n) [n]: ").strip().lower() in ("y", "yes"):
            from config.get_user_config import get_user_config
            get_user_config()

    # Run the main screenshot organizer (only if we get here)
    try:
        from cleanup_screenshots import cleanup_screenshots_task
        from screenshot_organizer import detect_screenshots
        
        watcher_task = asyncio.to_thread(detect_screenshots)
        cleanup_task = asyncio.create_task(cleanup_screenshots_task())
        await asyncio.gather(watcher_task, cleanup_task)
    except KeyboardInterrupt:
        print("Screenshot Organizer stopped")
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure watchdog is installed: pip install watchdog")


if __name__ == "__main__":
    import os
    asyncio.run(main())