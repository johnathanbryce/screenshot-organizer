from config.config_loader import CONFIG
from pathlib import Path

home = Path.home()


def get_user_config():
    """
    Allows users to configure their screenshot settings.

    Runs on main script load and overrides config.json file based on user input. Restarting of the script requires re-prompting .

    Allow for customization of the following:
        1. main directory name
        2. use desktop pathway or default pathway
        3. enable/disable auto screenshot file naming
        4. enable/disable auto screenshot deletion
        5. if screenshot deletion enabled, determine deletion cadence for individual folders after X days

    """
    print("\n===== Screenshot Organizer Configuration =====\n")
    print("Leave blank to use current/default values\n")

    # 1. main screenshots directory name
    screenshots_main_directory_name_config = CONFIG["screenshots_main_directory_name"]
    screenshots_main_directory_name_input = input(
        f'Customize your main screenshots folder name (default is "screenshots")? (y/n) [n]'
    ).lower()
    if screenshots_main_directory_name_input in ("y", "yes"):
        while True:
            folder_name = input("Enter folder name: ").strip()
            if len(folder_name) == 0 or len(folder_name) > 100:
                print("Folder name must be between 1 - 100 characters.")
                continue

            screenshots_main_directory_name_config = folder_name
            CONFIG["screenshots_main_directory_name"] = (
                screenshots_main_directory_name_config
            )
            break

    # 2. use desktop pathway for screenshots folder input:
    use_desktop_pathway_config = CONFIG["use_desktop_pathway"]
    print(
        f"\n==== Your main screenshots folder will be created in: {home}/{CONFIG['screenshots_main_directory_name']} ====\n"
    )
    use_desktop_pathway_input = input(
        f"Would you like your screenshots folder to be created on your Desktop instead? (y/n) [y]: "
    ).lower()
    if use_desktop_pathway_input in ("", "y", "yes"):
        use_desktop_pathway_config = True
    else:
        use_desktop_pathway_config = False
    CONFIG["use_desktop_pathway"] = use_desktop_pathway_config

    # 3. enable/disable auto screenshot file naming (default is true):
    print(
        "\n==== Via this script, screenshots are automatically numbered and timestamped (default)"
    )
    print("Format: 01 - 03:45 PM.png, 02 - 03:47 PM.png, etc.")
    use_auto_screenshot_naming_input = input(
        f"Enable organized screenshot naming? (y = numbered/timestamped, n = keep original names) [y]:"
    ).lower()
    if use_auto_screenshot_naming_input.lower() in ("", "y", "yes"):
        CONFIG["use_auto_screenshot_naming"] = True
    else:
        CONFIG["use_auto_screenshot_naming"] = False

    # 4. enable/disable auto deletion input:
    auto_delete_screenshots_config = CONFIG["auto_delete_directories"]
    auto_deletion_input = input(
        f"Enable auto-deletion of screenshots? (y/n) [y]: "
    ).lower()
    if auto_deletion_input in ("", "y", "yes"):
        auto_delete_screenshots_config = True
    else:
        auto_delete_screenshots_config = False
    CONFIG["auto_delete_directories"] = auto_delete_screenshots_config

    # 5. delete after days input:
    current_delete_days_config = CONFIG.get("delete_after_days", 30)
    while auto_delete_screenshots_config:
        try:
            delete_after_days_input = input(
                f"Delete screenshots after days (input number between 0 - 365): "
            ).strip()

            if delete_after_days_input == "":
                CONFIG["delete_after_days"] = current_delete_days_config
                break  # default config of 30 will be used if left blank

            delete_after_days_input_num = int(delete_after_days_input)

            if not (0 <= delete_after_days_input_num <= 365):
                print("Invalid number, please input between 0 - 365")
            else:
                CONFIG["delete_after_days"] = delete_after_days_input_num
                break

        except ValueError:
            print("Incorrect input, please try again.")
        except KeyboardInterrupt:
            print("Cancelling custom config setup, script will use default settings.")
            return CONFIG

    print(f"CONFIG from config.json: {CONFIG}")
