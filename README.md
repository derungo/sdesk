A simple utility to create .desktop files for snap packages.

Currently, running sdesk with no args will give you a list of snap packages without corresponding .desktop files in your usr/share/applications directory.

Running "sudo sdesk --write all" will create .desktop files for all listed packages.

"sudo sdesk --write package_name" will write the .desktop file for that specific package

"sdesk --exclude package_name" will build an exclusion list and can accept multiple packages seperated by commas. 

Install via the command line using "pip install git+https://github.com/derungo/sdesk.git"

If not already you will need to add /home/username/.local/bin to PATH

Script requires sudo to write files to the /usr/share/applications directory, so you will need to add /home/username/.local/bin to the secure_path variable in the "sudoers" file