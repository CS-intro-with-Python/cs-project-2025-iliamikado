# CS_2024_project

## Description

### Multiplayer Minesweeper

Multiplayer Minesweeper is an online multiplayer version
of the classic Minesweeper, where multiple players play
simultaneously on the same field and compete for the best score
in real time.

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

## Features

* Co-op Play\
Multiple players connect to the same game and open cells on a shared board.
* Real-time\
All player actions are instantly synchronized between clients: opening cells, detonating mines, and updating statistics.
* Player List\
A current list of players with their statistics is displayed to the right of the game board
* Scoring System\
Points are calculated based on your game performance, advancing you on the leaderboard.

## Git
branch main will store the latest stable version

## Success Criteria

* Minesweeper logic
* Multiplayer using web sockets
* Statistics
* Users authorisation
* UI for game field

