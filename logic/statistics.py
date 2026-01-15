from db.models import db, GameStats, User

def opened_cells(user_id, count, game_uuid):
    try:
        stats = db.session.query(GameStats).filter_by(user_id=user_id, game_uuid=game_uuid).first()
        if not stats:
            stats = GameStats(
                game_uuid=game_uuid,
                user_id=user_id,
                cells_opened=count,
                mines_opened=0,
            )
            db.session.add(stats)
        else:
            stats.cells_opened += count

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def opened_mine(user_id, game_uuid):
    try:
        stats = db.session.query(GameStats).filter_by(user_id=user_id, game_uuid=game_uuid).first()
        if not stats:
            stats = GameStats(
                game_uuid=game_uuid,
                user_id=user_id,
                cells_opened=0,
                mines_opened=1,
            )
            db.session.add(stats)
        else:
            stats.mines_opened += 1

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def get_users(game_uuid):
    results = (
        db.session.query(
            User.login,
            GameStats.cells_opened,
            GameStats.mines_opened
        )
        .join(User, User.id == GameStats.user_id)
        .filter(GameStats.game_uuid == game_uuid)
        .all()
    )

    users = []
    for login, cells_opened, mines_opened in results:
        users.append({
            "login": login,
            "opened_cells": cells_opened,
            "opened_mines": mines_opened,
            "score": cells_opened - mines_opened * 1000
        })

    users.sort(key=lambda u: u["score"], reverse=True)
    return users