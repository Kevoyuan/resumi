import os
import openai
import streamlit as st
import docx
from PyPDF2 import PdfFileReader

# DESIGN changes for Streamlit UI/UX


# Sidebar for setting OpenAI API key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"



def extract_properties_from_resume(resume_text):
    # Modified prompt for the OpenAI API
    prompt = '''
    Extract the following properties from the resume,don't miss out on any property below:
    - Name
    - Contact details including: Email, GitHub, Birthdate, Birthplace, LinkedIn, Address, Phone
    - Summary
    - List of Education experiences including: Duration, Institution, Location, Degree, Focus
    - List of Work Experiences including: Duration, Role, Location, Company, Responsibilities, Skills
    - List of Project Experiences including: Duration, Title, Location, Institution, Topic, Grade, Responsibilities, Skills
    - Languages & IT Skills: Break down the skills into categories. For the "Languages" category, list both the language and its proficiency. For other categories, list the skills under each category.
    - List of Hobbies
    - Location
    - Date of last update
    '''
    # Use the OpenAI API to process the resume
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"{prompt}\n\n{resume_text}",
        max_tokens=1000
    )
    # Extracted properties
    properties = response.choices[0].text.strip()
    # Convert the properties to a dictionary
    properties_dict = eval(properties)
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

    uploaded_file = st.file_uploader("Upload a Word or PDF file", type=["pdf", "docx"])

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            resume_text = read_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = read_docx(uploaded_file)
        properties = extract_properties_from_resume(resume_text)
        st.json(properties)
        
        # Save the properties to a JSON file
        with open('resume_properties.json', 'w') as json_file:
            json.dump(properties, json_file, indent=4)
        st.success("Properties saved to resume_properties.json")
    else:
        resume_text = st.text_area("Or paste your resume text here:")
        if st.button("Extract Properties"):
            properties = extract_properties_from_resume(resume_text)
            st.json(properties)
            
            # Save the properties to a JSON file
            with open('resume_properties.json', 'w') as json_file:
                json.dump(properties, json_file, indent=4)
            st.success("Properties saved to resume_properties.json")

if __name__ == '__main__':
    main_resume_extractor()
