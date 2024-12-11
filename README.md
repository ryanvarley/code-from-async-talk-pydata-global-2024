# Let's Get You Started with Asynchronous Programming | Ryan Varley

**PyData Global 2024 | 3rd December 2024**

This repository contains the code from my talk. You can find more information about the talk [here](https://blog.dataleadership.ai/p/pydata-get-started-with-python-async-in-25-minutes-talk).

The video of the talk is not yet available (unless you attended the conference). I will update this README when it is.

![](https://github.com/user-attachments/assets/5d286788-e89f-49a7-8fcf-62de6e0defd0)

## Overview

This repository consists of:

- `test-server`: A simple mock server that you can run locally to mimic the behaviour of the real server used in the talk. Note that you will get different results I did (e.g. timings) for this reason!
- `01_snippets_from_the_slides.ipynb`: Working versions of most of the code snippets from the talk.
- `02_content_warnings_sync.py`: The synchronous code for the content warnings application.
- `03_content_warnings_async_attempt.py`: The first attempt at an asynchronous content warnings application that contained some mistakes.
- `04_content_warnings_async_final.py`: The final version of the content warnings application.

I recommend running the code in this order, following the instructions below. All code requires the test server to be running (see below).

This guide assumes you are in the terminal and have not activated the `poetry shell`. If you have, just remove `poetry run` from the commands.

## Installation

This guide assumes you are using a Mac. Most steps will be very similar on Linux. YMMV on Windows.

You will need to install [Poetry](https://python-poetry.org/) if you haven't already.

Then, you can run `poetry install`. If you are having trouble using the correct version of Python, I recommend looking at [pyenv](https://github.com/pyenv/pyenv).

## Running the Local Server

In the repository directory, run (assuming you are not in the Poetry shell):

```bash
poetry run fastapi run test-server/main.py --workers 1
```

If successful, you should see something like:

>INFO   Uvicorn running on <http://0.0.0.0:8000> (Press CTRL+C to quit)  
>INFO   Started reloader process [32305] using WatchFiles  
>INFO   Started server process [32329]  
>INFO   Waiting for application startup.  
>INFO   Application startup complete.  

Leave that running and open a new terminal window, then return to the root directory of this repository.

## Running the Notebook

In the root directory of this repository, run:

```bash
poetry run jupyter lab
```

Open the notebook and run the cells in order.

I recommend using the `execute_time` extension for Jupyter so you can see runtimes, or running the notebook in VS Code if you are familiar with it.

## Running the Content Warnings Service

There are three versions:

First, the synchronous version I showed the output of, but not the code. Notice everything happening in order:

![](https://github.com/user-attachments/assets/283cea9f-0531-4d82-a6fa-9180e51619bf)

*Runtime approx 108s*

```bash
poetry run python 02_content_warnings_sync.py
```

Next, the first attempt at an asynchronous version that had inefficiencies:

Note that this version will likely fail with
>aiohttp.client_exceptions.ClientOSError: [Errno 54] Connection reset by peer
I started to try and fix this but the actual fix is the next script and if anything this is a better lesson. I *think* the core issue is the blocking model function doesn't allow other coroutines to run often enough and so the PATCH requests start timing out before they can be resumed.

![](https://github.com/user-attachments/assets/622d3741-7b13-4896-b9cc-77ca53076743)

*Runtime approx 8s before failure*

```bash
poetry run python 03_content_warnings_async_attempt.py
```

And lastly, the final version where we fixed these issues:

![](https://github.com/user-attachments/assets/5d286788-e89f-49a7-8fcf-62de6e0defd0)

*Runtime approx 13s*

```bash
poetry run python 04_content_warnings_async_final.py
```
