import streamlit as st
import datetime
import json

from memory_manager import load_user_profile, save_user_profile
from recommend import recommend_from_dataset, get_required_skills
from resume_parser import extract_skills_from_resume
from model_switcher import get_response, OPENAI_API_KEY
from job_finder import fetch_job_links, find_mock_jobs

st.set_page_config(page_title="Career Mentor Bot", layout="centered")
st.title("🎯 Career Mentor Bot (LLM-Powered Edition)")

# Apply basic dark/light theme toggle
st.sidebar.title("🔧 Settings")
theme_choice = st.sidebar.radio("Theme Mode:", ["Light", "Dark"])
if theme_choice == "Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: #FAFAFA;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'feedback_log' not in st.session_state:
    st.session_state.feedback_log = []

# Sidebar - Settings and Persona
st.sidebar.title("🔧 Settings")
available_models = ["Gemini"]
if OPENAI_API_KEY:
    available_models.append("OpenAI")
model_choice = st.sidebar.radio("Choose LLM Engine:", available_models)

persona = st.sidebar.radio("Select your persona:", ["Student", "Career Switcher", "Working Professional"])

# User Profile
user_id = st.text_input("Enter your name or username to get started:")
if user_id:
    profile = load_user_profile(user_id.lower())

    st.subheader("📝 Update Your Profile")
    profile["background"] = st.text_input("Your background:", value=profile.get("background", ""))
    skills_input = st.text_input("List your skills (comma-separated):", value=", ".join(profile.get("skills", [])))
    profile["skills"] = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
    profile["goals"] = st.text_area("What are your career goals?", value=profile.get("goals", ""))

    # Resume Upload
    st.subheader("📄 Upload Your Resume (PDF)")
    uploaded_resume = st.file_uploader("Choose a file", type=["pdf"])
    if uploaded_resume:
        resume_skills = extract_skills_from_resume(uploaded_resume)
        if resume_skills:
            st.markdown(f"🧠 **Skills from Resume:** `{', '.join(resume_skills)}`")
            profile["skills"] = list(set(profile["skills"] + resume_skills))
        else:
            st.warning("⚠️ Could not extract skills from the resume.")

        st.markdown("---")
        st.subheader("🏅 Inferred Job Level")
        level_prompt = (
            f"Persona: {persona}\n"
            f"Candidate Background: {profile['background']}\n"
            f"Skills: {', '.join(profile['skills'])}\n"
            f"Career Goals: {profile['goals']}\n"
            "Infer the most likely job level (e.g., Intern, Junior, Mid-level, Senior, Lead)."
        )
        inferred_level = get_response(level_prompt, model=model_choice)
        st.info(f"🔍 **Job Level Inference:** {inferred_level}")

    if st.button("💾 Save Profile"):
        save_user_profile(user_id.lower(), profile)
        st.success("✅ Profile saved successfully!")

    # Dataset-based Recommendations
    if profile["skills"]:
        st.subheader("📚 Recommended Roles from Dataset")
        dataset_recs = recommend_from_dataset(profile["skills"])
        if dataset_recs:
            for role, score in dataset_recs:
                st.write(f"- **{role}** (Skill Match: {score}%)")

            top_role = dataset_recs[0][0]
            required_info = get_required_skills(top_role)
            required_skills = required_info.get("skills", [])
            missing_skills = list(set(required_skills) - set(profile["skills"]))

            st.markdown("---")
            st.subheader("🌟 LLM Career Fit Recommendation")

            llm_prompt = (
                f"Persona: {persona}\n"
                f"Candidate Background: {profile['background']}\n"
                f"Skills: {', '.join(profile['skills'])}\n"
                f"Career Goals: {profile['goals']}\n"
                f"Target Role: {top_role}\n"
                f"Missing Skills: {', '.join(missing_skills)}\n"
                "\nBased on this, answer the following:\n"
                "- Fit confidence score (out of 100)\n"
                "- 2-3 online courses\n"
                "- 2 project ideas\n"
                "- Top 3 interview prep topics"
            )

            llm_output = get_response(llm_prompt, model=model_choice)
            st.info(llm_output)

            if missing_skills:
                st.warning(f"🧩 **Missing Skills for {top_role}:** {', '.join(missing_skills)}")
            else:
                st.success(f"✅ You meet all the key skills for a {top_role}!")

            # 🎯 NEW: Role-Specific Roadmap
            st.markdown("---")
            st.subheader("🗺 Personalized Learning Roadmap")
            roadmap_prompt = (
                f"Create a 3–6 month roadmap for a {persona} aiming for the role of {top_role}.\n"
                f"Skills: {', '.join(profile['skills'])}\n"
                f"Missing Skills: {', '.join(missing_skills)}\n"
                "Include weekly goals, key topics, project ideas, and relevant certifications."
            )
            roadmap_output = get_response(roadmap_prompt, model=model_choice)
            st.info(roadmap_output)

            # 🎤 NEW: Mock Interview Questions
            st.markdown("---")
            st.subheader("🎤 Mock Interview Questions")
            interview_prompt = (
                f"Provide 5 mock interview questions for a {top_role}.\n"
                f"Persona: {persona}\n"
                f"Skills: {', '.join(profile['skills'])}"
            )
            interview_output = get_response(interview_prompt, model=model_choice)
            st.info(interview_output)

            # 🔗 Job Links Section
            st.markdown("---")
            st.subheader("🔗 Relevant Job Links")
            job_links = fetch_job_links(top_role)
            if job_links:
               for job in job_links:
                   st.markdown(f"[{job['title']}]({job['url']}) - {job['company']} ({job['location']})")
            else:
                st.info("No live job links found. Showing some sample jobs instead.")
                mock_jobs = find_mock_jobs(top_role)
                for job in mock_jobs:
                    st.markdown(f"[{job['title']}]({job['url']}) - {job['company']} ({job['location']})")

            # 🗂 Dashboard Summary
            st.markdown("---")
            st.subheader("📊 Dashboard Summary")
            st.markdown(f"**👤 User:** {user_id}")
            st.markdown(f"**🎯 Target Role:** {top_role}")
            st.markdown(f"**🔍 Inferred Level:** {inferred_level}")
            st.markdown(f"**🧠 Skills:** {', '.join(profile['skills'])}")
            st.markdown(f"**📈 Missing Skills:** {', '.join(missing_skills) if missing_skills else 'None'}")

            # Feedback System
            st.markdown("---")
            st.subheader("💬 Feedback on Recommendation")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Like"):
                    st.success("Thanks for the positive feedback!")
                    st.session_state.feedback_log.append({"user": user_id, "role": top_role, "reaction": "like"})
            with col2:
                if st.button("👎 Dislike"):
                    st.warning("We appreciate your feedback to improve.")
                    st.session_state.feedback_log.append({"user": user_id, "role": top_role, "reaction": "dislike"})

            feedback_text = st.text_area("Optional comments or suggestions:")
            if st.button("Submit Feedback") and feedback_text:
                st.success("✅ Feedback submitted!")
                st.session_state.feedback_log.append({
                    "user": user_id,
                    "role": top_role,
                    "reaction": "comment",
                    "text": feedback_text
                })

        else:
            st.warning("No strong matches found in the dataset.")

    if st.button("🤖 Get Personalized Advice from LLM"):
        st.subheader("✨ Personalized Advice")
        prompt = (
            f"Persona: {persona}\n"
            f"Background: {profile['background']}\n"
            f"Skills: {', '.join(profile['skills'])}\n"
            f"Goals: {profile['goals']}\n"
            "Suggest career roles and learning paths."
        )
        advice = get_response(prompt, model=model_choice)
        st.info(advice)

        st.session_state.chat_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id,
            "profile": profile,
            "advice": advice,
            "model": model_choice
        })

# Sidebar - Session Log
st.sidebar.title("🗂 Session Options")
if st.sidebar.button("📜 View Session Log"):
    if st.session_state.chat_history:
        st.sidebar.markdown("### Chat History")
        for entry in st.session_state.chat_history:
            st.sidebar.markdown(f"**🕒 {entry['timestamp']}**")
            st.sidebar.markdown(f"- 👤 **User**: {entry['user_id']}")
            st.sidebar.markdown(f"- ⚙️ **Model**: {entry['model']}")
            st.sidebar.markdown(f"- 💬 **Advice**: {entry['advice']}")
            st.sidebar.markdown("---")
    else:
        st.sidebar.info("No session history yet.")

if st.session_state.chat_history:
    st.sidebar.download_button(
        label="📥 Download Chat History",
        data=json.dumps(st.session_state.chat_history, indent=4),
        file_name="career_mentor_chat_log.json",
        mime="application/json"
    )

if st.session_state.feedback_log:
    st.sidebar.download_button(
        label="📝 Download Feedback Log",
        data=json.dumps(st.session_state.feedback_log, indent=4),
        file_name="career_feedback_log.json",
        mime="application/json"
    )
