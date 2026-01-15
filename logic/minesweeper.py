import random
import uuid

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mine = False
        self.opened = False
        self.flag = False
        self.mines_count = 0

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "mine": self.mine,
            "opened": self.opened,
            "flag": self.flag,
            "mines_count": self.mines_count
        }


class Minesweeper:
    def __init__(self, mine_chance=0.15):
        self.mine_chance = mine_chance
        self.cells = {}
        self.initialized = False
        self.uuid = str(uuid.uuid4())

    def _set_cell(self, x, y):
        if (x, y) not in self.cells:
            cell = Cell(x, y)
            cell.mine = random.random() < self.mine_chance
            if not self.initialized:
                cell.mine = False
                self.initialized = True
            self.cells[(x, y)] = cell
        return self.cells[(x, y)]

    def _neighbors(self, x, y):
        neighbors = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                neighbors.append((x + dx, y + dy))
        return neighbors

    def _count_mines(self, x, y):
        return sum(self._set_cell(nx, ny).mine for nx, ny in self._neighbors(x, y))

    def open(self, x, y):
        stack = [(x, y)]
        opened = set()
        while stack:
            cx, cy = stack.pop()
            cell = self._set_cell(cx, cy)
            if cell.opened or cell.flag:
                continue
            cell.opened = True
            cell.mines_count = self._count_mines(cx, cy)
            opened.add(cell)
            if cell.mines_count == 0 and not cell.mine:
                for nx, ny in self._neighbors(cx, cy):
                    if (nx, ny) not in opened:
                        stack.append((nx, ny))
        return list(map(lambda c: c.to_json(), opened))

    def flag(self, x, y):
        cell = self.cells[(x, y)] if (x, y) in self.cells else self._set_cell(x, y)
        if not cell.opened:
            cell.flag = not cell.flag
        return cell.to_json()

    def field(self):
        field = []
        for cell in self.cells.values():
            if cell.opened or cell.flag:
                field.append(cell.to_json())
        return field
