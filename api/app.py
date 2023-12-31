from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import requests

app = Flask(__name__)


def extract_numbers_from_query(query):
    query_words = query.split(" ")
    numbers = []

    for word in query_words:
        cleaned_word = "".join(filter(str.isdigit, word))
        if cleaned_word:
            numbers.append(int(cleaned_word))

    return numbers


def arithmetic_operation(query, operator):
    numbers = extract_numbers_from_query(query)

    if operator == "plus":
        return str(numbers[0] + numbers[1])
    elif operator == "minus":
        return str(numbers[0] - numbers[1])
    elif operator == "multiplied":
        return str(numbers[0] * numbers[1])
    elif operator == "largest":
        return str(max(numbers))
    elif operator == "primes":
        for num in numbers:
            if is_prime(num):
                return str(num)
        return "No primes found"
    elif operator == "a square and a cube":
        for num in numbers:
            if is_square_and_cube(num):
                return str(num)
        return "No numbers that are both square and cube found"
    else:
        return "Unknown operation"


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_square_and_cube(n):
    root = int(n**0.5)
    if root * root == n:
        cube_root = round(n ** (1 / 3))
        if cube_root * cube_root * cube_root == n:
            return True
    return False


def process_query(query):
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"

    elif query == "asteroids":
        return "Unknown"

    elif "name" in query:
        return "team"

    elif "plus" in query:
        return arithmetic_operation(query, "plus")

    elif "minus" in query:
        return arithmetic_operation(query, "minus")

    elif "multiplied" in query:
        return arithmetic_operation(query, "multiplied")

    elif "largest" in query:
        return arithmetic_operation(query, "largest")

    elif "primes" in query:
        return arithmetic_operation(query, "primes")

    elif "a square and a cube" in query:
        return arithmetic_operation(query, "a square and a cube")

    else:
        return "Invalid query"


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/github_form", methods=["GET", "POST"])
def github_form():
    if request.method == "POST":
        username = request.form.get("username")
        return redirect(url_for('hello_github_user', username=username))
    return render_template("github_username.html")


@app.route("/hello_github_user", methods=["GET"])
def hello_github_user():
    username = request.args.get("username")
    search_term = request.args.get("search_term", "").lower()
    response = requests.get(f"https://api.github.com/users/{username}/repos")
    repos_data = []
    language_counts = {}

    if response.status_code == 200:
        for repo in response.json():
            updated_at = datetime.strptime(
                repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
            ).strftime("%Y-%m-%d %H:%M:%S")

            commits_url = repo["commits_url"].split("{")[0]
            commits_response = requests.get(commits_url)

            if commits_response.status_code == 200:
                latest_commit = commits_response.json()[0]
                commit_author_date = latest_commit["commit"]["author"]["date"]
                formatted_commit_date = datetime.strptime(
                    commit_author_date, "%Y-%m-%dT%H:%M:%SZ"
                ).strftime("%Y-%m-%d %H:%M:%S")

                commit_author_name = latest_commit["commit"]["author"]["name"]
                commit_message = latest_commit["commit"]["message"]
                commit_sha = latest_commit["sha"]

                commit_data = {
                    "name": repo["name"],
                    "updated_at": updated_at,
                    "latest_commit_hash": commit_sha,
                    "latest_commit_author": commit_author_name,
                    "latest_commit_date": formatted_commit_date,
                    "latest_commit_message": commit_message,
                }
                repos_data.append(commit_data)

                language = repo.get("language", None)
                if language:
                    current_count = language_counts.get(language, 0)
                    language_counts[language] = current_count + 1

    if search_term:
        repos_data = [
            repo for repo in repos_data
            if search_term.lower() in repo["name"].lower()
        ]

    languages = list(language_counts.keys())
    counts = list(language_counts.values())

    return render_template(
        "hello_github_user.html",
        username=username,
        search_term=search_term,
        repos_data=repos_data,
        languages=languages,
        counts=counts,
    )


@app.route("/query/<q>")
def query(q):
    result = process_query(q)
    return result


if __name__ == "__main__":
    app.run(debug=True)
