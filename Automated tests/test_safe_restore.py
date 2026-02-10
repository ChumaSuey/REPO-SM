import unittest
import shutil
import tempfile
import pathlib
import os
from unittest.mock import patch, MagicMock

# Import the module under test
import manager
import parser

class TestSafeRestore(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the test
        self.test_dir = tempfile.mkdtemp()
        self.test_path = pathlib.Path(self.test_dir)
        
        # Define paths for "live" saves and "backups"
        self.live_save_path = self.test_path / "LiveSaves"
        self.backup_store_path = self.test_path / "Backups"
        
        # Create directories
        self.live_save_path.mkdir()
        self.backup_store_path.mkdir()
        
        # Create "Live" content
        (self.live_save_path / "file1.txt").write_text("Original Live Content")
        
        # Create a backup
        self.backup_name = "test_backup"
        self.specific_backup_path = self.backup_store_path / self.backup_name
        self.specific_backup_path.mkdir()
        (self.specific_backup_path / "file1.txt").write_text("New Backup Content")

    def tearDown(self):
        # Clean up temp directory
        shutil.rmtree(self.test_dir)

    @patch('manager.get_local_backup_path')
    @patch('parser.get_save_path')
    def test_restore_success(self, mock_get_save_path, mock_get_backup_path):
        """Test a normal, successful restore."""
        mock_get_save_path.return_value = self.live_save_path
        mock_get_backup_path.return_value = self.backup_store_path
        
        # Perform restore
        result = manager.restore_saves(self.backup_name)
        
        self.assertTrue(result)
        # Check if content matches backup
        self.assertEqual((self.live_save_path / "file1.txt").read_text(), "New Backup Content")
        # Check if temp backup is gone
        temp_backups = list(self.test_path.glob("*_TEMP_RESTORE_BACKUP"))
        self.assertEqual(len(temp_backups), 0)

    @patch('manager.get_local_backup_path')
    @patch('parser.get_save_path')
    def test_restore_failure_rollback(self, mock_get_save_path, mock_get_backup_path):
        """Test that failure during copy restores the original state."""
        mock_get_save_path.return_value = self.live_save_path
        mock_get_backup_path.return_value = self.backup_store_path
        
        # We need to mock shutil.copytree to fail ONLY when copying the backup to live
        # But allow it to work for creating the temp backup.
        # This is tricky because manager.restore_saves calls copytree twice (or 3 times if rollback).
        
        real_copytree = shutil.copytree
        
        def side_effect(src, dst, **kwargs):
            # Check if we are copying FROM backup TO live
            # src will be .../Backups/test_backup
            # dst will be .../LiveSaves
            if str(src) == str(self.specific_backup_path) and str(dst) == str(self.live_save_path):
                raise IOError("Simulated Copy Failure")
            return real_copytree(src, dst, **kwargs)
            
        with patch('shutil.copytree', side_effect=side_effect):
            result = manager.restore_saves(self.backup_name)
            
        self.assertFalse(result)
        
        # VERIFY ROLLBACK: Content should be "Original Live Content"
        self.assertTrue(self.live_save_path.exists(), "Live save path should exist")
        self.assertEqual((self.live_save_path / "file1.txt").read_text(), "Original Live Content")
        
        # Verify temp backup is cleaned up
        temp_backups = list(self.test_path.glob("*_TEMP_RESTORE_BACKUP"))
        self.assertEqual(len(temp_backups), 0, "Temp backup should be removed after rollback")

if __name__ == '__main__':
    unittest.main()
