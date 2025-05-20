import re
from PyPDF2 import PdfReader

# A sample skill list — expand it as needed
SKILL_KEYWORDS = [
    "python", "java", "c++", "javascript", "sql", "machine learning", "deep learning",
    "aws", "azure", "docker", "kubernetes", "html", "css", "pandas", "numpy", "react",
    "node.js", "data analysis", "data visualization", "linux", "tensorflow", "pytorch"
]

def extract_text_from_pdf(pdf_file) -> str:
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_skills_from_resume(uploaded_file) -> list:
    text = extract_text_from_pdf(uploaded_file).lower()
    found_skills = set()

    for skill in SKILL_KEYWORDS:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)

    return sorted(found_skills)
