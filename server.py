import os
from flask import Flask, render_template, request, jsonify, session, redirect
from flask_socketio import SocketIO, emit
from logic.minesweeper import Minesweeper
from db.models import db, User
from logger.logger import setup_logging

app = Flask(__name__)
setup_logging(app)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/minesweeper"
)
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


socketio = SocketIO(app, cors_allowed_origins="*")
db.init_app(app)

with app.app_context():
    db.create_all()

game = Minesweeper()

@app.before_request
def log_request():
    app.logger.info(
        "%s %s | IP: %s",
        request.method,
        request.path,
        request.remote_addr
    )

@app.route("/")
def main_page():
    return render_template("game.html", user=session.get("user_login", None))

@app.route("/login")
def login_page():
    return render_template("login.html", user=session.get("user_login", None))

@app.post("/api/register")
def register():
    data = request.get_json()
    login = data.get("login")
    password = data.get("password")

    app.logger.info("Register! Login: %s", login)

    if not login or not password:
        app.logger.info("Registration without login or password")
        return jsonify({"error": "login and password required"}), 400

    if User.query.filter_by(login=login).first():
        app.logger.info("User %s already exist", login)
        return jsonify({"error": "user already exists"}), 400

    try:
        user = User(login=login)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session["user_login"] = user.login
    except Exception:
        app.logger.exception("Failed registration")
        return jsonify({
            "status": "error"
        })


    return jsonify({
        "status": "ok",
        "user": {
            "id": user.id,
            "login": user.login
        }
    })


@app.post("/api/login")
def login_handle():
    data = request.get_json()
    login = data.get("login")
    password = data.get("password")

    app.logger.info("Logining! Login: %s", login)

    if not login or not password:
        app.logger.info("Logining without login or password")
        return jsonify({"error": "login and password required"}), 400

    user = User.query.filter_by(login=login).first()
    if not user or not user.password_hash:
        app.logger.info("Login %s does not exist", login)
        return jsonify({"error": "invalid credentials"}), 401

    if not user.check_password(password):
        app.logger.info("Wrong password for login %s", login)
        return jsonify({"error": "invalid credentials"}), 401

    session["user_id"] = user.id
    session["user_login"] = user.login

    return jsonify({
        "status": "ok",
        "user": {
            "id": user.id,
            "login": user.login
        }
    })

@app.route("/logout")
def logout():
    if "user_id" not in session:
        return "Not authorised", 400
    app.logger.info("User %s logout", session["user_login"])
    session.clear()
    return redirect("/")

@socketio.on("connect")
def on_connect():
    emit("board_redraw", game.field())

@socketio.on("click_cell")
def click_cell(data):
    if "user_id" not in session:
        emit("error", {"error": "Not Authorized"})
        return
    x, y = data["x"], data["y"]

    app.logger.info("%s pressed on %d, %d", session["user_login"], x, y)
    opened = game.open(x, y)
    emit("board_update", opened, broadcast=True)


@socketio.on("flag_cell")
def flag_cell(data):
    if "user_id" not in session:
        emit("error", {"error": "Not Authorized"})
        return
    x, y = data["x"], data["y"]
    app.logger.info("%s put flag on %d, %d", session["user_login"], x, y)
    cell = game.flag(x, y)
    emit("board_update", [cell], broadcast=True)


@socketio.on("reset_game")
def reset_game():
    global game
    game = Minesweeper()
    if "user_login" not in session and session["user_login"] != "iliamikado":
        return
    emit("board_redraw", game.field(), broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
