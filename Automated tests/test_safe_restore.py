import pathlib
import shutil
import tempfile
import unittest
from unittest.mock import patch

import manager
import parser


class TestSafeRestore(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_path = pathlib.Path(self.test_dir)

        self.live_save_path = self.test_path / "LiveSaves"
        self.backup_store_path = self.test_path / "Backups"

        self.live_save_path.mkdir()
        self.backup_store_path.mkdir()

        (self.live_save_path / "file1.txt").write_text("Original Live Content")

        self.backup_name = "test_backup"
        self.specific_backup_path = self.backup_store_path / self.backup_name
        self.specific_backup_path.mkdir()
        (self.specific_backup_path / "file1.txt").write_text("New Backup Content")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("manager.get_local_backup_path")
    @patch("parser.get_save_path")
    def test_restore_success(self, mock_get_save_path, mock_get_backup_path):
        mock_get_save_path.return_value = self.live_save_path
        mock_get_backup_path.return_value = self.backup_store_path

        result = manager.restore_saves(self.backup_name)

        self.assertTrue(result)
        self.assertEqual(
            (self.live_save_path / "file1.txt").read_text(), "New Backup Content"
        )
        temp_backups = list(self.test_path.glob("*_RESTORE_OLD"))
        self.assertEqual(len(temp_backups), 0)

    @patch("manager.get_local_backup_path")
    @patch("parser.get_save_path")
    def test_restore_failure_rollback(self, mock_get_save_path, mock_get_backup_path):
        mock_get_save_path.return_value = self.live_save_path
        mock_get_backup_path.return_value = self.backup_store_path

        real_copytree = shutil.copytree

        def side_effect(src, dst, **kwargs):
            if (
                str(src) == str(self.specific_backup_path)
                and dst.name == "LiveSaves_RESTORING"
            ):
                raise IOError("Simulated Copy Failure")
            return real_copytree(src, dst, **kwargs)

        with patch("shutil.copytree", side_effect=side_effect):
            result = manager.restore_saves(self.backup_name)

        self.assertFalse(result)

        self.assertTrue(self.live_save_path.exists(), "Live save path should exist")
        self.assertEqual(
            (self.live_save_path / "file1.txt").read_text(), "Original Live Content"
        )

        temp_dirs = list(self.test_path.glob("*_RESTORING"))
        self.assertEqual(
            len(temp_dirs), 0, "Staging directory should be cleaned up after failure"
        )


if __name__ == "__main__":
    unittest.main()
