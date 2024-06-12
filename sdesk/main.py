import logging
import subprocess
import os
import argparse

EXCLUDE_FILE = "exclusion_list.txt"
LOG_FILE = "script.log"

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_exclusion_set():
    try:
        with open(EXCLUDE_FILE, 'r') as file:
            excluded = {line.strip() for line in file if line.strip()}
        logging.info(f"Exclusion list read: {excluded}")
    except FileNotFoundError:
        excluded = set()
        logging.warning("Exclusion file not found, starting with an empty set.")
    return excluded

def update_exclusion_list(packages):
    try:
        with open(EXCLUDE_FILE, 'w') as file:
            file.writelines(f"{pkg}\n" for pkg in packages)
        logging.info(f"Updated exclusion list written: {packages}")
    except Exception as e:
        logging.error(f"Failed to update exclusion list: {e}")

def list_snap_packages(exclude_set):
    logging.info("Running snap list...")
    try:
        result = subprocess.run(['snap', 'list'], stdout=subprocess.PIPE, text=True)
        logging.debug(f"'snap list' output: {result.stdout}")

        packages = [line.split()[0] for line in result.stdout.split('\n')[1:] if line]
        filtered_packages = [pkg for pkg in packages if pkg not in exclude_set]
        logging.info(f"Filtered packages: {filtered_packages}")

        return filtered_packages
    except Exception as e:
        logging.error(f"Failed to list snap packages: {e}")
        return []

def check_desktop_files(package_name):
    desktop_path = f"/usr/share/applications/{package_name}.desktop"
    exists = os.path.exists(desktop_path)
    logging.debug(f"Checking desktop file for {package_name}: {exists}")
    return exists

def create_desktop_file(package_name):
    desktop_path = f"/usr/share/applications/{package_name}.desktop"
    try:
        with open(desktop_path, 'w') as f:
            f.write(f"[Desktop Entry]\nType=Application\nName={package_name}\nExec=snap run {package_name}\nIcon={package_name}\n")
        logging.info(f"Created .desktop file for {package_name}")
    except Exception as e:
        logging.error(f"Failed to create .desktop file for {package_name}: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Manage .desktop files for Snap packages.")
    parser.add_argument("--write", nargs='?', const='all', default=None,
                        help="Write .desktop files. Optionally specify a specific package name, or 'all' for all missing files.")
    parser.add_argument("--exclude", default="",
                        help="Add comma-separated list of Snap packages to permanently exclude (e.g., 'core20,flutter,dotnet-sdk'). Updates the exclusion list.")
    return parser.parse_args()

def main():
    logging.info("Starting main function")

    args = parse_args()
    excluded_packages = get_exclusion_set()
    logging.debug(f"Excluded packages: {excluded_packages}")

    if args.exclude:
        new_exclusions = set(args.exclude.split(','))
        excluded_packages.update(new_exclusions)
        update_exclusion_list(excluded_packages)
        logging.info(f"Updated exclusion list: {', '.join(excluded_packages)}")
        return

    packages = list_snap_packages(excluded_packages)
    logging.debug(f"Snap packages: {packages}")

    missing_desktop_files = [pkg for pkg in packages if not check_desktop_files(pkg)]
    logging.debug(f"Missing .desktop files: {missing_desktop_files}")

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
        logging.warning(f"No action needed or invalid package specified for --write: {args.write}")

if __name__ == "__main__":
    main()
