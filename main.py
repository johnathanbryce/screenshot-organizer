import asyncio
from cleanup_screenshots import cleanup_screenshots_task
from screenshot_organizer import detect_screenshots

# TODO:

# 3. prompt for user input to allow user to control the following (global variables with reset functionality i.e. reset.py w/ cmd: 'python reset.py')
#       - folder name: daily_dir -- > allow flexibility for date format
#               - either default setup (01 -04:25 PM) or (screenshot-01, screenshot-02, etc)
# 4. error handling
# 5. task runner
# 6. gracefully stop runner and cleanup the loop instead of force quit via ctrl+c or program shut down (i.e turning off computer)


async def main():
    if input("Configure settings? (y/n) [n]: ").strip().lower() in ("y", "yes"):
        from config.get_user_config import get_user_config

        get_user_config()

    # blocking screenshot task runs in its own thread
    watcher_task = asyncio.to_thread(detect_screenshots)
    # async cleanup loop
    cleanup_task = asyncio.create_task(cleanup_screenshots_task())
    await asyncio.gather(watcher_task, cleanup_task)


if __name__ == "__main__":
    asyncio.run(main())
