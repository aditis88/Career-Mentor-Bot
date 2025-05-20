import google.generativeai as genai
import json
import os
from prompts import career_prompt
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")


def get_llm_recommendations(profile):
    prompt = career_prompt.format(
        background=profile["background"],
        skills=", ".join(profile["skills"]),
        goals=profile["goals"]
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini Error: {str(e)}"


def load_career_dataset():
    with open("careers.json", "r") as f:
        return json.load(f)


def recommend_from_dataset(user_skills, threshold=0.4):
    careers = load_career_dataset()
    recommendations = []

    for career in careers:
        career_skills = set(skill.lower() for skill in career.get("skills", []))
        user_skills_set = set(skill.lower() for skill in user_skills)

        if not career_skills:
            continue

        match_score = len(career_skills & user_skills_set) / len(career_skills)

        if match_score >= threshold:
            recommendations.append((career["role"], round(match_score * 100, 2)))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations


def get_required_skills(role_name):
    careers = load_career_dataset()
    for career in careers:
        if career["role"].lower() == role_name.lower():
            return {
                "skills": career.get("skills", []),
                "resources": {
                    "courses": career.get("courses", ["No specific courses listed."]),
                    "projects": career.get("projects", ["No sample projects available."]),
                    "interview_topics": career.get("interview_topics", ["No interview topics listed."])
                }
            }
    return None


def get_missing_skills(user_skills, target_role):
    role_data = get_required_skills(target_role)
    if not role_data:
        return "⚠️ Role not found in dataset."

    required_skills = set(skill.lower() for skill in role_data["skills"])
    user_skills_set = set(skill.lower() for skill in user_skills)

    missing = required_skills - user_skills_set

    return list(missing)
