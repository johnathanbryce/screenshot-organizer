import asyncio
from cleanup_screenshots import cleanup_screenshots_task
from screenshot_organizer import detect_screenshots

# TODO:
# - isolate get_user_config into functional steps instead of all in the fn
# -  create a script command 'python reset_settings.py' for a user to run initiate get_user_config to allow a user to reset their settings?
# - error handling
# - task runner
# - gracefully stop runner and cleanup the loop instead of force quit via ctrl+c or program shut down (i.e turning off computer)


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
