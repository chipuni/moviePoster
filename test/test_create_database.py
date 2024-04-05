from create_database import *


def test_list_movies():
    """Use a simpler file to check that it reads correctly."""
    top5 = list_movies("data/test_top5.tsv")
    assert(top5 == ["Star Wars: Episode VII - The Force Awakens",
                    "Avengers: Endgame",
                    "Spider-Man: No Way Home",
                    "Avatar",
                    "Black Panther"])