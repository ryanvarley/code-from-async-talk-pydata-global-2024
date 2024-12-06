import asyncio
import hashlib
import time

import aiohttp

from utils import API_URL, STATE, get_video_ids, log_message

# add sempahores to limit the number of concurrent requests
video_semaphore = asyncio.Semaphore(5)
transcript_semaphore = asyncio.Semaphore(10)


async def get_video(video_id, session):
    # Sempahores are used as a context manager and block if the limit is reached
    async with video_semaphore:
        log_message(f"🚀 Get video {video_id}", "red")
        async with session.get(
            f"{API_URL}/videos/{video_id}",
        ) as response:
            response.raise_for_status()
            log_message(f"Finished video {video_id} 🏁", "red")
            return await response.json()


async def get_video_transcript(video_id, session):
    # Note this semaphore too
    async with transcript_semaphore:
        log_message(f"🚀 Get transcript {video_id}", "blue", offset=26)
        async with session.get(
            f"{API_URL}/videos/{video_id}/transcript",
        ) as response:
            log_message(f"Finished {video_id} 🏁", "blue", offset=26)
            response.raise_for_status()
            return await response.text()


async def save_video_content_warnings(video_id, warning_ids, session):
    log_message(f"🚀 Saving result {video_id}", "yellow", offset=76)
    async with session.patch(
        f"{API_URL}/videos/{video_id}", json={"warnings": warning_ids}
    ) as response:
        response.raise_for_status()
    log_message(f"Finished {video_id} 🏁", "yellow", offset=76)


def is_nasa(text, video_id):
    """Would contain a more complex model in a real case."""
    log_message(f"🚀 Run model {video_id}", "green", offset=52)
    # Simulate a model taking 1s but actually computing vs sleeping
    [hashlib.sha512(b"a" * 10**8).hexdigest() for i in range(10)]
    log_message(f"Finished {video_id} 🏁", "green", offset=52)

    # The "model"
    if "nasa" in text.lower().split():
        return True

    return False


async def generate_content_warnings(video_id, session):
    # We asyncio.gather now instead of awaiting individually which was blocking
    video_task = get_video(video_id, session)
    transcript_task = get_video_transcript(video_id, session)
    video, transcript = await asyncio.gather(video_task, transcript_task)

    text = f"{video["title"]} {video["description"]} {transcript}"

    warning_ids = []

    # We can use the loop to run the blocking function in a separate thread
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, is_nasa, text, video_id)

    # We could also use a ProcessPoolExecutor to run the blocking function in a separate process
    # This is better if CPU heavy as we are only unblocking the event loop above, not
    # using and more CPU power. However you would need to deal with multiprocessing issues.

    # from concurrent.futures import ProcessPoolExecutor
    # with ProcessPoolExecutor() as executor:
    # result = await loop.run_in_executor(executor, is_nasa, text, video_id)

    if result:
        warning_ids.append("nasa")

    await save_video_content_warnings(video_id, warning_ids, session=session)


async def main(video_ids):
    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [generate_content_warnings(video_id, session) for video_id in video_ids]

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    video_ids = get_video_ids(n=100)
    STATE["time"] = time.time()
    asyncio.run(main(video_ids))
