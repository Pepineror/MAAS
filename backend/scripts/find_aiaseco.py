import os
import sys
from pathlib import Path

# Add root directory to sys.path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from dotenv import load_dotenv
load_dotenv()

from backend.tools.custom_tools import RedmineTools

def find_aiaseco():
    tools = RedmineTools()
    projects = tools.list_projects()
    print("Found projects:")
    for p in projects:
        if "error" in p:
            print(f"Error: {p['error']}")
            continue
        print(f"- ID: {p['id']}, Name: {p['name']}, Identifier: {p['identifier']}")
        if "aiaseco" in p['name'].lower() or "aiaseco" in p['identifier'].lower():
            print(f">>> MATCH FOUND: {p['name']} (ID: {p['id']})")

if __name__ == "__main__":
    find_aiaseco()
