import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
 JD Percentage Match(highlighted bold text): next line  Matching Keywords which are in resume information then  in next line missing keywords(Highlighted bold text) with pointwise but short and concise and next line with spaces for profile summary listed in resume information and at last give some recommendations.   
"""
## streamlit app
st.sidebar.title("Advanced Resume Tracking System")
st.sidebar.text("Improve Your Resume Right now!")
jd=st.sidebar.text_area("Paste the Job Description",placeholder="Input the Job description for matching otherwise you will get only profile review with recommendations")
uploaded_file=st.sidebar.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.sidebar.button("Submit")


if uploaded_file is None:
    st.header("Advanced Resume Tracking System")
    st.markdown("---")
    st.markdown("Welcome to the advanced resume tracking system where you can simply upload the job description and resume and can see matching , missing and recommendations for job.")
    st.markdown("Neeraj Kumar")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.link_button("Linkdin", "https://www.linkedin.com/in/neeraj-kumar-9a75811a2")
    with col2:
        st.link_button("Github", "https://github.com/neerajcodes888")
    with col3:
        st.link_button("Kaggle", "https://www.kaggle.com/neerajdata")
    st.markdown("---")
    st.info('Resume Tracking - Making Job Applications Easier', icon=None)
    st.warning(' Upload  Resume in  .pdf format Only')


if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        space="                                                      "
        response=get_gemini_repsonse(text+" as resume information "+space+jd+" as job description "+space+input_prompt)
        st.subheader(response)
