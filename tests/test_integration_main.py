import unittest
from unittest.mock import patch, mock_open, MagicMock
import subprocess
import os
from io import StringIO
import sys
from sdesk.main import main, get_exclusion_set, update_exclusion_list, list_snap_packages, check_desktop_files, create_desktop_file, backup_desktop_files, restore_desktop_files, interactive_mode

class TestIntegration(unittest.TestCase):

    @patch.dict(os.environ, {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"})
    @patch('subprocess.run')
    @patch('os.path.exists', side_effect=lambda path: False)
    @patch('builtins.open', new_callable=mock_open, read_data='pkg1\npkg2\n')
    def test_integration_write_all(self, mock_file, mock_exists, mock_run):
        # Simulate the output of 'snap list'
        mock_run.return_value.stdout = 'Name   Version   Rev    Tracking       Publisher   Notes\npkg1 1.0\npkg2 2.0\npkg3 3.0\n'

        # Capture the output of the print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Simulate command-line arguments
        test_args = ['main.py', '--write=all']
        with patch('sys.argv', test_args):
            main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Check that subprocess.run was called correctly
        mock_run.assert_called_once_with(['snap', 'list'], stdout=subprocess.PIPE, text=True)

        # Check that create_desktop_file was called for pkg3 only since others are excluded
        mock_file().write.assert_called_once_with(
            "[Desktop Entry]\nType=Application\nName=pkg3\nExec=snap run pkg3\nIcon=pkg3\n"
        )

        # Check print output
        output_value = captured_output.getvalue()
        expected_output = "Created .desktop file for pkg3"
        self.assertIn(expected_output, output_value)

    @patch('gettext.gettext', lambda s: s)
    @patch('gettext.dgettext', lambda domain, message: message)
    @patch('builtins.input', side_effect=['a', 'pkg4', 'q'])
    @patch('sdesk.main.get_exclusion_set', return_value={'pkg1', 'pkg2'})
    def test_interactive_mode_add(self, mock_get_exclusion_set, mock_input):
        # Capture the output of the print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Simulate command-line arguments
        test_args = ['main.py', '--interactive']
        with patch('sys.argv', test_args):
            with patch('builtins.open', mock_open(read_data='pkg1\npkg2\n')):
                interactive_mode()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Expected calls in the interactive mode
        expected_calls = [
            "Interactive mode: manage your exclusion list",
            "Current exclusion list: {'pkg1', 'pkg2'}",
            "Options: [a]dd, [r]emove, [q]uit",
            "Current exclusion list: {'pkg4', 'pkg1', 'pkg2'}",
            "Options: [a]dd, [r]emove, [q]uit"
        ]

        # Capture the print output
        actual_calls = captured_output.getvalue().strip().split('\n')

        for expected in expected_calls:
            self.assertIn(expected, actual_calls)

    @patch('sdesk.main.backup_desktop_files')
    @patch('sdesk.main.restore_desktop_files')
    def test_backup_restore(self, mock_restore, mock_backup):
        # Simulate command-line arguments for backup
        test_args_backup = ['main.py', '--backup']
        with patch('sys.argv', test_args_backup):
            main()
        mock_backup.assert_called_once()

        # Simulate command-line arguments for restore
        test_args_restore = ['main.py', '--restore']
        with patch('sys.argv', test_args_restore):
            main()
        mock_restore.assert_called_once()

if __name__ == '__main__':
    unittest.main()
