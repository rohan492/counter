import base64
import requests
import os
from datetime import datetime

# GitHub repository details
OWNER = "rohan492"
REPO = "counter"
FILE_PATH = "counter.txt"
BRANCH = "main"
TOKEN = os.getenv("TOKEN")

# GitHub API URL for the file
url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"
headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

# Step 1: Get the current file content and SHA
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    sha = data["sha"]
else:
    print("Failed to fetch file:", response.json())
    exit()

# Step 2: Update the content (increment counter or update timestamp)
new_content = f"Last updated: {datetime.now().isoformat()}"
new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")  # Encode to Base64

# Step 3: Prepare the payload
payload = {
    "message": "Automated update to maintain streak",
    "content": new_content_encoded,
    "sha": sha,  # Required for updating an existing file
    "branch": BRANCH,
}

# Step 4: Commit the change
response = requests.put(url, json=payload, headers=headers)

if response.status_code == 200 or response.status_code == 201:
    print("✅ File updated successfully.")
else:
    print("❌ Failed to update the file:", response.json())
