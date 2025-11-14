const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");

const cellSize = 32;

let cells = {};

let centerX = 0;
let centerY = 0;
let radius = 10;

function key(x, y) {
    return `${x},${y}`;
}

async function loadAllCells() {
    const res = await fetch("/board");
    console.log(res)
    const data = await res.json();
    console.log(data)

    data.forEach(cell => {
        cells[key(cell.x, cell.y)] = cell;
    });

    drawBoard();
}

async function clickCell(x, y) {
    const res = await fetch("/click", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({x, y})
    });

    const newlyOpened = await res.json();

    newlyOpened.forEach(cell => {
        cells[key(cell.x, cell.y)] = cell;
    });

    drawBoard();
}


function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let vy = -radius; vy <= radius; vy++) {
        for (let vx = -radius; vx <= radius; vx++) {
            let x = centerX + vx;
            let y = centerY + vy;

            const cell = cells[key(x, y)];

            const px = (vx + radius) * cellSize;
            const py = (vy + radius) * cellSize;

            if (!cell || !cell.opened) {
                ctx.fillStyle = "#999";
            } else if (cell.mine) {
                ctx.fillStyle = "red";
            } else {
                ctx.fillStyle = "#ddd";
            }

            ctx.fillRect(px, py, cellSize - 1, cellSize - 1);

            if (cell && cell.opened && !cell.mine && cell.mines_count) {
                ctx.fillStyle = "black";
                ctx.font = "16px sans-serif";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText(cell.mines_count, px + cellSize / 2, py + cellSize / 2);
            }
        }
    }
}

canvas.addEventListener("click", (e) => {
    const rect = canvas.getBoundingClientRect();
    const cx = Math.floor((e.clientX - rect.left) / cellSize) - radius;
    const cy = Math.floor((e.clientY - rect.top) / cellSize) - radius;

    const x = centerX + cx;
    const y = centerY + cy;

    clickCell(x, y);
});

window.addEventListener("keydown", (e) => {
    if (e.key.toLowerCase() === "r") {
        fetch("/reset", {method: "POST"});
        cells = {};
        drawBoard();
    }
});


loadAllCells();
