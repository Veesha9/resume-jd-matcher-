# 📄 Resume vs Job Description Matcher

A web app that analyzes how well a resume matches a job description using NLP techniques — giving you a match score, skill gap analysis, and the ability to compare against multiple job postings at once to find your strongest fit.

**🔗 Live Demo:** [veesha-resume-matcher.streamlit.app](https://veesha-resume-matcher.streamlit.app)

---

## ✨ Features

- **PDF Resume Parsing** — Upload any resume PDF and extract clean, readable text (with automatic fallback extraction for tricky PDFs)
- **NLP Match Scoring** — Uses TF-IDF vectorization + cosine similarity to measure how closely a resume's content overlaps with a job description
- **Skill Gap Analysis** — Detects specific technical and soft skills present in both documents, highlighting:
  - ✅ Skills you have that match the JD
  - ❌ Skills the JD wants that are missing from your resume
  - ➕ Bonus skills on your resume not explicitly asked for
- **Multi-JD Comparison** — Paste multiple job descriptions at once and get a ranked leaderboard showing which role you're the strongest match for
- **Clean, Interactive UI** — Built with Streamlit for an instant, no-install web experience

---

## 🛠️ Tech Stack

| Component            | Technology                          |
|-----------------------|--------------------------------------|
| Frontend / App        | Streamlit                           |
| PDF Text Extraction   | pdfplumber, PyMuPDF (fallback)      |
| NLP / Matching        | scikit-learn (TF-IDF, cosine similarity) |
| Data Handling         | pandas                              |
| Deployment            | Streamlit Community Cloud           |

---

## 🚀 How It Works

1. Upload your resume (PDF)
2. Paste one or more job descriptions
3. Click **Analyze** — the app:
   - Extracts and cleans resume text
   - Converts both documents into TF-IDF vectors
   - Computes cosine similarity for an overall match score
   - Cross-references both texts against a curated list of ~90 common technical and soft skills
4. View your score, skill breakdown, and (if comparing multiple JDs) a ranked list of best-fit roles

---

## 💻 Run It Locally

```bash
git clone https://github.com/Veesha9/resume-jd-matcher-.git
cd resume-jd-matcher-
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
streamlit run app.py
```

---

## 📂 Project Structure

```
resume-matcher/
├── app.py                     # Streamlit app — UI and orchestration
├── requirements.txt           # Python dependencies
└── utils/
    ├── pdf_parser.py          # PDF text extraction + cleaning
    ├── matcher.py              # TF-IDF scoring + skill gap logic
    └── skills_database.py      # Curated list of tech/soft skills
```

---

## 🙋 About

Built by [Veesha Thaker](https://linkedin.com/in/veesha-thaker) as a personal project to solve a real problem faced during internship/job applications — quickly checking resume-JD alignment before applying, and understanding what skills to build next.
