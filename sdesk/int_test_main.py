import unittest
from unittest.mock import patch, mock_open
import subprocess
import os
from io import StringIO
import sys

# Assuming the script is named 'main.py'. Change 'main' to your script name if different.
from main import main

class TestIntegration(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='pkg1\npkg2\n')
    @patch('subprocess.run')
    @patch('os.path.exists')
    def test_integration_write_all(self, mock_exists, mock_run, mock_file):
        # Simulate the output of 'snap list'
        mock_run.return_value.stdout = 'Name   Version   Rev    Tracking       Publisher   Notes\npkg1 1.0\npkg2 2.0\npkg3 3.0\n'
        # Simulate that no .desktop files exist
        mock_exists.side_effect = lambda path: False

        # Capture the output of the print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Simulate command-line arguments
        test_args = ['main.py', '--write=all']
        with patch('sys.argv', test_args):
            main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Print captured output for debugging
        print("Captured Output:", captured_output.getvalue())

        # Check that subprocess.run was called correctly
        mock_run.assert_called_once_with(['snap', 'list'], stdout=subprocess.PIPE, text=True)
        
        # Check that create_desktop_file was called for each package
        expected_writes = [
            "[Desktop Entry]\nType=Application\nName=pkg1\nExec=snap run pkg1\nIcon=pkg1\n",
            "[Desktop Entry]\nType=Application\nName=pkg2\nExec=snap run pkg2\nIcon=pkg2\n",
            "[Desktop Entry]\nType=Application\nName=pkg3\nExec=snap run pkg3\nIcon=pkg3\n"
        ]
        for write in expected_writes:
            mock_file().write.assert_any_call(write)

        # Check print output
        captured_output.seek(0)
        output_lines = captured_output.readlines()
        assert "Created .desktop file for pkg1" in output_lines
        assert "Created .desktop file for pkg2" in output_lines
        assert "Created .desktop file for pkg3" in output_lines

    @patch('builtins.open', new_callable=mock_open, read_data='pkg1\npkg2\n')
    @patch('subprocess.run')
    @patch('os.path.exists')
    def test_integration_exclude_and_write(self, mock_exists, mock_run, mock_file):
        # Simulate the output of 'snap list'
        mock_run.return_value.stdout = 'Name   Version   Rev    Tracking       Publisher   Notes\npkg1 1.0\npkg2 2.0\npkg3 3.0\n'
        # Simulate that no .desktop files exist
        mock_exists.side_effect = lambda path: False

        # Capture the output of the print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Simulate command-line arguments to exclude 'pkg3' and write .desktop files
        test_args = ['main.py', '--exclude=pkg3', '--write=all']
        with patch('sys.argv', test_args):
            main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Print captured output for debugging
        print("Captured Output:", captured_output.getvalue())

        # Check that subprocess.run was called correctly
        mock_run.assert_called_once_with(['snap', 'list'], stdout=subprocess.PIPE, text=True)
        
        # Check that create_desktop_file was called for each package except the excluded one
        expected_writes = [
            "[Desktop Entry]\nType=Application\nName=pkg1\nExec=snap run pkg1\nIcon=pkg1\n",
            "[Desktop Entry]\nType=Application\nName=pkg2\nExec=snap run pkg2\nIcon=pkg2\n"
        ]
        for write in expected_writes:
            mock_file().write.assert_any_call(write)

        # Check print output
        captured_output.seek(0)
        output_lines = captured_output.readlines()
        assert "Created .desktop file for pkg1" in output_lines
        assert "Created .desktop file for pkg2" in output_lines
        assert "Updated exclusion list: pkg1, pkg2, pkg3" in output_lines

if __name__ == '__main__':
    unittest.main()
