A simple utility to create .desktop files for snap packages.

Currently running the script with no args will give you a list of snap packages without corresponding .desktop files in your usr/share/applications directory.

Running the script with "--write all" will create .desktop files for all listed packages.

"--write <package_name>" will write the .desktop file for that specific package

"--exclude <package_name>" will build an exclusion list and can accept multiple packages seperated by commas. 