import unittest
import sys
import os
import pathlib

# Add parent directory to path to import parser
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parser

class TestParser(unittest.TestCase):
    def test_get_save_path(self):
        """
        Test that get_save_path returns a Path object or None, 
        and if it returns a path, it must exist.
        """
        path = parser.get_save_path()
        
        if path is not None:
            self.assertIsInstance(path, pathlib.Path)
            self.assertTrue(path.exists())
            self.assertTrue(path.is_dir())
            print(f"\n[TEST] Save path found at: {path}")
        else:
            print("\n[TEST] Save path not found (this might be expected if the game is not installed or no saves exist).")

if __name__ == '__main__':
    unittest.main()
