# 📄 Resume Analyzer Pro

**Resume Analyzer Pro** is a modern, offline, Streamlit-based app that helps you analyze and optimize your resume against any job description.

It gives you:
- 🎯 Job match percentage
- 🤖 ATS-style compatibility score
- 🛠️ Technical vs soft skill breakdown
- 📋 Quality checklist (structure, metrics, formatting)
- 🔒 Privacy scan (SSN, address, contact info)
- 💡 Personalized, actionable improvement tips

All analysis runs **locally** on your machine — no API keys, no external calls.

---

## 🚀 Features

### 1. Smart Job Matching
- Compares your resume against a pasted job description
- Extracts meaningful keywords from both
- Calculates a **Job Match %** based on important technical and soft skills

### 2. ATS Compatibility Check
- Flags:
  - Missing section headers (Experience, Education, Skills)
  - Missing dates
  - Missing bullet points
  - Overly long resumes
- Produces an **ATS Score /100** with clear warnings

### 3. Skills Distribution
- Detects:
  - ✅ Technical skills (Python, SQL, AWS, Tableau, etc.)
  - ✅ Soft skills (leadership, communication, teamwork, etc.)
- Shows the balance between technical and soft skills

### 4. Resume Quality Checklist
Checks for:
- Contact information
- Professional summary
- Bullet points
- Employment dates
- Quantified achievements
- Education & skills sections
- Appropriate length (1–2 pages)
- Basic formatting and action verbs

### 5. Privacy & Security
- Warns if:
  - Social Security Number–like patterns appear
  - Full street address is included
- Confirms presence of:
  - Phone number
  - Email address
- Includes best practices for safe resume sharing

### 6. Personalized Tips
- Generates tailored suggestions such as:
  - Add more job-specific keywords
  - Improve ATS structure
  - Add metrics and impact
  - Highlight more technical/soft skills
  - Adjust resume length

---

## 🧱 Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **Language**: Python
- **Libraries**:
  - `PyPDF2` – PDF parsing
  - `python-docx` – DOCX parsing
  - `scikit-learn` – stopword list (ENGLISH_STOP_WORDS)
  - `re`, `hashlib`, `collections` – keyword & text processing
  - `pandas`, `plotly` – analytics & visualization-ready

> 🔐 No API keys required. Everything is processed locally.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/resume-analyzer.git
cd resume-analyzer

