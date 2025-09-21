from pathlib import Path
import time
import shutil
import asyncio


async def cleanup_screenshots_task():
    screenshots_dir = Path.home() / "screenshots"

    delete_after_seconds = 30 * 24 * 60 * 60  # delete after 30 days
    scan_interval_seconds = 60 * 60  # scan every hour

    while True:
        await asyncio.sleep(scan_interval_seconds)

        if not screenshots_dir.exists():
            print(f"Screenshots folder {screenshots_dir} does not exist yet")
            continue

        for dir in screenshots_dir.iterdir():
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
