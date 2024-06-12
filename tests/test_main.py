import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import subprocess
from sdesk.main import get_exclusion_set, update_exclusion_list, list_snap_packages, check_desktop_files, create_desktop_file, backup_desktop_files, restore_desktop_files, interactive_mode

class TestMain(unittest.TestCase):

    def test_get_exclusion_set(self):
        # Mocking the open function and simulating file content
        m = mock_open(read_data='pkg1\npkg2\n')
        with patch('builtins.open', m):
            excluded_packages = get_exclusion_set()
            self.assertEqual(excluded_packages, {'pkg1', 'pkg2'})

    def test_get_exclusion_set_file_not_found(self):
        # Mocking the open function to raise a FileNotFoundError
        with patch('builtins.open', side_effect=FileNotFoundError):
            excluded_packages = get_exclusion_set()
            self.assertEqual(excluded_packages, set())

    def test_update_exclusion_list(self):
        packages = ['pkg1', 'pkg2']
        # Mocking the open function
        with patch('builtins.open', mock_open()) as mock_file:
            update_exclusion_list(packages)
            mock_file.assert_called_once_with('exclusion_list.txt', 'w')
            mock_file().writelines.assert_called_once()
            calls = mock_file().writelines.call_args[0][0]
            self.assertEqual(list(calls), ['pkg1\n', 'pkg2\n'])

    def test_list_snap_packages(self):
        exclude_set = {'pkg1', 'pkg2'}
        result_stdout = 'Name   Version   Rev    Tracking       Publisher   Notes\npkg1 1.0\npkg2 2.0\npkg3 3.0\n'
        # Mocking the subprocess.run function
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = result_stdout
            packages = list_snap_packages(exclude_set)
            mock_run.assert_called_once_with(['snap', 'list'], stdout=subprocess.PIPE, text=True)
            self.assertEqual(packages, ['pkg3'])

    def test_check_desktop_files(self):
        package_name = 'pkg1'
        desktop_path = f"/usr/share/applications/{package_name}.desktop"
        # Mocking os.path.exists to return True
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            exists = check_desktop_files(package_name)
            mock_exists.assert_called_once_with(desktop_path)
            self.assertTrue(exists)

    def test_create_desktop_file_dry_run(self):
        package_name = 'pkg1'
        with patch('builtins.print') as mocked_print:
            create_desktop_file(package_name, dry_run=True)
            mocked_print.assert_called_once_with(f"Would create .desktop file for {package_name}")

    def test_create_desktop_file(self):
        package_name = 'pkg1'
        desktop_path = f"/usr/share/applications/{package_name}.desktop"
        # Mocking the open function
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('builtins.print') as mocked_print:
                create_desktop_file(package_name, dry_run=False)
                mock_file.assert_called_once_with(desktop_path, 'w')
                mock_file().write.assert_called_once_with(
                    f"[Desktop Entry]\nType=Application\nName={package_name}\nExec=snap run {package_name}\nIcon={package_name}\n")
                mocked_print.assert_called_once_with(f"Created .desktop file for {package_name}")

    def test_backup_desktop_files(self):
        with patch('os.makedirs') as mock_makedirs, \
             patch('os.listdir', return_value=['app1.desktop', 'app2.desktop']) as mock_listdir, \
             patch('shutil.copy') as mock_copy:
            backup_desktop_files()
            mock_makedirs.assert_called_once_with('desktop_backups')
            mock_copy.assert_any_call('/usr/share/applications/app1.desktop', 'desktop_backups')
            mock_copy.assert_any_call('/usr/share/applications/app2.desktop', 'desktop_backups')

    def test_restore_desktop_files(self):
        with patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=['app1.desktop', 'app2.desktop']) as mock_listdir, \
             patch('shutil.copy') as mock_copy:
            restore_desktop_files()
            mock_copy.assert_any_call('desktop_backups/app1.desktop', '/usr/share/applications')
            mock_copy.assert_any_call('desktop_backups/app2.desktop', '/usr/share/applications')

    def test_restore_desktop_files_no_backup(self):
        with patch('os.path.exists', return_value=False):
            with self.assertLogs(level='WARNING') as log:
                restore_desktop_files()
                self.assertIn('WARNING:root:Backup directory not found, cannot restore .desktop files', log.output)

    def test_interactive_mode(self):
        exclusion_set = {'pkg1', 'pkg2'}
        with patch('builtins.input', side_effect=['a', 'pkg3', 'q']), \
             patch('builtins.print'), \
             patch('sdesk.main.get_exclusion_set', return_value=exclusion_set), \
             patch('sdesk.main.update_exclusion_list') as mock_update:
            interactive_mode()
            mock_update.assert_called_with({'pkg1', 'pkg2', 'pkg3'})

if __name__ == '__main__':
    unittest.main()
