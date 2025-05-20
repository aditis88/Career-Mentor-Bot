import os
from datetime import datetime

def log_session(user_id, profile, dataset_recommendations, llm_advice):
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, f"{user_id}_session_log.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"--- Session on {datetime.now()} ---\n")
        f.write("Background: " + profile["background"] + "\n")
        f.write("Skills: " + ", ".join(profile["skills"]) + "\n")
        f.write("Goals: " + profile["goals"] + "\n\n")

        f.write("📚 Dataset-Based Recommendations:\n")
        for role, score in dataset_recommendations:
            f.write(f"- {role} ({score}%)\n")

        f.write("\n✨ LLM Personalized Advice:\n")
        f.write(llm_advice + "\n")
        f.write("-" * 50 + "\n\n")
