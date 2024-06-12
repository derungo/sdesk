import subprocess
import os
import argparse

EXCLUDE_FILE = "exclusion_list.txt"

def get_exclusion_set():
    try:
        with open(EXCLUDE_FILE, 'r') as file:
            excluded = {line.strip() for line in file if line.strip()}
        print(f"Exclusion list read: {excluded}")  # Debugging print statement
    except FileNotFoundError:
        excluded = set()
        print("Exclusion file not found, starting with an empty set.")  # Debugging print statement
    return excluded

def update_exclusion_list(packages):
    with open(EXCLUDE_FILE, 'w') as file:
        file.writelines(f"{pkg}\n" for pkg in packages)
    print(f"Updated exclusion list written: {packages}")  # Debugging print statement

def list_snap_packages(exclude_set):
    print("Running snap list...")  # Debugging print statement
    result = subprocess.run(['snap', 'list'], stdout=subprocess.PIPE, text=True)
    print(f"'snap list' output: {result.stdout}")  # Debugging print statement

    packages = [line.split()[0] for line in result.stdout.split('\n')[1:] if line]
    filtered_packages = [pkg for pkg in packages if pkg not in exclude_set]
    print(f"Filtered packages: {filtered_packages}")  # Debugging print statement

    return filtered_packages

def check_desktop_files(package_name):
    desktop_path = f"/usr/share/applications/{package_name}.desktop"
    exists = os.path.exists(desktop_path)
    print(f"Checking desktop file for {package_name}: {exists}")  # Debugging print statement
    return exists

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
    print("Starting main function")  # Debugging print statement

    args = parse_args()
    excluded_packages = get_exclusion_set()
    print(f"Excluded packages: {excluded_packages}")  # Debugging print statement

    if args.exclude:
        new_exclusions = set(args.exclude.split(','))
        excluded_packages.update(new_exclusions)
        update_exclusion_list(excluded_packages)
        print(f"Updated exclusion list: {', '.join(excluded_packages)}")
        return

    packages = list_snap_packages(excluded_packages)
    print(f"Snap packages: {packages}")  # Debugging print statement

    missing_desktop_files = [pkg for pkg in packages if not check_desktop_files(pkg)]
    print(f"Missing .desktop files: {missing_desktop_files}")  # Debugging print statement

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
