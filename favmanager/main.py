import sys
import argparse
import subprocess
import os
from . import storage

def addfav():
    parser = argparse.ArgumentParser(description="Add a favorite directory")
    parser.add_argument("alias", help="Alias for the directory")
    parser.add_argument("path", nargs="?", default=os.getcwd(), help="Path to the directory (default: current directory)")
    args = parser.parse_args()
    storage.add_entry(False, args.alias, args.path)
    print(f"Directory favorite added: {args.alias} -> {os.path.abspath(args.path)}")

def rmfav():
    parser = argparse.ArgumentParser(description="Remove a favorite directory")
    parser.add_argument("alias", help="Alias for the directory")
    args = parser.parse_args()
    if storage.remove_entry(False, args.alias):
        print(f"Directory favorite removed: {args.alias}")
    else:
        print(f"Alias not found: {args.alias}", file=sys.stderr)

def goto():
    parser = argparse.ArgumentParser(description="Get path of a favorite directory")
    parser.add_argument("alias", help="Alias for the directory")
    args = parser.parse_args()
    path = storage.get_path(False, args.alias)
    if path:
        print(path)
    else:
        print(f"Alias not found: {args.alias}", file=sys.stderr)
        sys.exit(1)

def addfavf():
    parser = argparse.ArgumentParser(description="Add a favorite file")
    parser.add_argument("alias", help="Alias for the file")
    parser.add_argument("path", help="Path to the file")
    args = parser.parse_args()
    storage.add_entry(True, args.alias, args.path)
    print(f"File favorite added: {args.alias} -> {os.path.abspath(args.path)}")

def rmfavf():
    parser = argparse.ArgumentParser(description="Remove a favorite file")
    parser.add_argument("alias", help="Alias for the file")
    args = parser.parse_args()
    if storage.remove_entry(True, args.alias):
        print(f"File favorite removed: {args.alias}")
    else:
        print(f"Alias not found: {args.alias}", file=sys.stderr)

def execute():
    parser = argparse.ArgumentParser(description="Execute a favorite file")
    parser.add_argument("alias", help="Alias for the file")
    parser.add_argument("--interpreter", default="python", help="Interpreter to run the file (default: python)")
    args, unknown = parser.parse_known_args()
    
    path = storage.get_path(True, args.alias)
    if not path:
        print(f"Alias not found: {args.alias}", file=sys.stderr)
        sys.exit(1)
    
    cmd = [args.interpreter, path] + unknown
    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        print(f"Interpreter not found: {args.interpreter}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error executing file: {e}", file=sys.stderr)
        sys.exit(1)

def listfav():
    dirs = storage.load_dirs()
    files = storage.load_files()
    
    print("--- Favorite Directories ---")
    if dirs:
        for alias, path in dirs.items():
            print(f"{alias:15} -> {path}")
    else:
        print("No directory favorites saved.")
        
    print("\n--- Favorite Files ---")
    if files:
        for alias, path in files.items():
            print(f"{alias:15} -> {path}")
    else:
        print("No file favorites saved.")
