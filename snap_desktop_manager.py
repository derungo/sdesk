#!/usr/bin/env python3

import subprocess
import os
import argparse

EXCLUDE_FILE = "exclusion_list.txt"

def get_exclusion_set():
    try:
        with open(EXCLUDE_FILE, 'r') as file:
            excluded = {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        excluded = set()
    return excluded

def update_exclusion_list(packages):
    with open(EXCLUDE_FILE, 'w') as file:
        file.writelines(f"{pkg}\n" for pkg in packages)

def list_snap_packages(exclude_set):
    result = subprocess.run(['snap', 'list'], stdout=subprocess.PIPE, text=True)
    packages = [line.split()[0] for line in result.stdout.split('\n')[1:] if line]
    filtered_packages = [pkg for pkg in packages if pkg not in exclude_set]
    return filtered_packages

def check_desktop_files(package_name):
    desktop_path = f"/usr/share/applications/{package_name}.desktop"
    return os.path.exists(desktop_path)

def create_desktop_file(package_name):
    desktop_path = f"/usr/share/applications/{package_name}.desktop"
    with open(desktop_path, 'w') as f:
        f.write(f"[Desktop Entry]\nType=Application\nName={package_name}\nExec=snap run {package_name}\nIcon={package_name}\n")
    print(f"Created .desktop file for {package_name}")

def parse_args():
    parser = argparse.ArgumentParser(description="Manage .desktop files for Snap packages.")
    parser.add_argument("--write", nargs='?', const='all', default=None,
                        help="Write .desktop files. Optionally specify a specific package name, or 'all' for all missing files.")
    parser.add_argument("--exclude", default="",
                        help="Add comma-separated list of Snap packages to permanently exclude (e.g., 'core20,flutter,dotnet-sdk'). Updates the exclusion list.")
    return parser.parse_args()

def main():
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