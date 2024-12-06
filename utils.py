"""
Some non-essential shared common code between the scripts
"""

import time

import requests
from rich.console import Console
from rich.text import Text

console = Console()

STATE = {"time": None}

API_URL = "http://0.0.0.0:8000"


def get_video_ids(n=100):
    response = requests.get(
        f"{API_URL}/videos?n={n}",
    )
    response.raise_for_status()
    return response.json()


def log_message(message, color, offset=0):
    elapsed_time = time.time() - STATE["time"]
    formatted_time = f"[{elapsed_time:>7.2f}s] "
    text = Text(formatted_time + " " * offset + message, style=color)
    console.print(text)
