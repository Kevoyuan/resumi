import os
import openai
import streamlit as st
import docx
from PyPDF2 import PdfFileReader
import json
# DESIGN changes for Streamlit UI/UX


# Sidebar for setting OpenAI API key
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
openai_api_key = st.secrets['OPENAI_API_KEY']

def extract_properties_from_resume(resume_text,openai_api_key=openai_api_key):
    # Modified prompt for the OpenAI API
    prompt = '''
    Extract resume properties and structure in JSON. For any duration, use format="DD.MM.YYYY",if no day include, save DD=01, eg: 04/2020 = 01.04.2020):
    {
        "Name": "",
        "Contact": {"Email": "", "GitHub": "", "Birthdate": "", "Birthplace": "", "LinkedIn": "", "Address": "", "Phone": ""},
        "Summary": "",
        "Education": [{"Duration": "", "Institution": "", "Location": "", "Degree": "", "Focus": ""}],
        "Work Experience": [{"Duration": "", "Role": "", "Location": "", "Company": "", "Responsibilities": [""], "Skills": [""]}],
        "Project Experience": [{"Duration": "", "Title": "", "Location": "", "Institution": "", "Topic": "", "Grade": "", "Responsibilities": [""], "Skills": [""]}],
        "Languages & IT Skills": Capture any IT skill category eg: technical skills, program languagues (as keys) with its respective skills (as sub-keys). For "Languages": {
            "Language": "Proficiency_Level"
        },
        "Hobbies": [""],
        "Location": "",
        "Date": ""
    }
    For mapping the user's language proficiency to the preset levels:
    Mother language can be mapped to Native.
    Terms like fluent can be mapped to C1 or C2 depending on the depth of fluency.
    Basic knowledge can be mapped to A1 or A2.
    Intermediate proficiency can be mapped to B1 or B2.

    '''

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
        
    openai.api_key = openai_api_key
    
    # Use the OpenAI API to process the resume
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n\n{resume_text}",
        max_tokens=2000,
    )
    # Extracted properties
    properties = response.choices[0].text.strip()
    # Convert the properties to a dictionary
    properties_dict = json.loads(properties)
  
    # try:
    #     properties_dict = json.loads(properties)
    # except json.JSONDecodeError:
    #     st.error("The model's response couldn't be parsed as JSON. Please check the response format.")
    

    st.write(f"Raw Response: {properties}")
    return properties_dict



def read_pdf(file):
    pdf = PdfFileReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def main_resume_extractor():
    st.title("Resume Refinement")

    # uploaded_file = st.file_uploader("Upload a Word or PDF file", type=["pdf", "docx"])

    # if uploaded_file:
    #     pass
        # if uploaded_file.type == "application/pdf":
        #     resume_text = read_pdf(uploaded_file)
        # elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        #     resume_text = read_docx(uploaded_file)
        # properties = extract_properties_from_resume(resume_text)
        # st.json(properties)
        
        # # Save the properties to a JSON file
        # with open('resume_properties.json', 'w') as json_file:
        #     json.dump(properties, json_file, indent=4)
        # st.success("Properties saved to resume_properties.json")
    # else:
    resume_text = st.text_area("Paste your resume text here:")
    if st.button("Extract Properties"):
        properties = extract_properties_from_resume(resume_text)
        st.json(properties)
        
        # Save the properties to a JSON file
        with open('resume_properties.json', 'w') as json_file:
            json.dump(properties, json_file, indent=4)
        st.success("Properties saved to resume_properties.json")

if __name__ == '__main__':
    main_resume_extractor()
