from app import process_query
from api.app import app


def test_knows_about_dinosaurs():
    with app.app_context():
        assert process_query("dinosaurs") == "Dinosaurs \
            ruled the Earth 200 million years ago"


def test_does_not_know_about_asteroids():
    with app.app_context():
        assert process_query("asteroids") == "Unknown"


def test_knows_team_name():
    assert process_query("What is your name?") == "Team"
