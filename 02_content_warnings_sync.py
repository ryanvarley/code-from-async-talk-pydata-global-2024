import hashlib
import time

import requests

from utils import API_URL, STATE, get_video_ids, log_message


def get_video(video_id):
    log_message(f"🚀 Get video {video_id}", "red")
    response = requests.get(
        f"{API_URL}/videos/{video_id}",
    )
    response.raise_for_status()
    log_message(f"Finished video {video_id} 🏁", "red")
    return response.json()


def get_video_transcript(video_id):
    log_message(f"🚀 Get transcript {video_id}", "blue", offset=26)
    response = requests.get(f"{API_URL}/videos/{video_id}/transcript")
    log_message(f"Finished {video_id} 🏁", "blue", offset=26)
    response.raise_for_status()
    return response.text


def save_video_content_warnings(video_id, warning_ids):
    log_message(f"🚀 Saving result {video_id}", "yellow", offset=76)
    response = requests.patch(
        f"{API_URL}/videos/{video_id}", json={"warnings": warning_ids}
    )
    response.raise_for_status()
    log_message(f"Finished {video_id} 🏁", "yellow", offset=76)


def is_nasa(text, video_id):
    log_message(f"🚀 Run model {video_id}", "green", offset=52)
    # Simulate a model taking 1s but actually computing vs sleeping
    [hashlib.sha512(b"a" * 10**8).hexdigest() for i in range(10)]
    log_message(f"Finished {video_id} 🏁", "green", offset=52)

    # The "model"
    if "nasa" in text.lower().split():
        return True
    return False


def generate_content_warnings(video_id):
    video = get_video(video_id)
    transcript = get_video_transcript(video_id)

    text = f"{video['title']} {video['description']} {transcript}"
    warning_ids = []

    result = is_nasa(text, video_id)
    if result:
        warning_ids.append("nasa")

    save_video_content_warnings(video_id, warning_ids)


def main(video_ids):
    for video_id in video_ids:
        generate_content_warnings(video_id)


if __name__ == "__main__":
    video_ids = get_video_ids(n=100)

    STATE["time"] = time.time()
    main(video_ids)
