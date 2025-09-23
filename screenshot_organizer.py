from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time
from datetime import datetime
from config.config_loader import CONFIG

home_dir = Path.home()
DESKTOP_PATHWAY = f"{home_dir}/Desktop"


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

        # change the name of the screenshot to be more user friendly if enabled
        use_auto_screenshot_renaming = CONFIG["use_auto_screenshot_naming"]
        if use_auto_screenshot_renaming:
            filename = rename_screenshot(
                filename, daily_dir
            )  # override default file name with custom screenshot file name (automatically numbered and timestamped)

        new_file_path = daily_dir / filename

        # move the file to the organized folder
        screenshot_file_path.rename(new_file_path)

    except FileNotFoundError:
        print("Screenshot was not moved to daily directory - file not found")
    except Exception as e:
        print(f"Error moving screenshot: {e}")


def create_folder_structure():
    user_prefers_desktop = CONFIG["use_desktop_pathway"]

    # ensure folder destination exists & create the directories to hold the screenshots
    if user_prefers_desktop:
        screenshot_base_dir = (
            Path.home() / "Desktop" / CONFIG["screenshots_main_directory_name"]
        )
    else:
        screenshot_base_dir = Path.home() / CONFIG["screenshots_main_directory_name"]

    # ensure base directory exists
    try:
        screenshot_base_dir.mkdir(exist_ok=True)
    except PermissionError:
        print("Permission error during creation of screenshots folder...")

    # create the daily folder inside base directory
    if screenshot_base_dir.exists():
        daily_dir = create_daily_directory(screenshot_base_dir)
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
