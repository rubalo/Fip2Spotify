from pathlib import Path

import requests

from config import Config

URL = "https://www.playlisteradio.com/fip-radio"


def fetch_tracks_info(result_folder: Path) -> None:
    pages = [
        "",
    ] + ["?page={page_url}".format(page_url=x) for x in range(1, 86)]

    for num, page in enumerate(pages):
        url_page = URL + page

        file = result_folder / f"page-{num}.html"

        if file.exists():
            print(f"Skipping {file}, already exists")
            continue

        r = requests.get(url_page)

        if r.status_code == requests.codes.ok:
            with open(file, "w") as f:
                f.write(r.text)
        else:
            print(f"Error {r.status_code} while fetching {url_page}")


def main() -> None:
    conf = Config()
    fetch_tracks_info(conf.data_folder)


if __name__ == "__main__":
    main()
