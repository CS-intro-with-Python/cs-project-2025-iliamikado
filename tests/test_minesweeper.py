import unittest
from logic.minesweeper import Minesweeper, Cell


class TestCell(unittest.TestCase):

    def test_initial_state(self):
        cell = Cell(1, 2)
        self.assertEqual(cell.x, 1)
        self.assertEqual(cell.y, 2)
        self.assertFalse(cell.mine)
        self.assertFalse(cell.opened)
        self.assertFalse(cell.flag)
        self.assertEqual(cell.mines_count, 0)

    def test_to_json(self):
        cell = Cell(0, 0)
        cell.mine = True
        cell.opened = True
        cell.flag = False
        cell.mines_count = 3

        self.assertEqual(cell.to_json(), {
            "x": 0,
            "y": 0,
            "mine": True,
            "opened": True,
            "flag": False,
            "mines_count": 3
        })


class TestMinesweeper(unittest.TestCase):

    def test_flag_toggle(self):
        game = Minesweeper()
        cell = game.flag(1, 1)
        self.assertTrue(cell["flag"])

        cell = game.flag(1, 1)
        self.assertFalse(cell["flag"])

    def test_flag_on_opened_cell_does_nothing(self):
        game = Minesweeper()
        game.open(0, 0)

        cell = game.flag(0, 0)
        self.assertFalse(cell["flag"])

    def test_open_opens_cell(self):
        game = Minesweeper()
        opened = game.open(2, 2)

        self.assertTrue(any(
            c["x"] == 2 and c["y"] == 2 for c in opened
        ))

    def test_open_propagates_without_mines(self):
        game = Minesweeper()
        opened = game.open(0, 0)

        self.assertGreater(len(opened), 0)

    def test_open_does_not_open_flagged_cell(self):
        game = Minesweeper()
        game.flag(0, 0)

        opened = game.open(0, 0)

        self.assertEqual(len(opened), 0)

    def test_field_returns_only_opened_or_flagged(self):
        game = Minesweeper()
        game.flag(1, 1)
        game.open(0, 0)

        field = game.field()

        for cell in field:
            self.assertTrue(cell["opened"] or cell["flag"])

    def test_uuid_unique(self):
        g1 = Minesweeper()
        g2 = Minesweeper()

        self.assertNotEqual(g1.uuid, g2.uuid)

if __name__ == "__main__":
    unittest.main()
