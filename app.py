from flask import Flask, request, session, flash, redirect, render_template
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "crow"

boggle_game = Boggle()

@app.route('/')
def homepage():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    num_of_trys = session.get("num_of_trys", 0)

    return render_template("home.html", board=board, highscore=highscore, num_of_trys=num_of_trys)

@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
