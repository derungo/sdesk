# SDESK

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Badges](#badges)

## About <a name = "about"></a>

SDESK is a utility designed to manage and generate .desktop files for Snap packages. It simplifies accessing Snap applications directly from desktop environments by ensuring they have corresponding .desktop files in the `/usr/share/applications` directory. The utility lists Snap packages that lack .desktop files and facilitates their creation, allowing users to customize which packages to process.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure that Python and pip are installed on your system. SDESK works on Linux distributions that support Snap packages.

### Installing

To install SDESK, use the following pip command:

~~~
pip install git+https://github.com/derungo/sdesk.git
~~~

Post-Installation Configuration:

Update PATH:

Ensure that `/home/username/.local/bin` is in your PATH. Add it by running:
~~~
echo "export PATH=\"$HOME/.local/bin:\$PATH\"" >> ~/.bashrc
source ~/.bashrc
~~~
Configure sudoers for Secure Execution:

To allow sudo access to SDESK, add `/home/username/.local/bin` to the secure_path in your sudoers file:
~~~
sudo visudo
~~~
And modify the secure_path setting as follows:
~~~
Defaults    secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/username/.local/bin"
~~~

## Usage <a name = "usage"></a>

List Missing .desktop Files:
~~~
sdesk
~~~
Create .desktop Files for All Listed Packages:
~~~
sudo sdesk --write all
~~~
Create a .desktop File for a Specific Package:
~~~
sudo sdesk --write <package_name>
~~~
Exclude Specific Packages:
~~~
sdesk --exclude package1,package2
~~~
Check the Version:
~~~
sdesk --version
~~~
Dry Run (Show what would be done without making any changes):
~~~
sdesk --dry-run --write all
~~~
Backup Current .desktop Files:
~~~
sdesk --backup
~~~
Restore .desktop Files from Backup:
~~~
sdesk --restore
~~~
Interactive Mode to Manage Exclusion List:
~~~
sdesk --interactive
~~~
Enable Verbose Output:
~~~
sdesk --verbose
~~~

## Contributing <a name = "contributing"></a>

Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request. You can also open issues if you encounter bugs or have feature requests.

## License <a name = "license"></a>

SDESK is made available under the MIT License. For more details, see the LICENSE file in the repository.

## Badges <a name = "badges"></a>  
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)  
