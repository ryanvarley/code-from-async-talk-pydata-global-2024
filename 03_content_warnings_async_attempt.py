import asyncio
import hashlib
import time

import aiohttp

from utils import API_URL, STATE, get_video_ids, log_message


async def get_video(video_id, session):
    log_message(f"🚀 Get video {video_id}", "red")
    async with session.get(
        f"{API_URL}/videos/{video_id}",
    ) as response:
        response.raise_for_status()
        log_message(f"Finished video {video_id} 🏁", "red")
        return await response.json()


async def get_video_transcript(video_id, session):
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
        log_message(f"Finished {video_id} 🏁", "yellow", offset=76)
        response.raise_for_status()
        return await response.json()


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
    video = await get_video(video_id, session)
    transcript = await get_video_transcript(video_id, session)

    text = f"{video["title"]} {video["description"]} {transcript}"

    warning_ids = []

    result = is_nasa(text, video_id)

    if result:
        warning_ids.append("nasa")

    await save_video_content_warnings(video_id, warning_ids, session=session)
    return warning_ids


async def main(video_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [generate_content_warnings(video_id, session) for video_id in video_ids]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    video_ids = get_video_ids(n=100)
    STATE["time"] = time.time()
    asyncio.run(main(video_ids))
