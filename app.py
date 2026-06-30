"""
Resume vs Job Description Matcher
-----------------------------------
A beginner-friendly NLP + Data Analysis project.

What it does:
1. Extracts text from an uploaded resume (PDF)
2. Extracts text from a pasted/uploaded job description
3. Cleans and tokenizes both texts
4. Computes a match score using TF-IDF + Cosine Similarity
5. Finds matched and missing skills using a predefined skills database
6. Visualizes results with matplotlib
7. (Optional) Uses an LLM to suggest resume improvements

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills_data import SKILLS_DB, SKILL_SYNONYMS

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Resume vs JD Matcher", page_icon="📄", layout="wide")
st.title("📄 Resume vs Job Description Matcher")
st.markdown(
    "Upload your resume and paste a job description to see your **match score**, "
    "**matched skills**, and **missing skills** you should add."
)

# ---------------------------------------------------------
# STEP 1: TEXT EXTRACTION
# ---------------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    """Extract raw text from an uploaded PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ---------------------------------------------------------
# STEP 2: TEXT CLEANING
# ---------------------------------------------------------
def clean_text(text):
    """Lowercase, remove special characters and extra whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s+#./-]", " ", text)  # keep tech symbols like c++, c#, .net
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------
# STEP 3: SKILL EXTRACTION
# ---------------------------------------------------------
def extract_skills(text, skills_db, synonyms=None):
    """Find which predefined skills appear in the given text.

    Checks the canonical skill name first, then falls back to checking
    any known alternate phrasings (synonyms) for that skill.
    """
    synonyms = synonyms or {}
    text = text.lower()
    found = set()

    def has_match(phrase):
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(phrase.lower()) + r"(?![a-zA-Z0-9])"
        return re.search(pattern, text) is not None

    for skill in skills_db:
        if has_match(skill):
            found.add(skill)
            continue
        # check synonyms / alternate phrasings for this skill
        for alt_phrase in synonyms.get(skill, []):
            if has_match(alt_phrase):
                found.add(skill)
                break
    return found


# ---------------------------------------------------------
# STEP 4: SIMILARITY SCORE
# ---------------------------------------------------------
def compute_similarity(resume_text, jd_text):
    """TF-IDF + cosine similarity between resume and job description."""
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)


# ---------------------------------------------------------
# STEP 5: VISUALIZATION
# ---------------------------------------------------------
def plot_match_summary(matched_count, missing_count):
    fig, ax = plt.subplots(figsize=(4, 4))
    labels = ["Matched Skills", "Missing Skills"]
    values = [matched_count, missing_count]
    colors = ["#4CAF50", "#E57373"]
    ax.pie(values, labels=labels, autopct="%1.0f%%", colors=colors, startangle=90)
    ax.set_title("Skill Match Breakdown")
    return fig


def plot_top_missing(missing_skills, top_n=10):
    df = pd.DataFrame({"skill": list(missing_skills)})
    df = df.head(top_n)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(df["skill"], range(len(df), 0, -1), color="#E57373")
    ax.set_xlabel("Priority (higher = add first)")
    ax.set_title(f"Top Missing Skills to Add")
    ax.invert_yaxis()
    return fig


# ---------------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------------
st.sidebar.header("Inputs")
resume_file = st.sidebar.file_uploader("Upload your Resume (PDF)", type=["pdf"])
jd_text_input = st.sidebar.text_area("Paste the Job Description here", height=300)
analyze_btn = st.sidebar.button("🔍 Analyze Match")

# ---------------------------------------------------------
# MAIN LOGIC
# ---------------------------------------------------------
if analyze_btn:
    if not resume_file:
        st.error("Please upload your resume PDF.")
    elif not jd_text_input.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analyzing..."):
            # Extract & clean
            raw_resume_text = extract_text_from_pdf(resume_file)
            resume_clean = clean_text(raw_resume_text)
            jd_clean = clean_text(jd_text_input)

            # Similarity score
            match_score = compute_similarity(resume_clean, jd_clean)

            # Skill extraction
            resume_skills = extract_skills(resume_clean, SKILLS_DB, SKILL_SYNONYMS)
            jd_skills = extract_skills(jd_clean, SKILLS_DB, SKILL_SYNONYMS)

            matched_skills = resume_skills.intersection(jd_skills)
            missing_skills = jd_skills.difference(resume_skills)

        # ---------------- RESULTS ----------------
        st.header("Results")

        col1, col2, col3 = st.columns(3)
        col1.metric("Overall Match Score", f"{match_score}%")
        col2.metric("Skills Matched", len(matched_skills))
        col3.metric("Skills Missing", len(missing_skills))

        st.progress(min(int(match_score), 100))

        col4, col5 = st.columns(2)
        with col4:
            st.subheader("Skill Match Breakdown")
            if matched_skills or missing_skills:
                fig1 = plot_match_summary(len(matched_skills), len(missing_skills))
                st.pyplot(fig1)
            else:
                st.info("No predefined skills detected in either document. Try a more detailed JD.")

        with col5:
            st.subheader("Top Missing Skills")
            if missing_skills:
                fig2 = plot_top_missing(missing_skills)
                st.pyplot(fig2)
            else:
                st.success("No missing skills detected! 🎉")

        st.subheader("✅ Matched Skills")
        st.write(", ".join(sorted(matched_skills)) if matched_skills else "None found.")

        st.subheader("❌ Missing Skills (consider adding these)")
        st.write(", ".join(sorted(missing_skills)) if missing_skills else "None — great coverage!")

        # ---------------- DATA TABLE ----------------
        st.subheader("📊 Detailed Skill Table")
        all_skills = sorted(resume_skills.union(jd_skills))
        df = pd.DataFrame({
            "Skill": all_skills,
            "In Resume": ["Yes" if s in resume_skills else "No" for s in all_skills],
            "In Job Description": ["Yes" if s in jd_skills else "No" for s in all_skills],
        })
        df.index = df.index + 1          # start S.No. at 1 instead of 0
        df.index.name = "S.No."
        st.dataframe(df, use_container_width=True)

        # utf-8-sig adds a BOM so Excel auto-detects UTF-8 and won't garble special characters
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("Download Skill Report as CSV", csv, "skill_report.csv", "text/csv")

else:
    st.info("👈 Upload a resume and paste a job description, then click **Analyze Match**.")