from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from dotenv import dotenv_values

from config import Config


def parse_tracks_info(config: Config) -> None:
    song_list = []

    path = Path(config.data_folder)
    result_file = config.tracks_file

    for file in path.glob("page-*.html"):
        with open(file, "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            table = soup.find("table", class_="tbl-result")

            for row in table.find_all("tr"):
                horraire = row.find("td", class_="horaire")
                title = row.find("span", class_="titre")
                artist = row.find("span", class_="artiste")

                if horraire and title and artist:
                    print(horraire.text, title.text, artist.text)
                    song_list.append(
                        {
                            "horaire": horraire.text,
                            "titre": title.text,
                            "artiste": artist.text,
                        },
                    )

    df = pd.DataFrame(song_list)
    df["horaire"] = pd.to_datetime(df["horaire"], format="%d/%m/%Y %H:%M")
    df = df.sort_values("horaire")
    df = df.set_index("horaire")
    df = df.between_time("7:00", "23:59")
    df.to_csv(result_file, sep=";")


if __name__ == "__main__":
    parse_tracks_info(Config())
