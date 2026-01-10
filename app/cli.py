import json
import os.path
import shutil
import subprocess
from core.backup import BackupCreator
from core.restore import RestoreFile
from core.cleaner import ClearByTime
from core.list import ShowData
from core.temp_backup import TemporaryBackup
from app.logging_config import setup_logging
import argparse
import os
import hashlib

def file_hash(file_path):
    file = hashlib.sha256()
    with open(file_path, "rb") as f:
        file.update(f.read())
    return file.hexdigest()

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
                                     Create a backup for a file with default 1 day
                                     bt -b /path/to/file
                                     
                                     Create a temporary backup while editing file in the text editor
                                     bt edit vim example.txt
                                     
                                     Create a backup for a file with 5 hours to store
                                     bt -b /path/to/file -t 5 -k h
                                     
                                     Show all files in backup storage 
                                     bt --show
                                     
                                     Restore file by ID
                                     bt -r 12345
                                     ''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-b', '--backup', help="Path for file to create a backup")
    parser.add_argument('-r', '--rollback',type=int, help="ID of the backup to restore")
    parser.add_argument('-t', '--time', type=int, default=1, help="Time for storing the backup")
    parser.add_argument('-k', '--keep', choices=['h', 'd'], default='d', help="Time index: -h for hours, -d for days")
    parser.add_argument('-s', '--show', action='store_true', help="Shows info about copied files")
    subparsers = parser.add_subparsers(dest="command")
    edit_parser = subparsers.add_parser("edit", help="Edits file and creates a backup for safety")
    edit_parser.add_argument("editor", help="Editor (for example: nano, vim, kate)")
    edit_parser.add_argument("file", help="File path")

    args = parser.parse_args()

    if args.command == "edit":
        file_path = args.file
        editor = args.editor

        if not shutil.which(editor):
            parser.error("Editor not found")

        if editor in ("kate",):
            editor += " -b"
        elif editor in ("gedit", "code", "codium"):
            editor += " --wait"

        if not os.path.isfile(file_path):
            parser.error("File does not exist")

        hash_before = file_hash(file_path)
        backup = TemporaryBackup(file_path)
        backup.create()
        try:
            subprocess.run(editor.split() + [file_path], check=False)
        except KeyboardInterrupt:
            backup.restore()
            backup.clean()
            return

        hash_after = file_hash(file_path)
        if hash_after != hash_before:
            answer_check = input("Keep changes? [y/N]").lower()
            if answer_check != "y":
                backup.restore()
        backup.clean()
        return

    if args.backup:
        BackupCreator().create_backup(args.backup, args.time, args.keep)

    if args.rollback:
        RestoreFile().restore_file(args.rollback)

    if args.show:
        ShowData().show_data()

if __name__ == '__main__':
    main()

