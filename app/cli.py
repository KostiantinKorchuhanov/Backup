import json
import os.path
from core.backup import BackupCreator
from core.restore import RestoreFile
from core.cleaner import ClearByTime
from core.list import ShowData
from app.logging_config import setup_logging
import argparse

def main():
    if not os.path.exists("database"):
        os.mkdir("database")

    data_file = os.path.join("database", "data.json")
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            json.dump([], f)

    setup_logging()
    ClearByTime().check_clean()

    parser = argparse.ArgumentParser(description="Safe config backup and restore utility",
                                     epilog='''
                                     Examples:
                                     # Create a backup for a file with default 1 day
                                     bt -b /path/to/file
                                     
                                     # Create a backup for a file with 5 hours to store
                                     bt -b /path/to/file -t 5 -k h
                                     
                                     # Show all files in backup storage 
                                     bt --show
                                     
                                     # Restore file by ID
                                     bt -r 12345
                                     ''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-b', '--backup', help="Path for file to create a backup")
    parser.add_argument('-r', '--rollback',type=int, help="ID of the backup to restore")
    parser.add_argument('-t', '--time', type=int, default=1, help="Time for storing the backup")
    parser.add_argument('-k', '--keep', choices=['h', 'd'], default='d', help="Time index: -h for hours, -d for days")
    parser.add_argument('-s', '--show', action='store_true', help="Shows info about copied files")

    args = parser.parse_args()

    if args.backup:
        BackupCreator().create_backup(args.backup, args.time, args.keep)

    if args.rollback:
        RestoreFile().restore_file(args.rollback)

    if args.show:
        ShowData().show_data()

if __name__ == '__main__':
    main()

