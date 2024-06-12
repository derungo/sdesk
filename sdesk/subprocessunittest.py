import unittest
from unittest.mock import patch
import subprocess

def run_snap_list():
    return subprocess.run(['snap', 'list'], stdout=subprocess.PIPE, text=True)

class TestSubprocessRun(unittest.TestCase):

    @patch('subprocess.run')
    def test_subprocess_run_called(self, mock_run):
        mock_run.return_value.stdout = 'Name   Version   Rev    Tracking       Publisher   Notes\npkg1 1.0\npkg2 2.0\npkg3 3.0\n'
        output = run_snap_list()
        mock_run.assert_called_once_with(['snap', 'list'], stdout=subprocess.PIPE, text=True)
        self.assertIn('pkg1 1.0', output.stdout)

if __name__ == '__main__':
    unittest.main()
