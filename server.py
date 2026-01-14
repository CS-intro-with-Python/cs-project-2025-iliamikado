from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from logic.minesweeper import Minesweeper

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(app, cors_allowed_origins="*")

game = Minesweeper()


@app.route("/")
def main_page():
    return render_template("index.html")


@socketio.on("connect")
def on_connect():
    emit("full_board", game.field())


@socketio.on("click_cell")
def click_cell(data):
    x, y = data["x"], data["y"]
    opened = game.open(x, y)
    emit("cells_update", opened, broadcast=True)


@socketio.on("flag_cell")
def flag_cell(data):
    x, y = data["x"], data["y"]
    cell = game.flag(x, y)
    emit("cells_update", [cell], broadcast=True)


@socketio.on("reset_game")
def reset_game():
    global game
    game = Minesweeper()
    emit("full_board", game.field(), broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
