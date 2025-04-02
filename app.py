import streamlit as st
import PyPDF2
import docx
from dotenv import load_dotenv
import os
import openai
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Title
st.title("💼 Smart Application Toolkit")
st.subheader("Your AI-powered assistant for job applications")

# Upload Resume
st.markdown("### 📄 Upload Your Resume")
resume_file = st.file_uploader("Choose your resume (PDF or DOCX)", type=["pdf", "docx"])

# Paste or Upload Job Description
st.markdown("### 📝 Paste the Job Description")
job_description = st.text_area("Paste the job description here")

# Analyze Button
if resume_file and job_description:
    st.success("✅ Analysis started...")

    resume_text = ""

    if resume_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(resume_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text()

    elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(resume_file)
        for para in doc.paragraphs:
            resume_text += para.text + "\n"

    st.markdown("### 🧾 Extracted Resume Content:")
    st.text(resume_text)

    # GPT Analysis with OpenAI v1+
    with st.spinner("🤖 Analyzing with GPT..."):
        prompt = f"""
        You are an AI career assistant. Compare the resume below with the job description.
        Highlight strengths, missing skills, and give improvement tips.

        Resume:
        {resume_text}

        Job Description:
        {job_description}
        """

        response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # ✅ simpler, works for OpenRouter
    messages=[
        {"role": "system", "content": "You are a helpful and professional resume analyzer."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=500
)

        gpt_output = response.choices[0].message.content
        st.markdown("### 🤖 GPT Resume Analysis")
        st.write(gpt_output)

else:
    st.warning("⚠️ Please upload a resume and paste a job description.")
