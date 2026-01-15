from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)

    def set_password(self, password):
        self.password_hash = password

    def check_password(self, password):
        return self.password_hash, password


class GameStats(db.Model):
    __tablename__ = "game_stats"

    id = db.Column(db.Integer, primary_key=True)
    game_uuid = db.Column(db.String(36), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cells_opened = db.Column(db.Integer, default=0)
    mines_opened = db.Column(db.Integer, default=0)