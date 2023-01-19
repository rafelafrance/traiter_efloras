import unittest

from tests.setup import test


class TestSmoke(unittest.TestCase):
    def test_smoke_01(self):
        self.assertEqual(
            test("calyx yellow"),
            [
                {"flower_part": "calyx", "trait": "flower_part", "start": 0, "end": 5},
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "calyx",
                    "start": 6,
                    "end": 12,
                },
            ],
        )
