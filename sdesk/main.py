import subprocess
import os
import argparse
import logging
import shutil
from .version import __version__  # Import the version number


EXCLUDE_FILE = "exclusion_list.txt"
BACKUP_DIR = "desktop_backups"
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

def create_desktop_file(package_name, dry_run):
    desktop_path = f"/usr/share/applications/{package_name}.desktop"
    if dry_run:
        print(f"Would create .desktop file for {package_name}")
        logging.info(f"Dry run: would create .desktop file for {package_name}")
    else:
        try:
            with open(desktop_path, 'w') as f:
                f.write(f"[Desktop Entry]\nType=Application\nName={package_name}\nExec=snap run {package_name}\nIcon={package_name}\n")
            print(f"Created .desktop file for {package_name}")
            logging.info(f"Created .desktop file for {package_name}")
        except Exception as e:
            logging.error(f"Failed to create .desktop file for {package_name}: {e}")

def backup_desktop_files():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    for file in os.listdir("/usr/share/applications"):
        if file.endswith(".desktop"):
            shutil.copy(os.path.join("/usr/share/applications", file), BACKUP_DIR)
    logging.info("Backup of .desktop files completed")

def restore_desktop_files():
    if os.path.exists(BACKUP_DIR):
        for file in os.listdir(BACKUP_DIR):
            shutil.copy(os.path.join(BACKUP_DIR, file), "/usr/share/applications")
        logging.info("Restore of .desktop files completed")
    else:
        logging.warning("Backup directory not found, cannot restore .desktop files")

def interactive_mode():
    print("Interactive mode: manage your exclusion list")
    exclusion_set = get_exclusion_set()
    while True:
        print("\nCurrent exclusion list:", exclusion_set)
        print("Options: [a]dd, [r]emove, [q]uit")
        choice = input("Choose an option: ").strip().lower()
        if choice == 'a':
            pkg = input("Enter package name to exclude: ").strip()
            if pkg:
                exclusion_set.add(pkg)
                update_exclusion_list(exclusion_set)
        elif choice == 'r':
            pkg = input("Enter package name to remove from exclusion: ").strip()
            if pkg in exclusion_set:
                exclusion_set.remove(pkg)
                update_exclusion_list(exclusion_set)
        elif choice == 'q':
            break
        else:
            print("Invalid option, please choose again.")

def parse_args():
    parser = argparse.ArgumentParser(description="Manage .desktop files for Snap packages.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--write", nargs='?', const='all', default=None,
                        help="Write .desktop files. Optionally specify a specific package name, or 'all' for all missing files.")
    parser.add_argument("--exclude", default="",
                        help="Add comma-separated list of Snap packages to permanently exclude (e.g., 'core20,flutter,dotnet-sdk'). Updates the exclusion list.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making any changes.")
    parser.add_argument("--backup", action="store_true", help="Backup current .desktop files.")
    parser.add_argument("--restore", action="store_true", help="Restore .desktop files from backup.")
    parser.add_argument("--interactive", action="store_true", help="Enter interactive mode to manage exclusion list.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.interactive:
        interactive_mode()
        return

    if args.backup:
        backup_desktop_files()
        return

    if args.restore:
        restore_desktop_files()
        return

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
            create_desktop_file(pkg, args.dry_run)
    elif args.write in missing_desktop_files:
        create_desktop_file(args.write, args.dry_run)
    else:
        logging.warning(f"No action needed or invalid package specified for --write: {args.write}")

if __name__ == "__main__":
    main()
