import unittest
import sys
import os
import shutil
import pathlib
import tempfile
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import manager
import parser

class TestManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to act as the "REPO save folder"
        self.test_dir = tempfile.mkdtemp()
        self.mock_save_path = pathlib.Path(self.test_dir) / "mock_saves"
        self.mock_save_path.mkdir()
        
        # Create some dummy files in the mock save folder
        (self.mock_save_path / "save1.dat").write_text("dummy data")
        
        # Mock parser.get_save_path to return our temp folder
        self.original_get_save_path = parser.get_save_path
        parser.get_save_path = lambda: self.mock_save_path
        
        # Backup existing config if any
        self.config_path = manager.get_config_path()
        self.original_config = None
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.original_config = f.read()
            os.remove(self.config_path)

    def tearDown(self):
        # Restore original function
        parser.get_save_path = self.original_get_save_path
        # Clean up temp dir
        shutil.rmtree(self.test_dir)
        
        # Restore config
        if self.original_config:
            with open(self.config_path, 'w') as f:
                f.write(self.original_config)
        elif self.config_path.exists():
            os.remove(self.config_path)
            
        # Clean up default local backups created during test if needed
        # (We might want to be careful here, but for now relying on temp dirs for custom paths)

    def test_get_local_backup_path_default(self):
        # Ensure no config exists
        if self.config_path.exists():
            os.remove(self.config_path)
            
        path = manager.get_local_backup_path()
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "REPO Local backup")

    def test_set_local_backup_path(self):
        custom_dir = pathlib.Path(self.test_dir) / "custom_backups"
        manager.set_local_backup_path(custom_dir)
        
        # Check if config file was created
        self.assertTrue(self.config_path.exists())
        
        # Check if get_local_backup_path returns new path
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
        
        # Clean up
        shutil.rmtree(backup_path)

    def test_restore_saves(self):
        # First create a backup
        backup_name = "test_restore_1"
        manager.total_backup(backup_name)
        
        # Modify the "live" save
        (self.mock_save_path / "save1.dat").write_text("modified data")
        
        # Restore
        success = manager.restore_saves(backup_name)
        self.assertTrue(success)
        
        # Check if content is back to original
        content = (self.mock_save_path / "save1.dat").read_text()
        self.assertEqual(content, "dummy data")
        
        # Clean up
        shutil.rmtree(manager.get_local_backup_path() / backup_name)

    def test_set_backup_state(self):
        # Create a dummy folder
        dummy_folder = pathlib.Path(self.test_dir) / "my_save"
        dummy_folder.mkdir()
        
        # Test: Disable (Add _backup)
        new_path = manager.set_backup_state(dummy_folder, active=False)
        self.assertTrue(new_path.name.endswith("_backup"))
        self.assertTrue(new_path.exists())
        self.assertFalse(dummy_folder.exists()) # Old path shouldn't exist
        
        # Test: Enable (Remove _backup)
        restored_path = manager.set_backup_state(new_path, active=True)
        self.assertFalse(restored_path.name.endswith("_backup"))
        self.assertTrue(restored_path.exists())
        self.assertFalse(new_path.exists())
        
        # Test: Idempotency (Disable when already disabled)
        path_again = manager.set_backup_state(restored_path, active=False)
        path_again_2 = manager.set_backup_state(path_again, active=False)
        self.assertEqual(path_again, path_again_2)
        self.assertTrue(path_again.name.endswith("_backup"))

if __name__ == '__main__':
    unittest.main()
