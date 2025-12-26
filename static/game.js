const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");

const cellSize = 32;

let cells = {};

let centerX = 0;
let centerY = 0;
let radius = 10;

let isDragging = false;
let dragMoved = false;
let lastMouseX = 0;
let lastMouseY = 0;

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
    console.log(x, y)
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

async function flagCell(x, y) {
    console.log(x, y)
    const res = await fetch("/flag", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({x, y})
    });

    const cell = await res.json();
    cells[key(cell.x, cell.y)] = cell;

    drawBoard();
}



function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const halfCols = Math.ceil(canvas.width / cellSize / 2);
    const halfRows = Math.ceil(canvas.height / cellSize / 2);

    for (let vy = -halfRows; vy <= halfRows; vy++) {
        for (let vx = -halfCols; vx <= halfCols; vx++) {

            const x = Math.floor(centerX + vx);
            const y = Math.floor(centerY + vy);

            const cell = cells[key(x, y)];

            const px = (vx + halfCols) * cellSize;
            const py = (vy + halfRows) * cellSize;

            if (!cell || !cell.opened) {
                ctx.fillStyle = "#999";
            } else if (cell.mine) {
                ctx.fillStyle = "red";
            } else {
                ctx.fillStyle = "#ddd";
            }

            ctx.fillRect(px, py, cellSize - 1, cellSize - 1);

            if (cell && cell.flag && !cell.opened) {
                ctx.fillStyle = "red";
                ctx.font = "20px sans-serif";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText("🚩", px + cellSize / 2, py + cellSize / 2);
            }

            if (cell && cell.opened && !cell.mine && cell.mines_count > 0) {
                ctx.fillStyle = "black";
                ctx.font = "16px sans-serif";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText(
                    cell.mines_count,
                    px + cellSize / 2,
                    py + cellSize / 2
                );
            }
        }
    }
}

canvas.addEventListener("contextmenu", (e) => {
    e.preventDefault();
});


canvas.addEventListener("click", (e) => {
    if (dragMoved) return;

    const rect = canvas.getBoundingClientRect();

    const halfCols = Math.floor(canvas.width / cellSize / 2);
    const halfRows = Math.floor(canvas.height / cellSize / 2);

    const vx = Math.floor((e.clientX - rect.left) / cellSize) - halfCols;
    const vy = Math.floor((e.clientY - rect.top) / cellSize) - halfRows;

    const x = Math.floor(centerX + vx) - 1;
    const y = Math.floor(centerY + vy) - 1;

    clickCell(x, y);
});

canvas.addEventListener("mousedown", (e) => {
    if (e.button !== 2) return;

    const rect = canvas.getBoundingClientRect();

    const halfCols = Math.floor(canvas.width / cellSize / 2);
    const halfRows = Math.floor(canvas.height / cellSize / 2);

    const vx = Math.floor((e.clientX - rect.left) / cellSize) - halfCols;
    const vy = Math.floor((e.clientY - rect.top) / cellSize) - halfRows;

    const x = Math.floor(centerX + vx) - 1;
    const y = Math.floor(centerY + vy) - 1;

    flagCell(x, y);
});



window.addEventListener("keydown", (e) => {
    if (e.key.toLowerCase() === "r") {
        fetch("/reset", {method: "POST"});
        cells = {};
        drawBoard();
    }
});

loadAllCells();

function resizeCanvas() {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    drawBoard();
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();

canvas.addEventListener("mousedown", (e) => {
    dragMoved = false;
    isDragging = (e.button === 0);

    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
});


window.addEventListener("mouseup", () => {
    isDragging = false;
});

window.addEventListener("mousemove", (e) => {
    if (!isDragging) return;

    const dx = e.clientX - lastMouseX;
    const dy = e.clientY - lastMouseY;

    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
        dragMoved = true;
    }

    lastMouseX = e.clientX;
    lastMouseY = e.clientY;

    centerX -= dx / cellSize;
    centerY -= dy / cellSize;

    drawBoard();
});