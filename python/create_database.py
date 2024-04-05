"""
This script downloads the files and creates the database that will be used
by the rest of the code.
"""

from PIL import Image
import os
import time
import urllib.parse
import urllib.request

import requests

# Constants
DATABASE_DIRECTORY = "../database"
IMAGE_SIZE = (342, 513)
TIMEOUT = 5
TOP_MOVIES_URL = "https://raw.githubusercontent.com/kalilurrahman/" + \
                     "BoxOfficeData/main/boxofficemojoustop1000.tsv"
TOP_MOVIES_FILENAME = "boxofficemojoustop1000.tsv"


def create_directory(directory):
    """
    If the database directory does not exist, create it.
    Then use it as the default database.

    param directory to create.
    """
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass

    os.chdir(directory)


def download_top_movies(url, filename_top_movies):
    """
    Download the top movies from GitHub.

    :param url: The URL to download from.
    :param filename_top_movies: Where to write the file.
    """
    f = requests.get(url, timeout=TIMEOUT)

    with open(filename_top_movies, "w", encoding="utf-8") as outfile:
        outfile.write(f.text)


def post_process_title(title):
    """Box office mojo gives a different title for one film than
       TMBD."""
    if title == "Three Men And a Baby":
        return "3 Men and a Baby"
    elif title == "9 to 5":
        return "Nine to Five"
    else:
        return title


def list_movies(filename_top_movies):
    """
    Given a file in .tsv format, output just the names of movies.

    :param filename_top_movies:
    :return: A list of movies.
    """
    result = []

    with open(filename_top_movies, "r", encoding="utf-8") as infile:
        # Skip the header
        infile.readline()

        tsv = infile.readline()
        while tsv != "":
            title = tsv.split("\t")[1]
            title = post_process_title(title)
            result.append(title)
            tsv = infile.readline()

    return result


def call_api(endpoint):
    """This function calls the main tmdb database API."""
    url = f"https://api.themoviedb.org/3/{endpoint}"

    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {os.environ["TMDB_READ_ACCESS_TOKEN"]}'
    }

    response = requests.get(url, headers=headers)

    return response.json()


def get_configuration():
    """Return the list of configurations. This is important for
       figuring out the address to get images from."""
    return call_api("configuration")


def convert_title_to_poster_path(title):
    """This looks up the path for the movie poster."""
    title_quoted = urllib.parse.quote(title)
    response = call_api(f"search/movie?query="
                        f"{title_quoted}&include_adult=false&language"
                        f"=en-US&page=1")
    if "results" in response and len(response["results"]) > 0:
        return response["results"][0]["poster_path"]
    else:
        return None


def download_poster_from_path(config, poster_path, filename):
    """Given a poster path, download the poster into the default
       directory (which was set in create_directory)."""
    if poster_path is not None:
        url = f'{config["images"]["base_url"]}w342{poster_path}'
        urllib.request.urlretrieve(url, filename)
    else:
        print(f"ERROR: poster_path was not set for {filename}. Look up why!")


def fix_filename(filename):
    """The movie Fahrenheit 9/11 contains a slash, which would be a directory
       in Unix. Fix it."""
    return filename.replace("/", "-")


def resize_image(filename):
    """Ensure that all images are the same size."""
    im = Image.open(filename)
    im = im.resize(IMAGE_SIZE)
    im.save(filename)


def main():
    """Download and fix all of the """
    create_directory(DATABASE_DIRECTORY)
    download_top_movies(TOP_MOVIES_URL, TOP_MOVIES_FILENAME)
    config = get_configuration()

    titles = list_movies(TOP_MOVIES_FILENAME)
    for title in titles:
        poster_path = convert_title_to_poster_path(title)
        filename = fix_filename(f"{title}.jpg")
        download_poster_from_path(config, poster_path, filename)
        print(f"Finished: {title}")
        time.sleep(5)

    for root, dirs, filenames in os.walk(DATABASE_DIRECTORY):
        for filename in filenames:
            if filename.endswith("jpg"):
                resize_image(filename)


if __name__ == "__main__":
    if "TMDB_READ_ACCESS_TOKEN" not in os.environ:
        print("Please set the TMBD_READ_ACCESS_TOKEN in order to download "
              "the movie posters. See README.txt for more details.")
    else:
        main()
