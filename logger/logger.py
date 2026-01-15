import logging

def setup_logging(app):
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # for h in list(root_logger.handlers):
    #     root_logger.removeHandler(h)

    file_handler = logging.FileHandler("app.log", mode='w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    root_logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)

    other_loggers = ["engineio", "socketio", "werkzeug"]
    for name in other_loggers:
        logger = logging.getLogger(name)
        logger.setLevel(logging.WARNING)
        logger.handlers.clear()
        logger.propagate = True

    sql_logger = logging.getLogger("sqlalchemy.engine")
    sql_logger.setLevel(logging.INFO)
    sql_logger.propagate = True

