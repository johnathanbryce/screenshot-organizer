from pathlib import Path
import time
import shutil
import asyncio
from config.config_loader import CONFIG


async def cleanup_screenshots_task():
    delete_after_days = CONFIG["delete_after_days"]
    user_prefers_desktop = CONFIG["use_desktop_pathway"]

    if user_prefers_desktop:
        screenshot_base_dir = Path.home() / "Desktop" / "screenshots"
    else:
        screenshot_base_dir = Path.home() / "screenshots"

    delete_after_seconds = (
        delete_after_days * 24 * 60 * 60
    )  # (deletion day(s) defined in config.json)
    scan_interval_seconds = 60 * 60  # scan every hour

    while True:
        await asyncio.sleep(scan_interval_seconds)

        if not screenshot_base_dir.exists():
            print(f"Screenshots folder {screenshot_base_dir} does not exist yet")
            continue

        for dir in screenshot_base_dir.iterdir():
            # skip hidden files/folders and ensure it's a directory
            if dir.name.startswith(".") or not dir.is_dir():
                continue

            try:
                dir_age_seconds = time.time() - dir.stat().st_ctime
                print(f"{dir} is {dir_age_seconds:.2f} seconds old")

                if dir_age_seconds >= delete_after_seconds:
                    shutil.rmtree(dir)
                    print(f"Deleted folder: {dir}")
            except Exception as e:
                print(f"Failed to delete folder {dir}: {e}")
