# Async Download Zip Files

This project downloads multiple zip files 
concurrently using Python `aiohttp` and `asyncio`,
extracts them into indivdual subfolders, and clean up ZIPs.

Designed for practicing data engineering tasks like automated 
file acquistions and extractions, and is containerized 
with `Docker`


## Features
- Asynchronous file downloads with `aiohttp`
- Automatic ZIP extraction into organized subfolders
- Graceful error handling (404s, invalid ZIPs)
- Dockerized for ease of use
- Volume mounting to persist extracted data

## Requirements
[] Python
[] Docker


## Running with Docker
```python
docker build -t async-zip-downloader .
docker run async-zip-downloader
docker run -it --entrypoint /bin/bash async-zip-downloader
```


## Running Locally
```python
python main.py
```




