SDESK

sdesk is a utility designed to manage and generate .desktop files for Snap packages. It simplifies accessing Snap applications directly from desktop environments by ensuring they have corresponding .desktop files in the /usr/share/applications directory.

Features:
List Missing .desktop Files: Automatically lists Snap packages that lack .desktop files.

Create .desktop Files: Facilitates the creation of .desktop files:

sudo sdesk --write all — Creates files for all listed packages.

sudo sdesk --write <package_name> — Targets a specific package for .desktop file creation.

Exclusion List: Allows specifying packages to exclude from processing, useful for packages that do not need a .desktop file or are system utilities.

Installation
Prerequisites
Ensure that Python and pip are installed on your system. sdesk works on Linux distributions that support Snap packages.

Install sdesk:
To install sdesk, use the following pip command:

pip install git+https://github.com/derungo/sdesk.git

Post-Installation Configuration:
Update PATH:
Ensure that /home/username/.local/bin is in your PATH. Add it by running:

echo "export PATH=\"$HOME/.local/bin:\$PATH\"" >> ~/.bashrc
source ~/.bashrc

Configure sudoers for Secure Execution:
To allow sudo access to sdesk, add /home/username/.local/bin to the secure_path in your sudoers file:

sudo visudo

And modify the secure_path setting as follows:

Defaults    secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/username/.local/bin"

Usage:
List Missing .desktop Files:

sdesk

Create .desktop Files for All Listed Packages:

sudo sdesk --write all

Create a .desktop File for a Specific Package:


sudo sdesk --write <package_name>

Exclude Specific Packages:

sdesk --exclude package1,package2

Contributing:
Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request. You can also open issues if you encounter bugs or have feature requests.

License:
sdesk is made available under the MIT License. For more details, see the LICENSE file in the repository.
