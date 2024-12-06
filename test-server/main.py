"""
A test server to run our async code against.

This server somewhat simulates the behaviour of the real video service used during the talk. 
It is not meant to be accurate but rather to provide a similar experience without the risk 
of accidentally starting a DoS attack on a real service.

The endpoints behave predictably, without randomness, to allow you to observe the impact 
in a controlled environment. The exception is degradation: the endpoints degrade severely 
if "overloaded," simulating that aspect of the talk.
"""

import asyncio

import fastapi
from video_db import video_db

app = fastapi.FastAPI()

# Endpoint semaphores to simulate degradation
# Artifical delays are added based on # requests above threshold
video_semaphore = asyncio.Semaphore(value=10)
transcript_semaphore = asyncio.Semaphore(value=20)


@app.get("/videos/")
async def videos_list(n: int = 100):
    """Return a list of all video IDs."""
    await asyncio.sleep(0.05)
    return list(video_db.keys())[:n]


@app.get("/videos/{video_id}")
async def videos(video_id: str):
    await artificial_delay(
        semaphore=video_semaphore, min_delay=0.2, degredation_factor=0.1
    )
    try:
        video_data = video_db[video_id]
        return {
            key: value for key, value in video_data.items() if not key == "transcript"
        }
    except KeyError:
        raise fastapi.HTTPException(status_code=404, detail="Video not found")


@app.patch("/videos/{video_id}")
async def videos_update(video_id: str, data: dict):
    video_db[video_id].update(data)
    await asyncio.sleep(0.05)
    return "success"


@app.get("/videos/{video_id}/transcript")
async def transcript(video_id: str):
    await artificial_delay(
        semaphore=transcript_semaphore,
        min_delay=0.1,
    )
    try:
        return video_db[video_id]["transcript"]
    except KeyError:
        raise fastapi.HTTPException(status_code=404, detail="Video not found")


async def artificial_delay(
    semaphore: asyncio.Semaphore, min_delay: float = 0.05, degredation_factor=0.1
):
    """Simulate a delay in fetching a video.

    Implements a threshold above which the service significantly slows down.
    """

    async with semaphore:
        if semaphore._waiters:
            waiters = len(semaphore._waiters)
            degradation_delay = degredation_factor * min(waiters, 10)
        else:
            degradation_delay = 0

        delay = min_delay + degradation_delay

        await asyncio.sleep(delay)
        return
