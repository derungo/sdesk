#!/usr/bin/env python3

import subprocess
import os
import argparse

EXCLUDE_FILE = "exclusion_list.txt"

def get_exclusion_set():
    """
    Get the set of excluded packages from the exclusion list file.

    Returns:
        set: The set of excluded packages.
    """
    try:
        with open(EXCLUDE_FILE, 'r') as file:
            excluded = {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        excluded = set()
    return excluded

def update_exclusion_list(packages):
    """
    Update the exclusion list file with the given packages.

    Args:
        packages (list): The list of packages to be excluded.
    """
    with open(EXCLUDE_FILE, 'w') as file:
        file.writelines(f"{pkg}\n" for pkg in packages)

def list_snap_packages(exclude_set):
    """
    List all Snap packages, excluding the ones in the exclusion set.

    Args:
        exclude_set (set): The set of packages to be excluded.

    Returns:
        list: The list of Snap packages.
    """
    result = subprocess.run(['snap', 'list'], stdout=subprocess.PIPE, text=True)
    packages = [line.split()[0] for line in result.stdout.split('\n')[1:] if line]
    filtered_packages = [pkg for pkg in packages if pkg not in exclude_set]
    return filtered_packages

def check_desktop_files(package_name):
    """
    Check if the .desktop file exists for the given package.

    Args:
        package_name (str): The name of the package.

    Returns:
        bool: True if the .desktop file exists, False otherwise.
    """
    desktop_path = f"/usr/share/applications/{package_name}.desktop"
    return os.path.exists(desktop_path)

def create_desktop_file(package_name):
    """
    Create a .desktop file for the given package.

    Args:
        package_name (str): The name of the package.
    """
    desktop_path = f"/usr/share/applications/{package_name}.desktop"
    with open(desktop_path, 'w') as f:
        f.write(f"[Desktop Entry]\nType=Application\nName={package_name}\nExec=snap run {package_name}\nIcon={package_name}\n")
    print(f"Created .desktop file for {package_name}")

def parse_args():
    """
    Parse the command line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Manage .desktop files for Snap packages.")
    parser.add_argument("--write", nargs='?', const='all', default=None,
                        help="Write .desktop files. Optionally specify a specific package name, or 'all' for all missing files.")
    parser.add_argument("--exclude", default="",
                        help="Add comma-separated list of Snap packages to permanently exclude (e.g., 'core20,flutter,dotnet-sdk'). Updates the exclusion list.")
    return parser.parse_args()

def main():
    """
    The main function of the script.
    """
    args = parse_args()
    excluded_packages = get_exclusion_set()

    if args.exclude:
        new_exclusions = set(args.exclude.split(','))
        excluded_packages.update(new_exclusions)
        update_exclusion_list(excluded_packages)
        print(f"Updated exclusion list: {', '.join(excluded_packages)}")
        return

    packages = list_snap_packages(excluded_packages)
    missing_desktop_files = [pkg for pkg in packages if not check_desktop_files(pkg)]

    if args.write is None:
        if missing_desktop_files:
            print("Snap packages missing .desktop files:")
            for pkg in missing_desktop_files:
                print(f"- {pkg}")
        else:
            print("All Snap packages have .desktop files.")
    elif args.write == 'all':
        for pkg in missing_desktop_files:
            create_desktop_file(pkg)
    elif args.write in missing_desktop_files:
        create_desktop_file(args.write)
    else:
        print(f"No action needed or invalid package specified for --write: {args.write}")


if __name__ == "__main__":
    main()