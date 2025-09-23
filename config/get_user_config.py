from config.config_loader import CONFIG
from pathlib import Path
import json
import os
import platform

home = Path.home()


def clear_screen():
    if platform.system() == "windows":
        os.system("cls")
    else:
        os.system("clear")


def show_section_header(title):
    """Clear screen and show a section header"""
    clear_screen()
    print(f"\n{'='*50}")
    print(f"⚙️  {title}")
    print(f"{'='*50}\n")


def get_user_config():
    """
    Allows users to configure their screenshot settings.
    Configurations are saved directly to config.json via the CONFIG object.

    Allow for customization of the following:
        1. main directory name
        2. use desktop pathway or default pathway
        3. enable/disable auto screenshot file naming
        4. enable/disable auto screenshot deletion
        5. if screenshot deletion enabled, determine deletion for individual folders after X days

    """
    while True:
        # print("\n===== Screenshot Organizer Configuration =====\n")
        show_section_header("Screenshot Organizer Configuration")
        print("Leave blank to use current/default values\n")

        show_section_header("Main Folder Settings")
        # 1. main screenshots directory name
        screenshots_main_directory_name_config = CONFIG[
            "screenshots_main_directory_name"
        ]
        screenshots_main_directory_name_input = input(
            f'Customize your main screenshots folder name (default folder name is "screenshots")? (y/n) [n]: '
        ).lower()
        if screenshots_main_directory_name_input in ("y", "yes"):
            while True:
                folder_name = input("Enter your custom folder name: ").strip()
                if len(folder_name) == 0 or len(folder_name) > 100:
                    print("Folder name must be between 1 - 100 characters.")
                    continue

                screenshots_main_directory_name_config = folder_name
                CONFIG["screenshots_main_directory_name"] = (
                    screenshots_main_directory_name_config
                )
                break

        # 2. use desktop pathway for screenshots folder input:
        show_section_header("Main Folder Storage Location")
        use_desktop_pathway_config = CONFIG["use_desktop_pathway"]
        print(
            f"\n==== Your main screenshots folder will be created at: {home}/{CONFIG['screenshots_main_directory_name']} ====\n"
        )
        use_desktop_pathway_input = input(
            f'Would you like your main screenshots folder "{CONFIG['screenshots_main_directory_name']}" to be created on your Desktop instead? (y/n) [n]: '
        ).lower()
        if use_desktop_pathway_input in ("", "y", "yes"):
            use_desktop_pathway_config = True
        else:
            use_desktop_pathway_config = False
        CONFIG["use_desktop_pathway"] = use_desktop_pathway_config

        show_section_header("Screenshot File Naming")
        # 3. enable/disable auto screenshot file naming (default is true):
        print(
            "\n==== Via this script, screenshots are automatically numbered and timestamped ==== \n"
        )
        print(
            f"\nExample format of screenshots saved: 01 - 03:45 PM.png, 02 - 03:47 PM.png, etc. \n"
        )
        use_auto_screenshot_naming_input = input(
            f"Enable organized screenshot naming? (y = numbered/timestamped, n = keep default names) [y]: "
        ).lower()
        if use_auto_screenshot_naming_input.lower() in ("", "y", "yes"):
            CONFIG["use_auto_screenshot_naming"] = True
        else:
            CONFIG["use_auto_screenshot_naming"] = False

        # 4. enable/disable auto deletion input:
        show_section_header("Auto Deletion Settings")
        auto_delete_screenshots_config = CONFIG["auto_delete_directories"]
        auto_deletion_input = input(
            f"Enable auto-deletion of screenshots? (y/n) [y]: "
        ).lower()

        # only enable auto-deletion if user explicitly says "yes"
        auto_delete_enabled = auto_deletion_input in (
            "y",
            "yes",
        )
        CONFIG["auto_delete_directories"] = auto_delete_enabled

        # 5. delete after days input (ONLY if auto-deletion is explicitly enabled):
        if auto_delete_enabled:
            show_section_header("Deletion Timeline")
            current_delete_days_config = CONFIG.get("delete_after_days", 30)

            while True:
                try:
                    delete_after_days_input = input(
                        f"Delete screenshots after days (0-365) [{current_delete_days_config}]: "
                    ).strip()

                    if delete_after_days_input == "":
                        CONFIG["delete_after_days"] = current_delete_days_config
                        print(f"Using default of {current_delete_days_config} days")
                        break

                    delete_after_days_input_num = int(delete_after_days_input)

                    if not (0 <= delete_after_days_input_num <= 365):
                        print("Invalid number, please input between 0 - 365")
                    else:
                        CONFIG["delete_after_days"] = delete_after_days_input_num
                        break

                except ValueError:
                    print("Incorrect input, please try again.")
        else:
            # FIX: Remove delete_after_days when auto-deletion is disabled
            CONFIG.pop("delete_after_days", None)

        show_section_header("Configuration Summary")
        print(json.dumps(CONFIG, indent=2, sort_keys=True))

        confirm_config_input = input(
            '\nSave this configuration? (Enter "n" to start over) [y]: '
        )
        if confirm_config_input in ("", "y", "yes"):
            show_section_header("Configuration Saved")
            break  # exit config loop
        else:
            print("Restarting configuration...")
            continue  # restart config loop
