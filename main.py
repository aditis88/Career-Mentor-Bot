from logger import log_session
from memory_manager import load_user_profile, save_user_profile
from recommend import get_llm_recommendations, recommend_from_dataset

def main():
    print("🎯 Welcome to Career Mentor Bot (Gemini Edition) 🎯")
    user_id = input("Enter your name or username: ").lower()
    profile = load_user_profile(user_id)

    print("\n--- Update Your Profile ---")
    profile["background"] = input("Your background: ")
    profile["skills"] = input("List your skills (comma-separated): ").split(",")
    profile["skills"] = [skill.strip() for skill in profile["skills"]]
    profile["goals"] = input("What are your career goals? ")

    save_user_profile(user_id, profile)
    print("\n✅ Profile Saved Successfully!")

    # Dataset-based suggestion
    print("\n📚 Based on your skills, you might like these roles:")
    dataset_recommendations = recommend_from_dataset(profile["skills"])
    if dataset_recommendations:
        for role, score in dataset_recommendations:
            print(f"- {role} (Skill Match: {score}%)")
    else:
        print("No strong matches found in the dataset.")

    # Gemini LLM advice
    print("\n✨ Personalized Advice from Gemini Mentor:")
    advice = get_llm_recommendations(profile)
    print(advice)

    log_session(user_id, profile, dataset_recommendations, advice)
    print("\n📝 Session logged successfully!")


if __name__ == "__main__":
    main()
