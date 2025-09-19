import asyncio
from cleanup_screenshots import cleanup_screenshots_task
from screenshot_organizer import detect_screenshots


async def main():
    # blocking screenshot task runs in its own thread
    watcher_task = asyncio.to_thread(detect_screenshots)
    # async cleanup loop
    cleanup_task = asyncio.create_task(cleanup_screenshots_task())
    await asyncio.gather(watcher_task, cleanup_task)


if __name__ == "__main__":
    asyncio.run(main())
