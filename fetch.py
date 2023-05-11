from pathlib import Path

import requests


def main():
    url = "https://www.playlisteradio.com/fip-radio"

    pages = ["", ] + ["?page={page_url}".format(page_url=x)   for x in range(1, 86)]

    for num, page in enumerate(pages):
        url_page = url + page 

        file = Path(f"data/page-{num}.html")

        if file.exists():
            print(f"Skipping {file}, already exists")
            continue
        
        r = requests.get(url_page)

        if r.status_code == requests.codes.ok:
            with open(file, "w") as f:
                f.write(r.text)
        else:
            print(f"Error {r.status_code} while fetching {url_page}")

if __name__ == '__main__':
    main()