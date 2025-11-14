from flask import Flask, render_template, jsonify, request
from logic.minesweeper import Minesweeper

app = Flask(__name__)
game = Minesweeper()

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/')
def main_page():
    return render_template('index.html')

@app.get("/board")
def get_board():
    return jsonify(game.field())

@app.post("/click")
def click():
    data = request.get_json()
    x, y = data["x"], data["y"]
    return jsonify(game.open(x, y))

@app.post("/reset")
def reset():
    global game
    game = Minesweeper()
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0')