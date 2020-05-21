import typer
import asyncio
import aiohttp
from pathlib import Path
from click_spinner import spinner
from utils import *

BASE_LINK = "http://rule34.paheal.net/post/list/{}/{}"


def main(tag: str, pages_to_parse: int = 10, download_videos: bool = True, skip_existing: bool = True, download_path: str = "", concurent_downloads: int = 10, vebrose: bool = False):
    download_folder = Path(download_path or f"./{tag}")
    download_folder.mkdir()
    print("Getting number of available pages and checking if there are any")
    with spinner():
        actual_pages = get_pages_for_tag(BASE_LINK.format(tag, 1))

    if actual_pages == 0:
        print("There are no images on that tag")
        return

    if actual_pages < pages_to_parse:
        print(
            f"WARNING: There are only {actual_pages} available, but you requested {pages_to_parse}")
    else:
        actual_pages = pages_to_parse

    print("Getting image links")

    links_to_download = []

    semaphore = asyncio.Semaphore(value=concurent_downloads)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait(
            [get_elements_on_page(BASE_LINK.format(
                tag, i), download_folder, links_to_download, semaphore) for i in range(1, actual_pages+1)]
        )
    )

    print(f"Got {len(links_to_download)} objects to download, processing")

    with spinner():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.wait(
                [download_file(t, download_folder, semaphore, vebrose,
                               skip_existing) for t in links_to_download]
            )
        )

    print("Done!")


if __name__ == "__main__":
    typer.run(main)
