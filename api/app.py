from flask import Flask, render_template, request

app = Flask(__name__)


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
    if query == "asteroids":
        return "Unknown"
    if "name" in query:
        return "Team"
    if "largest" in query:
        query_words = query.split(" ")
        numbers = []
        for word in query_words:
            if word and word[0].isdigit():
                word = word[:-1]
                numbers.append(int(word))
        return str(max(numbers))
    if "plus" in query:
        query_words = query.split(" ")
        numbers = []
        for word in query_words:
            if word[-1] == "?":
                word = word[:-1]
            if word.isdigit():
                numbers.append(int(word))
        return str(sum(numbers))
    if "multiplied" in query:
        numbers = [int(word) for word in query.split() if word.isdigit()]
        return str(numbers[0] * numbers[1])
    if "primes" in query:
        numbers = [int(word) for word in query.split() if word.isdigit()]
        primes = [num for num in numbers if is_prime(num)]
        return "-".join(map(str, primes))
    if "square and a cube" in query:
        numbers = [int(word) for word in query.split() if word.isdigit()]
        result = [num for num in numbers if is_square_and_cube(num)]
        return "-".join(map(str, result))


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/query/<q>")
def query(q):
    result = process_query(q)
    return result


if __name__ == "__main__":
    app.run(debug=True)
