import json
import os

def load_user_profile(user_id):
    os.makedirs("data", exist_ok=True)
    path = f"data/{user_id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"id": user_id, "background": "", "goals": "", "skills": []}

def save_user_profile(user_id, profile):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{user_id}.json", "w") as f:
        json.dump(profile, f, indent=2)
