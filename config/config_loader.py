import json
from pathlib import Path


def load_config():

    default_config = {
        "screenshots_main_directory_name": str(
            Path.home() / "screenshots"
        ),  # /Users/user_name/screenshots
        "use_desktop_pathway": False,  # if user prefers saving on desktop, auto-create the screenshots folder on their desktop
        "delete_after_days": 30,
    }

    CONFIG_PATH = Path(__file__).parent / "config.json"

    if not CONFIG_PATH.exists():
        json.dump(default_config, f, indent=4)
        print(
            f"Created default config file at {CONFIG_PATH}. Please edit it and restart the script."
        )

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)  # turns JSON into a Python dict

    return config


# load once when this module is imported
CONFIG = load_config()
