from bs4 import BeautifulSoup
import aiohttp
from pathlib import Path
import aiofiles
import asyncio
import requests

IMAGE_FORMATS = ("png", "gif", "jpg", "bpm")


def get_pages_for_tag(link: str):
    text = requests.get(link).text

    soup = BeautifulSoup(text, features="html.parser")

    if soup.title == "No Images Found":
        return 0

    last_tag = soup.find("a", text="Last")

    if last_tag is None:
        return 1  # When title is not "No Images Found" but there are no line, there are exactly one page

    n_pages = int(last_tag["href"].split("/")[-1])
    return n_pages


async def get_elements_on_page(link: str, get_videos: bool, put_to: list, semaphore: asyncio.Semaphore):
    await semaphore.acquire()
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            text = await resp.text()

    semaphore.release()

    soup = BeautifulSoup(text, features="html.parser")

    for parent_tag in soup.find_all("div", class_="shm-thumb thumb"):
        if parent_tag["data-ext"] not in IMAGE_FORMATS and not get_videos:
            continue

        object_name = parent_tag["data-tags"] + \
            " " + parent_tag["data-post-id"]

        children = parent_tag.find("a", text="Image Only")
        link = children["href"]

        put_to.append((link, object_name))


async def download_file(t: tuple, path: Path, semaphore: asyncio.Semaphore, vebrose: bool, skip_existing: bool):
    if skip_existing and (path/t[1]).exists():
        return

    await semaphore.acquire()
    if vebrose:
        print(f"Downloading {t[0]}")
    async with aiohttp.ClientSession() as session:
        async with session.get(t[0]) as resp:
            if resp.status == 200:
                f = await aiofiles.open(path/t[1], mode='wb')
                await f.write(await resp.read())
                await f.close()
    semaphore.release()
