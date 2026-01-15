# CS_2024_project

## Description

### Multiplayer Minesweeper

Multiplayer Minesweeper is an online multiplayer version
of the classic Minesweeper, where multiple players play
simultaneously on the same field and compete for the best score
in real time.

## Features

* Co-op Play\
Multiple players connect to the same game and open cells on a shared board.
* Real-time\
All player actions are instantly synchronized between clients: opening cells, detonating mines, and updating statistics.
* Player List\
A current list of players with their statistics is displayed to the right of the game board
* Scoring System\
Points are calculated based on your game performance, advancing you on the leaderboard.


## Setup and run

Build container:
```
docker compose build
```

Run container:
```
docker compose up
```

## Requirements
requests\
Flask~=3.1.2\
flask-socketio\
eventlet\
flask-sqlalchemy\
psycopg2-binary\

Can be installed via
```
pip install requirements.txt
```

Not required if you launch using docker.

## Tests
### Unit tests
```
python -m unittest
```

### Integration tests
(firstly launch app)
```
python client.py
```

## Logs
Logs located in root directory, file app.log

## Git
branch main will store the latest stable version

## Success Criteria

* Minesweeper logic
* Multiplayer using web sockets
* Statistics
* Users authorisation
* UI for game field

## Used technologies

### Backend

* Python 3.11 — server programming language.
* Flask — web framework for routing, processing HTTP requests, and managing sessions.
* Flask-SocketIO — WebSocket implementation for real-time event exchange (game board, players).
* SQLAlchemy + Flask-SQLAlchemy — ORM for working with PostgreSQL, storing users and statistics.
* PostgreSQL — database for storing users and statistics.

### Frontend

* HTML / CSS / JS — page markup, styling, and event handling.
* WebSockets (Socket.IO) — updating the game board and player list in real time.

### DevOps / Deployment

* Docker + Docker Compose — application and database containerization.
* GitHub Actions — CI/CD for building the container, bringing up the server, and running integration tests.
* wait-for-it — waiting for the database to be ready before starting the server.

### Additional Tools

* UUID — generating unique identifiers for games.
* Logging — logging HTTP requests, errors, and player actions.
* unittest — a module for unit testing game logic.
* Swagger — REST API documentation (and description of WebSocket events).
