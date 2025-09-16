import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import os
import time

DESKTOP_PATHWAY = "/Users/johnbryce/Desktop"


class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):

        if "Screenshot" not in event.src_path and "screenshot" not in event.src_path:
            print(f"No screenshot found in: {event.src_path}")
            return

        screenshot = event
        move_screenshot(screenshot)

        # This gets called automatically when files are created
        # Check if it's a screenshot, then do something
        pass


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
    print(f"screenshot detected: {screenshot}")
    # moves file to organized folder
    create_folder_structure(screenshot)


def create_folder_structure(screenshot):
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


# TODO: Rename with clean timestamp format (2025-09-15_14-32-05.png).
def rename_screenshot():
    pass


def main():
    detect_screenshots()


if __name__ == "__main__":
    main()
