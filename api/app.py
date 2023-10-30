from flask import Flask, render_template, request

app = Flask(__name__)


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
            if word[0].isdigit():
                if word[-1] == "?":
                    word = word[:-1]
                    numbers.append(int(word))
        if numbers:
            return str(sum(numbers))
        else:
            return "No numbers found in the query"


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
