import json
import os
import pathlib
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import manager
import parser


class TestManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.mock_save_path = pathlib.Path(self.test_dir) / "mock_saves"
        self.mock_save_path.mkdir()
        (self.mock_save_path / "save1.dat").write_text("dummy data")

        self.get_save_path_patcher = patch.object(
            parser, "get_save_path", return_value=self.mock_save_path
        )
        self.get_save_path_patcher.start()

        self.config_path = manager.get_config_path()
        self.original_config = None
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                self.original_config = f.read()
            os.remove(self.config_path)

    def tearDown(self):
        self.get_save_path_patcher.stop()
        shutil.rmtree(self.test_dir)

        if self.original_config:
            with open(self.config_path, "w") as f:
                f.write(self.original_config)
        elif self.config_path.exists():
            os.remove(self.config_path)

    def test_get_local_backup_path_default(self):
        if self.config_path.exists():
            os.remove(self.config_path)

        path = manager.get_local_backup_path()
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "REPO Local backup")

    def test_set_local_backup_path(self):
        custom_dir = pathlib.Path(self.test_dir) / "custom_backups"
        manager.set_local_backup_path(custom_dir)

        self.assertTrue(self.config_path.exists())

        path = manager.get_local_backup_path()
        self.assertEqual(path, custom_dir)
        self.assertTrue(path.exists())

    def test_total_backup(self):
        backup_name = "test_backup_1"
        success = manager.total_backup(backup_name)
        self.assertTrue(success)

        backup_path = manager.get_local_backup_path() / backup_name
        self.assertTrue(backup_path.exists())
        self.assertTrue((backup_path / "save1.dat").exists())

        shutil.rmtree(backup_path)

    def test_restore_saves(self):
        backup_name = "test_restore_1"
        manager.total_backup(backup_name)

        (self.mock_save_path / "save1.dat").write_text("modified data")

        success = manager.restore_saves(backup_name)
        self.assertTrue(success)

        content = (self.mock_save_path / "save1.dat").read_text()
        self.assertEqual(content, "dummy data")

        shutil.rmtree(manager.get_local_backup_path() / backup_name)

    def test_set_backup_state(self):
        dummy_folder = pathlib.Path(self.test_dir) / "my_save"
        dummy_folder.mkdir()

        new_path = manager.set_backup_state(dummy_folder, active=False)
        self.assertTrue(new_path.name.endswith("_backup"))
        self.assertTrue(new_path.exists())
        self.assertFalse(dummy_folder.exists())

        restored_path = manager.set_backup_state(new_path, active=True)
        self.assertFalse(restored_path.name.endswith("_backup"))
        self.assertTrue(restored_path.exists())
        self.assertFalse(new_path.exists())

        path_again = manager.set_backup_state(restored_path, active=False)
        path_again_2 = manager.set_backup_state(path_again, active=False)
        self.assertEqual(path_again, path_again_2)
        self.assertTrue(path_again.name.endswith("_backup"))


if __name__ == "__main__":
    unittest.main()
