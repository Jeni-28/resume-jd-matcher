# 📄 Resume vs Job Description Matcher
## Screenshots
![Demo](screenshots/Demo.png)
![Result1](screenshots/Result1.png)
![Result2](screenshots/Result2.png)
![Result3](screenshots/Result3.png)

A Streamlit web app that compares a resume against a job description, generates a match score, and highlights which skills are present or missing — helping job seekers tailor their resumes more effectively.

## Features

- Upload a resume in PDF format and paste any job description
- Calculates an overall match score using TF-IDF + Cosine Similarity
- Detects relevant skills in both documents using a predefined skill list with synonym matching (e.g. "AWS" also matches "Amazon Web Services")
- Visualizes results with a skill match pie chart and a missing-skills bar chart
- Displays a detailed skill comparison table
- Exports results as a downloadable CSV report

## Tech Stack

- **Python**
- **Streamlit** — interactive web app interface
- **pandas / numpy** — data handling
- **matplotlib** — visualizations
- **scikit-learn** — TF-IDF vectorization and cosine similarity
- **pdfplumber** — PDF text extraction

## Project Structure

```
resume-jd-matcher/
├── app.py             # Main Streamlit application
├── skills_data.py     # Predefined skills list + synonym mappings
├── requirements.txt   # Python dependencies
└── README.md
```

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/resume-jd-matcher.git
   cd resume-jd-matcher
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```
   The app will open automatically at `http://localhost:8501`.

## How to Use

1. Upload your resume as a PDF in the sidebar.
2. Paste a job description (e.g. from LinkedIn, Naukri, or Indeed) into the text box.
3. Click **Analyze Match**.
4. Review your match score, matched/missing skills, visual charts, and the detailed comparison table.
5. Download the results as a CSV report if needed.

## How the Core Logic Works (Explained Simply)

1. **Reading the resume** — The app opens the uploaded PDF resume and reads all the text from it, page by page, using a tool called `pdfplumber`.
2. **Cleaning the text** — The text is converted to lowercase and extra symbols/punctuation are removed, so the app can compare words fairly. A few special symbols like `+`, `#`, and `.` are kept so that tech terms like `C++`, `C#`, and `.NET` don't get broken or misread.
3. **Finding skills** — The app has a list of about 70 common skills (stored in `skills_data.py`). It scans both the resume and the job description to check which of these skills appear in each one. It can also recognize different ways of writing the same skill — for example, "data viz" and "data visualization" are treated as the same thing.
4. **Calculating the match score** — The app turns both documents into number-based representations of the words they use (this is called TF-IDF) and then compares how similar those representations are (this is called cosine similarity). The result is a percentage score showing how closely the resume matches the job description. This is the same basic idea used by search engines to match your search query with relevant web pages.
5. **Comparing skills** — Once the app knows which skills are in the resume and which are in the job description, it simply compares the two lists: skills found in both = "matched skills", skills found only in the job description = "missing skills".
6. **Showing the results visually** — The app uses `matplotlib` to draw a pie chart (showing how many skills matched vs. how many are missing) and a bar chart (showing which missing skills to prioritize adding to your resume).

## Future Improvements

- Use an AI language model (LLM) to suggest ready-made resume bullet points based on the skills that are missing
- Make skill detection smarter by using NLP tools (like spaCy) to automatically spot skills, instead of only checking against a fixed list
- Allow comparing multiple versions of a resume against one job description, to see which version scores the best
- Put the app online (deploy it) using Streamlit Community Cloud, so anyone can use it from a link without installing anything

