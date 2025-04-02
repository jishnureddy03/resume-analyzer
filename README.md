# 💼 Resume Analyzer – Smart Application Toolkit

A Streamlit application that analyzes resumes against job descriptions using AI.  
It provides insights on job fit, missing skills, and personalized improvement tips.

---

## ✨ Features

### ✅ Current
- 📄 Resume text extraction (PDF/DOCX)
- 📝 Job description analysis
- 💪 Strengths identification
- 🧱 Missing skills detection
- 📋 Job fit feedback

### 🔧 Upcoming
- 📊 Skill match score (% fit between resume & JD)
- 🔍 Highlight missing keywords or hard skills
- ✍️ Tailored cover letter generation
- ✨ Resume bullet rewrite suggestions
- 💾 Download/save analysis results
- 💰 Token usage & cost estimator

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Document Processing**: PyPDF2, python-docx
- **AI Integration**: OpenRouter API (using `mistral/mistral-8b`)
- **Backend/Logic**: Python, Pandas

---

## 🚀 Getting Started

```bash
# 1. Clone this repository
git clone https://github.com/jishnureddy03/resume-analyzer.git

# 2. Move into the project directory
cd resume-analyzer

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your OpenRouter API key in .env
echo OPENROUTER_API_KEY=your_key_here > .env

# 5. Run the app
streamlit run app.py
