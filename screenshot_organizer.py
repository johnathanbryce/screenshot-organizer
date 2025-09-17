import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import os
import time
from datetime import datetime

DESKTOP_PATHWAY = "/Users/johnbryce/Desktop"


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

        # final validation - ensure the file exists before attempting to move
        if not screenshot_file_path.exists():
            print(f"Screenshot file not found: {screenshot.src_path}")
            return

        # construct the destination path and move the file
        filename = screenshot_file_path.name
        new_file_path = daily_dir / filename
        print(f"Moving: {screenshot_file_path} -> {new_file_path}")

        # move the file to the organized folder
        screenshot_file_path.rename(new_file_path)
        print(f"Successfully moved screenshot to {new_file_path}")

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
        print("screenshots directory already exists")
        pass  # directory already exists
    except PermissionError:
        print("Permission error...")
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
        print(f"{daily_dir} directory already exists")
        pass  # directory already exists
    except PermissionError:
        print("Permission error...")
    return daily_dir


# TODO: Rename with clean timestamp format (2025-09-15_14-32-05.png).
def rename_screenshot():
    pass


def main():
    detect_screenshots()


if __name__ == "__main__":
    main()
