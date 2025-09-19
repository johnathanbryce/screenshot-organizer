import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import os
import time
import threading
import shutil
import asyncio
from datetime import datetime

DESKTOP_PATHWAY = "/Users/johnbryce/Desktop"

# TODO:
# 2. auto-folder or entire screenshot deletion after X amount of time
# 3. prompt for user input to allow user to control the following (global variables with reset functionality i.e. reset.py w/ cmd: 'python reset.py')
#       - folder name: daily_dir -- > allow flexibility for date format
#               - either default setup (01 -04:25 PM) or (screenshot-01, screenshot-02, etc)
#       - auto folder deletion: enable or disable, if enabled set deletion for every X days in number between 1 - 365
#       - where screenshots folder exists: /Users/ (default) or on Desktop
# 4. error handling
# 5. task runner
# 6. gracefully stop runner and cleanup the loop instead of force quit via ctrl+c or program shut down (i.e turning off computer)


class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):

        if "Screenshot" not in event.src_path and "screenshot" not in event.src_path:
            print(f"No screenshot found in: {event.src_path}")
            return

        screenshot = event
        move_screenshot(screenshot)


def detect_screenshots():
    # watches for new files
    screenshot_handler = ScreenshotHandler()

    observer = Observer()
    observer.schedule(screenshot_handler, DESKTOP_PATHWAY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()


def move_screenshot(screenshot):
    """
    Moves a detected screenshot file from the Desktop to an organized daily folder.

    Handles macOS screenshot creation behavior where temporary hidden files (.Screenshot)
    are created first, then renamed to the final filename (Screenshot).

    Args:
        screenshot: FileSystemEvent object containing the src_path of the detected screenshot
    """
    # create the daily folder structure and get the target directory
    daily_dir = create_folder_structure()
    if not daily_dir.exists():
        print("Daily directory doesn't exist!")
        return

    try:
        # wait for macOS to finish the file creation process
        time.sleep(0.5)

        # Get the initial file path from the watchdog event
        screenshot_file_path = Path(screenshot.src_path)

        # macOS creates temporary screenshots with .Screenshot prefix, then renames to Screenshot
        # if the temp file doesn't exist, check for the final renamed file
        if not screenshot_file_path.exists() and screenshot_file_path.name.startswith(
            "."
        ):
            # remove the leading dot to get the final filename (i.e. remove the . from .Screenshot)
            final_filename = screenshot_file_path.name[1:]  #
            screenshot_file_path = screenshot_file_path.parent / final_filename

        # construct the destination path and move the file
        filename = screenshot_file_path.name
        # change the name of the screenshot to be more user friendly
        updated_filename = rename_screenshot(filename, daily_dir)
        new_file_path = daily_dir / updated_filename

        # move the file to the organized folder
        screenshot_file_path.rename(new_file_path)

    except FileNotFoundError:
        print("Screenshot was not moved to daily directory - file not found")
    except Exception as e:
        print(f"Error moving screenshot: {e}")


def create_folder_structure():
    # ensure folder destination exists & create the directories to hold the screenshots
    # 1. initializes the screenshots folder in /Users/username
    home_dir = Path.home()
    screenshots_dir = home_dir / "screenshots"
    try:
        screenshots_dir.mkdir()
    except FileExistsError:
        pass  # directory already exists
    except PermissionError:
        print("Permission error during creation of screenshots folder...")
    # 2. creates the daily folder for the screenshot inside /Users/username/screenshots
    if screenshots_dir.exists():
        # create the daily directory formatted as "DD MM YEAR i.e. 17 September 2025"
        daily_dir = create_daily_directory(screenshots_dir)
        return daily_dir


def create_daily_directory(screenshots_dir):
    current_date = datetime.now().strftime("%d %B %Y")
    daily_dir = screenshots_dir / current_date
    try:
        daily_dir.mkdir()
    except FileExistsError:
        pass  # directory already exists
    except PermissionError:
        print("Permission error in creation of daily directory...")
    return daily_dir


def get_screenshot_count(daily_dir):
    """Count existing screenshots and return next number."""
    if not daily_dir.exists():
        return 1

    # Only count image files to be more precise
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}
    existing_screenshots = sum(
        1
        for f in daily_dir.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    )

    return existing_screenshots + 1


def rename_screenshot(filename, daily_dir):
    """
    Rename screenshot with human-readable format and counter.

    Args:
        filename: Original screenshot filename
        daily_dir: Path to the daily directory

    Returns:
        str: New filename in format "01 - 12:47 PM.png"
    """
    now = datetime.now()
    original_path = Path(filename)
    file_extension = original_path.suffix or ".png"

    # get the current count of screenshots in the daily directory
    screenshot_count = get_screenshot_count(daily_dir)

    # format: "01 - 04.25 PM.png"
    # time_str = now.strftime("%I.%M %p")
    time_str = now.strftime("%I∶%M %p")
    updated_filename = f"{screenshot_count:02d} - {time_str}{file_extension}"

    return updated_filename


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


async def main():
    # blocking screenshot task runs in its own thread
    watcher_task = asyncio.to_thread(detect_screenshots)
    # async cleanup loop
    cleanup_task = asyncio.create_task(cleanup_screenshots_task())
    await asyncio.gather(watcher_task, cleanup_task)


if __name__ == "__main__":
    asyncio.run(main())
