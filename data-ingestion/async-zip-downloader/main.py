import os
import requests
import aiohttp
import asyncio
import zipfile
from aiohttp import ClientError

DOWNLOAD_URLS = [
    "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-zip-file.zip",
    "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-large-zip-file.zip",
    "https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.zip",  # broken (test error handling)
    "https://example.com/nonexistent.zip",  # broken (test error handling)
]

DOWNLOAD_DIR = "downloads"


def get_filename_from_url(url):
    """
    Get the filename from the url
    """
    return url.split("/")[-1] or "download.zip"


async def download_and_extract(session, url):
    """
    Downloads a ZIP file and extracts its contents into a unique subfolder.
    """
    try:
        print(f"Downloading: {url}")
        async with session.get(url, timeout=15) as response:
            if response.status != 200:
                raise ClientError(f"HTTP Error {response.status}")
            data = await response.read()

        filename = get_filename_from_url(url)
        zippath = os.path.join(DOWNLOAD_DIR, filename)

        with open(zippath, "wb") as f:
            f.write(data)

        if not zipfile.is_zipfile(zippath):
            raise ValueError(f"{zippath} is not a valid ZIP file")

        subfolder_name = os.path.splitext(filename)[0]
        extract_path = os.path.join(DOWNLOAD_DIR, subfolder_name)
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(zippath, "r") as z:
            z.extractall(extract_path)
            print(f"Extracted: {filename}")
        print(zippath)
        os.remove(zippath)

    except Exception as e:
        print(f"Error downloading {url} : {e}")


async def main():
    """
    Main function to run the download and extraction
    """
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = [download_and_extract(session, url) for url in DOWNLOAD_URLS]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
