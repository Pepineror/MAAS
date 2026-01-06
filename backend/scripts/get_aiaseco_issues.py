import os
from pathlib import Path
from dotenv import load_dotenv
from redminelib import Redmine
import json

# Load .env
dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path)

def get_aiaseco_issues(project_id=9):
    url = os.getenv("REDMINE_BASE_URL", "http://cidiia.uce.edu.do/")
    key = os.getenv("REDMINE_API_KEY")
    
    if not key:
        print("Error: REDMINE_API_KEY not found in .env")
        return

    redmine = Redmine(url, key=key)
    
    try:
        issues = redmine.issue.filter(project_id=project_id)
        print(f"Issues for project ID {project_id}:")
        for i in issues:
            print(f"- #{i.id}: {i.subject} (Status: {i.status.name})")
            # print description briefly
            desc = i.description or ""
            if desc:
                print(f"  Description: {desc[:100]}...")
            
            # check custom fields
            if hasattr(i, 'custom_fields'):
                for cf in i.custom_fields:
                    print(f"  CF: {cf['name']} = {cf['value']}")
                    
    except Exception as e:
        print(f"Error fetching issues: {str(e)}")

if __name__ == "__main__":
    get_aiaseco_issues()
