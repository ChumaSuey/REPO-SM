import pathlib
import unittest

import parser


class TestParser(unittest.TestCase):
    def test_get_save_path(self):
        path = parser.get_save_path()

        if path is not None:
            self.assertIsInstance(path, pathlib.Path)
            self.assertTrue(path.exists())
            self.assertTrue(path.is_dir())
            print(f"\n[TEST] Save path found at: {path}")
        else:
            print(
                "\n[TEST] Save path not found "
                "(expected if the game is not installed or has no saves)."
            )

    def test_get_default_save_path(self):
        path = parser.get_default_save_path()
        self.assertIsInstance(path, pathlib.Path)


if __name__ == "__main__":
    unittest.main()
