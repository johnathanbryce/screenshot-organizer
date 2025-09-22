from config.config_loader import CONFIG


def get_user_config():
    print("\n=== Screenshot Organizer Configuration ===")
    print("Leave blank to use current/default values")

    # enable/disable auto deletion input:
    auto_delete_screenshots_config = CONFIG["auto_delete_directories"]
    auto_deletion_input = input(f"Enable auto-deletion of screenshots? (y/n) [y]: ")
    if auto_deletion_input.lower() in ("", "y", "yes"):
        auto_delete_screenshots_config = True
    else:

        auto_delete_screenshots_config = False
    CONFIG["auto_delete_directories"] = auto_delete_screenshots_config

    # delete after days input:
    current_delete_config = CONFIG.get("delete_after_days", 30)
    while auto_delete_screenshots_config:
        try:
            delete_after_days_input = input(
                f"Delete screenshots after days (input number between 0 - 365): "
            ).strip()

            if delete_after_days_input == "":
                CONFIG["delete_after_days"] = current_delete_config
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
