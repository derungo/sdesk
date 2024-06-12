import unittest
from unittest.mock import patch, mock_open

def create_desktop_file(package_name):
    desktop_path = f"/usr/share/applications/{package_name}.desktop"
    with open(desktop_path, 'w') as f:
        f.write(f"[Desktop Entry]\nType=Application\nName={package_name}\nExec=snap run {package_name}\nIcon={package_name}\n")

class TestCreateDesktopFile(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_create_desktop_file(self, mock_file):
        create_desktop_file('pkg1')
        mock_file.assert_called_once_with('/usr/share/applications/pkg1.desktop', 'w')
        mock_file().write.assert_called_once_with("[Desktop Entry]\nType=Application\nName=pkg1\nExec=snap run pkg1\nIcon=pkg1\n")

if __name__ == '__main__':
    unittest.main()
