from app import process_query


def test_knows_about_dinosaurs():
    result = process_query("dinosaurs")
    expected = "Dinosaurs ruled the Earth 200 million years ago"
    assert result == expected


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_knows_team_name():
    assert process_query("What is your name?") == "Team"


def test_plus():
    assert process_query("What is 90 plus 32?") == "122"
