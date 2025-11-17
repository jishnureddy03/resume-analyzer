import streamlit as st
import PyPDF2
import docx
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter, defaultdict
from datetime import datetime
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import io
import string
import hashlib

# Page config
st.set_page_config(
    page_title="Resume Analyzer Pro",
    layout="wide",
    page_icon="📄",
    initial_sidebar_state="expanded"
)

# 🎨 ENHANCED COLOR PALETTE
PRIMARY_COLOR = "#6366F1"        # Indigo
SECONDARY_COLOR = "#8B5CF6"      # Violet
BACKGROUND_COLOR = "#0A0E27"     # Deep navy
CARD_BACKGROUND = "#1A1F3A"      # Dark slate blue
TEXT_COLOR = "#E2E8F0"           # Light slate
SUCCESS_COLOR = "#10B981"        # Emerald
WARNING_COLOR = "#F59E0B"        # Amber
ERROR_COLOR = "#EF4444"          # Red
INFO_COLOR = "#3B82F6"           # Blue
ACCENT_COLOR = "#EC4899"         # Pink
NEUTRAL_COLOR = "#94A3B8"        # Slate gray

# Enhanced CSS with Poppins font and improved animations
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {BACKGROUND_COLOR} 0%, #0F1419 100%);
    }}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {BACKGROUND_COLOR};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {PRIMARY_COLOR};
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {SECONDARY_COLOR};
    }}
    
    .main-header {{
        text-align: center;
        color: #FFFFFF;
        font-size: 4rem;
        margin-bottom: 0.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR}, {ACCENT_COLOR});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
        animation: fadeInDown 0.8s ease-out;
    }}
    
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .sub-header {{
        text-align: center;
        color: {NEUTRAL_COLOR};
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 400;
        letter-spacing: 0.5px;
        animation: fadeIn 1s ease-out;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
        padding: 2rem 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }}
    
    .metric-card:hover::before {{
        left: 100%;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.4);
    }}
    
    .metric-card h3 {{
        margin: 0 0 0.8rem 0;
        font-size: 0.95rem;
        opacity: 0.95;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .metric-card h2 {{
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }}
    
    .section-header {{
        color: {TEXT_COLOR};
        font-size: 2.5rem;
        font-weight: 700;
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 3px solid {PRIMARY_COLOR};
        position: relative;
        letter-spacing: -0.5px;
    }}
    
    .section-header::after {{
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 80px;
        height: 3px;
        background: {ACCENT_COLOR};
    }}
    
    .subsection-header {{
        color: {TEXT_COLOR};
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2.5rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }}
    
    .analysis-card {{
        background: {CARD_BACKGROUND};
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        color: {TEXT_COLOR};
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }}
    
    .analysis-card:hover {{
        border-color: {PRIMARY_COLOR};
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.2);
        transform: translateY(-2px);
    }}
    
    .warning-card {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
        border: 1px solid {WARNING_COLOR};
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #FCD34D;
        border-left: 4px solid {WARNING_COLOR};
        transition: all 0.3s ease;
    }}
    
    .warning-card:hover {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.08) 100%);
        transform: translateX(5px);
    }}
    
    .success-card {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid {SUCCESS_COLOR};
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #6EE7B7;
        border-left: 4px solid {SUCCESS_COLOR};
        transition: all 0.3s ease;
    }}
    
    .success-card:hover {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%);
        transform: translateX(5px);
    }}
    
    .info-card {{
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
        border: 1px solid {INFO_COLOR};
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #93C5FD;
        border-left: 4px solid {INFO_COLOR};
    }}
    
    .keyword-tag {{
        display: inline-block;
        background: linear-gradient(135deg, {SUCCESS_COLOR}, #059669);
        color: white;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
        transition: all 0.2s ease;
    }}
    
    .keyword-tag:hover {{
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }}
    
    .missing-keyword-tag {{
        display: inline-block;
        background: linear-gradient(135deg, {WARNING_COLOR}, #D97706);
        color: white;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
        transition: all 0.2s ease;
    }}
    
    .missing-keyword-tag:hover {{
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
    }}
    
    .checklist-item {{
        display: flex;
        align-items: center;
        padding: 0.8rem 0;
        font-size: 1.05rem;
        color: {TEXT_COLOR};
        border-bottom: 1px solid rgba(99, 102, 241, 0.1);
        transition: all 0.2s ease;
    }}
    
    .checklist-item:hover {{
        background: rgba(99, 102, 241, 0.05);
        padding-left: 1rem;
    }}
    
    .checklist-item:last-child {{
        border-bottom: none;
    }}
    
    .checklist-icon {{
        margin-right: 1rem;
        font-size: 1.3rem;
    }}
    
    .tips-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }}
    
    .tip-card {{
        background: {CARD_BACKGROUND};
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 2rem;
        color: {TEXT_COLOR};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .tip-card:hover {{
        transform: translateY(-5px);
        border-color: {PRIMARY_COLOR};
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.3);
        background: linear-gradient(135deg, {CARD_BACKGROUND} 0%, rgba(99, 102, 241, 0.1) 100%);
    }}
    
    .tip-icon {{
        font-size: 2.2rem;
        margin-bottom: 1rem;
    }}
    
    .tip-title {{
        font-weight: 600;
        color: {PRIMARY_COLOR};
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }}
    
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {PRIMARY_COLOR}, {SECONDARY_COLOR}, {ACCENT_COLOR});
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.8rem;
        background-color: {CARD_BACKGROUND};
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        color: {NEUTRAL_COLOR};
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(99, 102, 241, 0.1);
        color: {TEXT_COLOR};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }}
    
    .priority-action {{
        background: {CARD_BACKGROUND};
        border: 1px solid {WARNING_COLOR};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: {TEXT_COLOR};
        border-left: 4px solid {WARNING_COLOR};
        font-size: 1.05rem;
        line-height: 1.6;
        transition: all 0.3s ease;
    }}
    
    .priority-action:hover {{
        transform: translateX(5px);
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.2);
    }}
    
    .priority-action.success {{
        border-color: {SUCCESS_COLOR};
        border-left-color: {SUCCESS_COLOR};
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, {CARD_BACKGROUND} 100%);
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {CARD_BACKGROUND} 0%, {BACKGROUND_COLOR} 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }}
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: {TEXT_COLOR};
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }}
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {{
        background: rgba(99, 102, 241, 0.05);
        border: 2px dashed {PRIMARY_COLOR};
        border-radius: 12px;
        padding: 1.5rem;
    }}
    
    /* Text area styling */
    .stTextArea textarea {{
        background: {BACKGROUND_COLOR};
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 10px;
        color: {TEXT_COLOR};
        font-family: 'Poppins', sans-serif;
    }}
    
    .stTextArea textarea:focus {{
        border-color: {PRIMARY_COLOR};
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }}
</style>
""", unsafe_allow_html=True)

# Utility Functions


class ResumeAnalyzer:
    def __init__(self):
        self.stop_words = ENGLISH_STOP_WORDS
        self.technical_keywords = {
            'python', 'java', 'javascript', 'react', 'sql', 'aws', 'azure', 'docker',
            'kubernetes', 'machine learning', 'data science', 'api', 'git', 'agile',
            'tensorflow', 'pandas', 'numpy', 'mongodb', 'postgresql', 'redis', 'kafka',
            'html', 'css', 'nodejs', 'angular', 'vue', 'django', 'flask', 'spring',
            'typescript', 'graphql', 'rest', 'microservices', 'ci/cd', 'jenkins',
            'tableau', 'powerbi', 'excel', 'spark', 'hadoop', 'scala', 'ruby', 'php',
            'c++', 'c#', '.net', 'golang', 'rust', 'swift', 'kotlin', 'flutter'
        }
        self.soft_skills = {
            'leadership', 'communication', 'teamwork', 'problem solving', 'creativity',
            'analytical', 'management', 'collaboration', 'presentation', 'negotiation',
            'critical thinking', 'time management', 'adaptability', 'mentoring',
            'strategic planning', 'decision making', 'conflict resolution', 'empathy'
        }

    def extract_text_from_file(self, file):
        """Extract text from PDF or DOCX file"""
        text = ""
        try:
            if file.type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(file)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
        return text

    def extract_keywords(self, text):
        """Extract meaningful keywords from text with better filtering"""
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())

        excluded = self.stop_words.union({
            'resume', 'experience', 'work', 'job', 'company', 'year', 'years',
            'will', 'able', 'strong', 'good', 'excellent', 'required', 'preferred',
            'candidate', 'position', 'role', 'responsibilities', 'requirements',
            'qualifications', 'skills', 'knowledge', 'ability', 'experience',
            'working', 'including', 'related', 'plus', 'bonus', 'nice', 'have'
        })

        keywords = [
            word for word in words if word not in excluded and len(word) > 2]
        phrases = self.extract_technical_phrases(text)
        keywords.extend(phrases)

        return set(keywords)

    def extract_technical_phrases(self, text):
        """Extract common technical phrases and skills"""
        text_lower = text.lower()
        phrases = []

        technical_phrases = [
            'machine learning', 'data science', 'artificial intelligence', 'deep learning',
            'web development', 'full stack', 'front end', 'back end', 'software development',
            'project management', 'agile methodology', 'scrum master', 'product management',
            'cloud computing', 'devops', 'continuous integration', 'version control',
            'database design', 'data analysis', 'business intelligence', 'big data',
            'user experience', 'user interface', 'ui/ux', 'graphic design',
            'digital marketing', 'social media', 'content marketing', 'seo',
            'financial analysis', 'risk management', 'quality assurance', 'test automation',
            'natural language processing', 'computer vision', 'data engineering',
            'business analysis', 'stakeholder management', 'change management'
        ]

        for phrase in technical_phrases:
            if phrase in text_lower:
                phrases.append(phrase.replace(' ', '_'))

        return phrases

    def calculate_keyword_match(self, resume_text, job_text):
        """Calculate keyword match percentage with improved analysis"""
        resume_keywords = self.extract_keywords(resume_text)
        job_keywords = self.extract_keywords(job_text)

        if not job_keywords:
            return 0, set(), set()

        job_word_freq = Counter(re.findall(
            r'\b[a-zA-Z]{3,}\b', job_text.lower()))

        important_job_keywords = set()
        for keyword in job_keywords:
            keyword_clean = keyword.replace('_', ' ')
            freq = job_word_freq.get(keyword, 1)

            if (keyword in self.technical_keywords or
                keyword in self.soft_skills or
                freq > 2 or
                    any(tech in keyword for tech in ['python', 'java', 'sql', 'aws', 'react'])):
                important_job_keywords.add(keyword)

        if not important_job_keywords:
            important_job_keywords = set(
                list(job_keywords)[:min(20, len(job_keywords))])

        matched = resume_keywords.intersection(important_job_keywords)
        missing = important_job_keywords - resume_keywords

        if important_job_keywords:
            match_percentage = (
                len(matched) / len(important_job_keywords)) * 100
        else:
            match_percentage = 0

        return round(match_percentage, 1), matched, missing

    def count_skills(self, resume_text):
        """Count technical vs soft skills"""
        text_lower = resume_text.lower()
        tech_count = sum(
            1 for skill in self.technical_keywords if skill in text_lower)
        soft_count = sum(
            1 for skill in self.soft_skills if skill in text_lower)
        return tech_count, soft_count

    def check_ats_compatibility(self, resume_text):
        """Check ATS compatibility and return score with flags"""
        flags = []
        score = 100

        sections = ['experience', 'education', 'skills']
        found_sections = sum(
            1 for section in sections if section in resume_text.lower())
        if found_sections < 3:
            flags.append(
                "Missing clear section headers (Experience, Education, Skills)")
            score -= 20

        if not re.search(r'[•·\-\*]\s+', resume_text):
            flags.append(
                "No bullet points detected - use bullets for better parsing")
            score -= 15

        if not re.search(r'\d{4}', resume_text):
            flags.append("No dates found - include employment dates")
            score -= 20

        if len(resume_text.split()) > 800:
            flags.append("Resume may be too long - consider shortening")
            score -= 10

        return max(score, 0), flags

    def resume_checklist(self, resume_text):
        """Generate resume quality checklist"""
        checklist = {}
        text_lower = resume_text.lower()

        checklist['Contact information included'] = bool(
            re.search(r'@|\(\d{3}\)|\d{3}-\d{3}-\d{4}', resume_text))
        checklist['Professional summary present'] = any(
            word in text_lower for word in ['summary', 'objective', 'profile'])
        checklist['Uses bullet points effectively'] = bool(
            re.search(r'[•·\-\*]\s+', resume_text))
        checklist['Employment dates included'] = bool(
            re.search(r'\d{4}', resume_text))
        checklist['Quantifiable achievements shown'] = bool(
            re.search(r'\d+%|\$\d+|\d+\+|increased|improved|reduced', resume_text))
        checklist['Education section complete'] = any(word in text_lower for word in [
                                                      'education', 'degree', 'university', 'college'])
        checklist['Skills clearly listed'] = 'skill' in text_lower
        checklist['Appropriate length (1-2 pages)'] = 200 <= len(
            resume_text.split()) <= 600
        checklist['Professional formatting'] = len(
            re.findall(r'\n\s*\n', resume_text)) >= 3
        checklist['Action verbs used'] = bool(re.search(
            r'\b(managed|led|developed|created|implemented|achieved|improved)\b', text_lower))

        return checklist

    def privacy_check(self, resume_text):
        """Enhanced privacy check with recommendations"""
        findings = []

        if re.search(r'\d{3}-\d{2}-\d{4}', resume_text):
            findings.append(("🚨", "Social Security Number detected",
                            "REMOVE - Never include SSN on resumes"))

        if re.search(r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln)', resume_text):
            findings.append(("⚠️", "Full street address found",
                            "OPTIONAL - City, State is usually sufficient"))

        if re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', resume_text):
            findings.append(("✅", "Phone number included",
                            "GOOD - Professional contact method"))

        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            findings.append(("✅", "Email address included",
                            "GOOD - Essential for contact"))

        return findings


def create_content_hash(resume_file, job_description):
    """Create a hash of the current content to detect changes"""
    content = f"{resume_file.name}_{resume_file.size}_{job_description}"
    return hashlib.md5(content.encode()).hexdigest()

# Main App


def main():
    # Header
    st.markdown('<h1 class="main-header">📄 Resume Analyzer Pro</h1>',
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Resume Analysis & Career Optimization</p>',
                unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("### 🔧 Configuration")

    # Industry selection
    industries = [
        "Technology", "Marketing", "Finance", "Healthcare", "Education",
        "Engineering", "Design", "Sales", "Consulting", "General"
    ]

    industry = st.sidebar.selectbox(
        "🎯 Target Industry:",
        industries,
        help="Select your target industry for specialized analysis"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📁 Upload Resume")

    resume_file = st.sidebar.file_uploader(
        "Choose your resume file:",
        type=['pdf', 'docx'],
        help="Upload PDF or Word document"
    )

    st.sidebar.markdown("### 📝 Job Description")
    job_description = st.sidebar.text_area(
        "Paste the job description here:",
        height=150,
        help="Copy and paste the complete job posting",
        key="job_description_input"
    )

    # Analysis trigger
    analysis_ready = False
    if job_description and resume_file:
        analysis_ready = True
        st.sidebar.markdown("---")
        st.sidebar.success("✅ **Ready for Analysis!**")
        if st.sidebar.button("🚀 Analyze Resume", key="analyze_btn", use_container_width=True):
            # Clear old results to force fresh analysis
            if 'analysis_results' in st.session_state:
                del st.session_state.analysis_results
            if 'content_hash' in st.session_state:
                del st.session_state.content_hash
            st.session_state.analysis_triggered = True
            st.rerun()
    elif job_description:
        st.sidebar.info("📄 Upload your resume to begin")
    elif resume_file:
        st.sidebar.info("📝 Add job description to begin")

    # Initialize analyzer
    analyzer = ResumeAnalyzer()

    # Main content area
    if analysis_ready and (st.session_state.get('analysis_triggered', False) or 'analysis_results' in st.session_state):
        # Extract resume text
        resume_text = analyzer.extract_text_from_file(resume_file)

        if not resume_text.strip():
            st.error(
                "❌ Could not extract text from resume. Please check the file format.")
            return

        # Create content hash
        current_hash = create_content_hash(resume_file, job_description)

        # Check if we need fresh analysis
        need_reanalysis = (
            'analysis_results' not in st.session_state or
            st.session_state.get('content_hash') != current_hash
        )

        if need_reanalysis:
            # Clear trigger flag
            if 'analysis_triggered' in st.session_state:
                del st.session_state.analysis_triggered

            # Perform analysis with progress
            with st.spinner('🔄 Analyzing your resume...'):
                progress_bar = st.progress(0)

                progress_bar.progress(15, "🔍 Extracting keywords...")
                match_percentage, matched_keywords, missing_keywords = analyzer.calculate_keyword_match(
                    resume_text, job_description)

                progress_bar.progress(35, "🤖 Checking ATS compatibility...")
                ats_score, ats_flags = analyzer.check_ats_compatibility(
                    resume_text)

                progress_bar.progress(55, "🛠️ Counting skills...")
                tech_count, soft_count = analyzer.count_skills(resume_text)

                progress_bar.progress(75, "📊 Analyzing structure...")
                checklist = analyzer.resume_checklist(resume_text)

                progress_bar.progress(90, "🔒 Privacy check...")
                privacy_findings = analyzer.privacy_check(resume_text)

                progress_bar.progress(100, "✅ Complete!")

                # Store results
                st.session_state.analysis_results = {
                    'resume_text': resume_text,
                    'match_percentage': match_percentage,
                    'matched_keywords': matched_keywords,
                    'missing_keywords': missing_keywords,
                    'ats_score': ats_score,
                    'ats_flags': ats_flags,
                    'tech_count': tech_count,
                    'soft_count': soft_count,
                    'checklist': checklist,
                    'privacy_findings': privacy_findings
                }
                st.session_state.content_hash = current_hash

                progress_bar.empty()
                st.success("✅ Analysis complete!", icon="✨")

        results = st.session_state.analysis_results

        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", "🔍 Keywords", "📋 Quality Check",
            "🔒 Privacy", "💡 Tips"
        ])

        with tab1:
            st.markdown(
                '<h2 class="section-header">📊 Resume Overview</h2>', unsafe_allow_html=True)

            # Key metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f'''
                <div class="metric-card">
                    <h3>🎯 Job Match</h3>
                    <h2>{results["match_percentage"]}%</h2>
                </div>
                ''', unsafe_allow_html=True)

            with col2:
                st.markdown(f'''
                <div class="metric-card">
                    <h3>🤖 ATS Score</h3>
                    <h2>{results["ats_score"]}/100</h2>
                </div>
                ''', unsafe_allow_html=True)

            with col3:
                quality_score = round(
                    (sum(results["checklist"].values()) / len(results["checklist"])) * 100)
                st.markdown(f'''
                <div class="metric-card">
                    <h3>✅ Quality</h3>
                    <h2>{quality_score}%</h2>
                </div>
                ''', unsafe_allow_html=True)

            with col4:
                total_skills = results["tech_count"] + results["soft_count"]
                st.markdown(f'''
                <div class="metric-card">
                    <h3>🛠️ Total Skills</h3>
                    <h2>{total_skills}</h2>
                </div>
                ''', unsafe_allow_html=True)

            # Skills breakdown
            st.markdown(
                '<h3 class="subsection-header">🛠️ Skills Distribution</h3>', unsafe_allow_html=True)

            if results["tech_count"] > 0 or results["soft_count"] > 0:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f'''
                    <div class="analysis-card" style="text-align: center;">
                        <h4 style="color: {PRIMARY_COLOR}; margin-bottom: 1rem; font-size: 1.3rem;">🔧 Technical Skills</h4>
                        <div style="font-size: 3rem; font-weight: 800; color: {TEXT_COLOR}; margin: 1rem 0;">{results["tech_count"]}</div>
                        <div style="color: {NEUTRAL_COLOR}; font-size: 1rem;">Programming, tools, technologies</div>
                    </div>
                    ''', unsafe_allow_html=True)

                with col2:
                    st.markdown(f'''
                    <div class="analysis-card" style="text-align: center;">
                        <h4 style="color: {SECONDARY_COLOR}; margin-bottom: 1rem; font-size: 1.3rem;">🤝 Soft Skills</h4>
                        <div style="font-size: 3rem; font-weight: 800; color: {TEXT_COLOR}; margin: 1rem 0;">{results["soft_count"]}</div>
                        <div style="color: {NEUTRAL_COLOR}; font-size: 1rem;">Leadership, communication, teamwork</div>
                    </div>
                    ''', unsafe_allow_html=True)

                # Skills balance bar
                total_skills = results["tech_count"] + results["soft_count"]
                if total_skills > 0:
                    tech_percentage = (
                        results["tech_count"] / total_skills) * 100
                    soft_percentage = (
                        results["soft_count"] / total_skills) * 100

                    st.markdown(f'''
                    <div class="analysis-card">
                        <h5 style="margin-bottom: 1.5rem; color: {TEXT_COLOR}; font-size: 1.2rem;">Skills Balance</h5>
                        <div style="display: flex; height: 40px; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                            <div style="width: {tech_percentage}%; background: linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR}); display: flex; align-items: center; justify-content: center; color: white; font-size: 0.9rem; font-weight: 700;">
                                {f"Technical {tech_percentage:.0f}%" if tech_percentage > 15 else ""}
                            </div>
                            <div style="width: {soft_percentage}%; background: linear-gradient(135deg, {SECONDARY_COLOR}, {ACCENT_COLOR}); display: flex; align-items: center; justify-content: center; color: white; font-size: 0.9rem; font-weight: 700;">
                                {f"Soft {soft_percentage:.0f}%" if soft_percentage > 15 else ""}
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="warning-card">
                    <h4 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">⚠️ No Recognizable Skills Detected</h4>
                    <p style="margin: 0;">Consider adding specific technical skills (Python, SQL, AWS) and soft skills (leadership, communication) to your resume.</p>
                </div>
                ''', unsafe_allow_html=True)

            # Resume strength indicators
            st.markdown(
                '<h3 class="subsection-header">📊 Resume Strength Indicators</h3>', unsafe_allow_html=True)

            word_count = len(results["resume_text"].split())
            has_quantifiable = bool(re.search(
                r'\d+%|\$\d+|\d+\+|increased|improved|reduced', results["resume_text"]))
            has_action_verbs = bool(re.search(
                r'\b(managed|led|developed|created|implemented|achieved|improved)\b', results["resume_text"].lower()))

            indicators = [
                ("📏", "Resume Length", f"{word_count} words",
                 "optimal" if 200 <= word_count <= 600 else "warning"),
                ("🎯", "Job Relevance", f"{results['match_percentage']}%",
                 "optimal" if results['match_percentage'] > 30 else "warning"),
                ("📊", "Has Metrics", "Yes" if has_quantifiable else "Missing",
                 "optimal" if has_quantifiable else "warning"),
                ("⚡", "Action Verbs", "Used" if has_action_verbs else "Missing",
                 "optimal" if has_action_verbs else "warning"),
            ]

            cols = st.columns(4)
            for i, (icon, label, value, status) in enumerate(indicators):
                color = SUCCESS_COLOR if status == "optimal" else WARNING_COLOR
                with cols[i]:
                    st.markdown(f'''
                    <div class="analysis-card" style="text-align: center; border-left: 4px solid {color};">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                        <div style="font-size: 0.85rem; color: {NEUTRAL_COLOR}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
                        <div style="font-weight: 700; color: {color}; font-size: 1.2rem;">{value}</div>
                    </div>
                    ''', unsafe_allow_html=True)

        with tab2:
            st.markdown(
                '<h2 class="section-header">🔍 Keyword Analysis</h2>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    '<h3 class="subsection-header">✅ Matched Keywords</h3>', unsafe_allow_html=True)
                if results["matched_keywords"]:
                    matched_html = ""
                    for keyword in sorted(list(results["matched_keywords"]))[:30]:
                        display_keyword = keyword.replace('_', ' ').title()
                        matched_html += f'<span class="keyword-tag">{display_keyword}</span>'
                    st.markdown(
                        f'<div class="analysis-card">{matched_html}</div>', unsafe_allow_html=True)
                    st.success(
                        f"✨ Found {len(results['matched_keywords'])} matching keywords")
                else:
                    st.markdown(
                        '<div class="info-card">No matching keywords found. Consider reviewing the job description.</div>', unsafe_allow_html=True)

            with col2:
                st.markdown(
                    '<h3 class="subsection-header">❌ Missing Keywords</h3>', unsafe_allow_html=True)
                if results["missing_keywords"]:
                    missing_html = ""
                    for keyword in sorted(list(results["missing_keywords"]))[:30]:
                        display_keyword = keyword.replace('_', ' ').title()
                        missing_html += f'<span class="missing-keyword-tag">{display_keyword}</span>'
                    st.markdown(
                        f'<div class="analysis-card">{missing_html}</div>', unsafe_allow_html=True)
                    st.warning(
                        f"⚠️ Missing {len(results['missing_keywords'])} important keywords")
                else:
                    st.markdown(
                        '<div class="success-card">🎉 Excellent! All important keywords are present.</div>', unsafe_allow_html=True)

            # ATS compatibility
            st.markdown(
                '<h3 class="subsection-header">🤖 ATS Compatibility</h3>', unsafe_allow_html=True)
            if results["ats_flags"]:
                for flag in results["ats_flags"]:
                    st.markdown(
                        f'<div class="warning-card">⚠️ {flag}</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div class="success-card">✅ No major ATS issues detected! Your resume should parse well.</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown(
                '<h2 class="section-header">📋 Quality Assessment</h2>', unsafe_allow_html=True)

            checked_items = sum(results["checklist"].values())
            total_items = len(results["checklist"])
            score_percentage = (checked_items / total_items) * 100

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f'''
                <div class="metric-card" style="margin: 1rem 0 2rem 0;">
                    <h3>📊 Quality Score</h3>
                    <h2>{checked_items}/{total_items}</h2>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.1rem;">{score_percentage:.0f}% Complete</p>
                </div>
                ''', unsafe_allow_html=True)

            st.progress(checked_items / total_items)

            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            for item, status in results["checklist"].items():
                icon = "✅" if status else "❌"
                st.markdown(f'''
                <div class="checklist-item">
                    <span class="checklist-icon">{icon}</span>
                    <span>{item}</span>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown(
                '<h2 class="section-header">🔒 Privacy & Security</h2>', unsafe_allow_html=True)

            if results["privacy_findings"]:
                for icon, finding, recommendation in results["privacy_findings"]:
                    color_class = "success-card" if icon == "✅" else "warning-card"
                    st.markdown(f'''
                    <div class="{color_class}">
                        <span style="margin-right: 0.8rem; font-size: 1.4rem;">{icon}</span>
                        <strong style="font-size: 1.1rem;">{finding}:</strong> {recommendation}
                    </div>
                    ''', unsafe_allow_html=True)

                st.markdown(f'''
                <div class="info-card">
                    <h4 style="margin: 0 0 1rem 0; font-size: 1.2rem;">📋 Privacy Best Practices:</h4>
                    <ul style="margin: 0; padding-left: 1.5rem; line-height: 1.8;">
                        <li><strong>Essential:</strong> Phone number and professional email</li>
                        <li><strong>Recommended:</strong> City, State (no full address needed)</li>
                        <li><strong>Never include:</strong> SSN, personal ID numbers, or sensitive data</li>
                        <li><strong>LinkedIn:</strong> Add your profile URL for professional networking</li>
                    </ul>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div class="info-card">🔍 No personal information detected in analysis.</div>', unsafe_allow_html=True)

        with tab5:
            st.markdown(
                '<h2 class="section-header">💡 Improvement Tips</h2>', unsafe_allow_html=True)

            # Personalized tips
            personalized_tips = []

            if results["match_percentage"] < 50:
                personalized_tips.append(("🎯", "Optimize Keywords for This Job",
                                         f"Your resume matches only {results['match_percentage']}% of job keywords. Include more specific terms from the job posting in your experience bullets."))

            if results["ats_score"] < 80:
                personalized_tips.append(
                    ("🤖", "Fix ATS Issues", f"Your ATS score is {results['ats_score']}/100. Use standard section headers, add bullet points, and include employment dates to improve parsing."))

            if not re.search(r'\d+%|\$\d+|\d+\+|increased|improved|reduced', results["resume_text"]):
                personalized_tips.append(
                    ("📊", "Add Quantifiable Results", "Include specific numbers and percentages to show your impact: 'Increased sales by 25%' or 'Managed budget of $50K'."))

            if results["tech_count"] < 3:
                personalized_tips.append(
                    ("💻", "Highlight Technical Skills", "Add more relevant technical skills to match industry standards. List specific tools, programming languages, or software you've used."))

            if results["soft_count"] < 2:
                personalized_tips.append(
                    ("🤝", "Showcase Soft Skills", "Demonstrate leadership, communication, and teamwork abilities through specific examples in your experience section."))

            word_count = len(results["resume_text"].split())
            if word_count > 600:
                personalized_tips.append(
                    ("✂️", "Shorten Your Resume", f"Your resume has {word_count} words. Consider condensing to 1-2 pages (300-500 words) for better readability."))
            elif word_count < 200:
                personalized_tips.append(
                    ("📝", "Add More Detail", f"Your resume has only {word_count} words. Add more specific achievements and responsibilities to strengthen your candidacy."))

            if personalized_tips:
                st.markdown(
                    '<h3 class="subsection-header">🚀 Your Priority Actions</h3>', unsafe_allow_html=True)

                for icon, title, description in personalized_tips[:4]:
                    st.markdown(f'''
                    <div class="priority-action">
                        <span style="font-size: 1.5rem; margin-right: 1rem;">{icon}</span>
                        <strong style="color: {PRIMARY_COLOR}; font-size: 1.2rem;">{title}:</strong> {description}
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="priority-action success">
                    <span style="font-size: 1.5rem; margin-right: 1rem;">✅</span>
                    <strong style="color: {SUCCESS_COLOR}; font-size: 1.2rem;">Excellent Work!</strong> Your resume shows strong fundamentals. Focus on tailoring keywords for each specific job application.
                </div>
                ''', unsafe_allow_html=True)

            # Universal tips
            st.markdown(
                '<h3 class="subsection-header">📚 Universal Best Practices</h3>', unsafe_allow_html=True)

            universal_tips = [
                ("✍️", "Use Action Verbs",
                 "Start bullets with powerful verbs: achieved, optimized, implemented, led, developed, created, managed."),
                ("🎯", "Tailor for Each Application",
                 "Customize your resume for every job. Highlight the most relevant experience and skills first."),
                ("🔍", "Proofread Thoroughly",
                 "Check for typos, grammar errors, and ensure consistency in dates, formatting, and terminology."),
                ("📱", "Ensure ATS Compatibility",
                 "Use standard fonts, clear headings, and avoid complex formatting that systems can't parse."),
            ]

            st.markdown('<div class="tips-grid">', unsafe_allow_html=True)
            for icon, title, description in universal_tips:
                st.markdown(f'''
                <div class="tip-card">
                    <div class="tip-icon">{icon}</div>
                    <div class="tip-title">{title}</div>
                    <div style="line-height: 1.6; font-size: 1rem;">{description}</div>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Welcome screen
        st.markdown(f"""
        <div style="text-align: center; margin: 4rem 0;">
            <h2 style="color: #FFFFFF; margin-bottom: 1.5rem; font-size: 2.5rem; font-weight: 700;">🚀 Ready to Optimize Your Resume?</h2>
            <p style="font-size: 1.3rem; color: {NEUTRAL_COLOR}; margin-bottom: 3rem; line-height: 1.6;">
                Get professional-grade analysis in seconds. Upload your resume and paste a job description to begin.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Feature highlights
        features = [
            ("🎯", "Smart Job Matching",
             "See exactly how well your resume matches specific job requirements"),
            ("🤖", "ATS Optimization",
             "Ensure your resume passes through applicant tracking systems"),
            ("📊", "Skills Analysis",
             "Get detailed breakdown of technical and soft skills in your resume"),
            ("📋", "Quality Assessment",
             "Comprehensive checklist covering all essential resume elements"),
            ("🔒", "Privacy Check",
             "Identify personal information and get security recommendations"),
            ("💡", "Personalized Tips",
             "Receive specific, prioritized suggestions based on your resume"),
        ]

        st.markdown('<div class="tips-grid">', unsafe_allow_html=True)
        for icon, title, description in features:
            st.markdown(f'''
            <div class="tip-card">
                <div class="tip-icon">{icon}</div>
                <div class="tip-title">{title}</div>
                <div style="line-height: 1.5; font-size: 0.95rem; color: {NEUTRAL_COLOR};">{description}</div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # How it works
        st.markdown("---")
        st.markdown(f"""
        ### 🎯 How It Works
        
        **Step 1:** 🏢 Select your target industry from the sidebar  
        **Step 2:** 📄 Upload your resume (PDF or Word format)  
        **Step 3:** 📝 Paste the complete job description you're targeting  
        **Step 4:** 🚀 Click "Analyze Resume" to get comprehensive insights  
        **Step 5:** 📊 Review results across all analysis tabs  
        
        ### ✨ Key Features
        
        - **100% Private:** Your resume data stays secure - no external API calls
        - **Instant Analysis:** Get comprehensive results in seconds
        - **Job-Specific:** Tailored analysis based on actual job postings
        - **Comprehensive:** Covers keywords, ATS compatibility, quality, and privacy
        - **Actionable:** Clear, prioritized recommendations for improvement
        - **Professional:** Industry-standard analysis for career success
        """)

        # CTA
        if not resume_file and not job_description:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 50%, {ACCENT_COLOR} 100%); 
                        padding: 3rem; border-radius: 16px; color: white; text-align: center; margin: 3rem 0;
                        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.4);">
                <h3 style="margin-bottom: 1rem; font-size: 2rem; font-weight: 700;">Ready to Get Started? 👆</h3>
                <p style="margin: 0; font-size: 1.2rem; opacity: 0.95;">
                    Use the sidebar on the left to upload your resume and add a job description
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {NEUTRAL_COLOR}; padding: 2rem 0;">
        <p style="margin: 0;">Made with ❤️ using Streamlit | Resume Analyzer Pro v2.0</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">© 2024 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
