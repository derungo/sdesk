import unittest
from unittest.mock import patch, mock_open
import os
import subprocess
from main import get_exclusion_set, update_exclusion_list, list_snap_packages, check_desktop_files, create_desktop_file

class TestMain(unittest.TestCase):

    def test_get_exclusion_set(self):
        m = mock_open(read_data='pkg1\npkg2\n')
        with patch('builtins.open', m):
            excluded_packages = get_exclusion_set()
            self.assertEqual(excluded_packages, {'pkg1', 'pkg2'})

    def test_get_exclusion_set_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            excluded_packages = get_exclusion_set()
            self.assertEqual(excluded_packages, set())

    def test_update_exclusion_list(self):
        packages = ['pkg1', 'pkg2']
        with patch('builtins.open', create=True) as mock_open:
            update_exclusion_list(packages)
            mock_open.assert_called_once_with('exclusion_list.txt', 'w')
            mock_open.return_value.__enter__.return_value.writelines.assert_called_once()
            calls = mock_open.return_value.__enter__.return_value.writelines.call_args[0][0]
            self.assertEqual(list(calls), ['pkg1\n', 'pkg2\n'])

    def test_list_snap_packages(self):
        exclude_set = {'pkg1', 'pkg2'}
        result_stdout = 'pkg1 1.0\npkg2 2.0\npkg3 3.0\n'
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = result_stdout
            packages = list_snap_packages(exclude_set)
            mock_run.assert_called_once_with(['snap', 'list'], stdout=subprocess.PIPE, text=True)
            self.assertEqual(packages, ['pkg3'])

    def test_check_desktop_files(self):
        package_name = 'pkg1'
        desktop_path = f"/usr/share/applications/{package_name}.desktop"
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            exists = check_desktop_files(package_name)
            mock_exists.assert_called_once_with(desktop_path)
            self.assertTrue(exists)

    def test_create_desktop_file(self):
        package_name = 'pkg1'
        desktop_path = f"/usr/share/applications/{package_name}.desktop"
        with patch('builtins.open', create=True) as mock_open:
            create_desktop_file(package_name)
            mock_open.assert_called_once_with(desktop_path, 'w')
            mock_open.return_value.__enter__.return_value.write.assert_called_once_with(
                f"[Desktop Entry]\nType=Application\nName={package_name}\nExec=snap run {package_name}\nIcon={package_name}\n")

if __name__ == '__main__':
    unittest.main()
