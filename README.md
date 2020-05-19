# paheal-parser
Async file downloader for paheal r34

Install deps form req.txt and off you go!

```
Usage: parser.py [OPTIONS] TAG # Tag to download images

Options:
  --pages-to-parse # How many pages to download, 10 by default
  --download-videos / --no-download-videos # --download-videos by default
  --skip-existing / --no-skip-existing # --skip-existing by default
  --download-path # If not specified, downloads to ./TAG
  --concurent-downloads # Maximum number of concurrent downloads, 10 by default
  --vebrose / --no-vebrose # Log data currently downloaded in terminal
  ```