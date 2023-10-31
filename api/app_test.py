from app import process_query


def test_knows_about_dinosaurs():
    result = process_query("dinosaurs")
    expected = "Dinosaurs ruled the Earth 200 million years ago"
    assert result == expected


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_knows_team_name():
    assert process_query("What is your name?") == "team"


def test_plus():
    assert process_query("What is 90 plus 32?") == "122"


def test_minus():
    assert process_query("What is 90 minus 32?") == "58"


def test_multiplied():
    assert process_query("What is 8 multiplied by 6?") == "48"


def test_largest():
    query = "Which of the following numbers is the largest: 96, 27, 26?"
    assert process_query(query) == "96"


def test_prime():
    query = "Which of the following numbers are primes: 46, 33, 97, 60, 88?"
    assert process_query(query) == "97"


def test_square_and_cube():
    query = (
        "Which of the following numbers is both a square and a cube: "
        "45, 27, 64?"
    )
    assert process_query(query) == "64"
