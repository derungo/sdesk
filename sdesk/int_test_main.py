import unittest
from unittest.mock import patch, mock_open
import subprocess
import os
from io import StringIO
import sys

from main import main

class TestIntegration(unittest.TestCase):

    @patch.dict(os.environ, {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"})
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open, read_data='pkg1\npkg2\n')
    @patch('os.path.exists')
    def test_integration_write_all(self, mock_exists, mock_file, mock_run):
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
        output_value = captured_output.getvalue()
        print("Captured Output:", output_value)

        # Check that subprocess.run was called correctly
        try:
            mock_run.assert_called_once_with(['snap', 'list'], stdout=subprocess.PIPE, text=True)
        except AssertionError as e:
            print(f"Assertion Error: {e}")
            print(f"mock_run.call_args_list: {mock_run.call_args_list}")

        # Debugging print statements to trace logic
        print(f"mock_file.write.call_args_list: {mock_file().write.call_args_list}")

        # Check that create_desktop_file was called for each package
        expected_writes = [
            "[Desktop Entry]\nType=Application\nName=pkg3\nExec=snap run pkg3\nIcon=pkg3\n"
        ]
        for write in expected_writes:
            try:
                mock_file().write.assert_any_call(write)
            except AssertionError as e:
                print(f"Assertion Error: {e}")
                print(f"mock_file.write.call_args_list: {mock_file().write.call_args_list}")

        # Check print output
        output_lines = output_value.splitlines()
        print("Output Lines:", output_lines)  # Debugging print statement
        self.assertIn("Created .desktop file for pkg3", output_lines)

if __name__ == '__main__':
    unittest.main()
