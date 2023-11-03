import os
import openai
import streamlit as st
import docx
from PyPDF2 import PdfFileReader
import json
import re
# DESIGN changes for Streamlit UI/UX


# Sidebar for setting OpenAI API key
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
openai_api_key = st.secrets['OPENAI_API_KEY']
# Define a regular expression pattern to match and reformat dates
DATE_PATTERNS = [
    r'(\d{2})\.(\d{2,4})\s*-\s*(\d{2})\.(\d{2,4})',     # Matches '04.20 -08.20' and '04.2020 -08.2020'
    r'(\d{2})/(\d{2,4})\s*-\s*(\d{2})/(\d{2,4})'       # Matches '04/20 - 08/20' and '04/2020 -08/2020'
]


def extract_properties_from_resume(resume_text,openai_api_key=openai_api_key):
    # Modified prompt for the OpenAI API
    # prompt = '''
    # Please extract the following resume properties and structure into a JSON format. For the 'Duration' field, use the format 'DD.MM.YYYY-DD.MM.YYYY.' If the day is missing, please ensure that DD=01 (e.g., 04/2020 or 2020.04 should be formatted as 01.04.2020).

    # {
    #     "Name": "",
    #     "Contact": {"Email": "", "GitHub": "", "Birthdate": "", "Birthplace": "", "LinkedIn": "", "Address": "", "Phone": ""},
    #     "Summary": "",
    #     "Education": [{"Duration": "", "Institution": "", "Location": "", "Degree": "", "Focus": ""}],
    #     "Work Experience": [{"Duration": "", "Role": "", "Location": "", "Company": "", "Responsibilities": [""], "Skills": [""]}],
    #     "Project Experience": [{"Duration": "", "Title": "", "Location": "", "Institution": "", "Topic": "", "Grade": "", "Responsibilities": [""], "Skills": [""]}],
    #     "Languages & IT Skills": {},
    #     "Hobbies": [""],
    #     "Location": "",
    #     "Date": ""
    # }

    # For mapping the user's language proficiency to the preset levels:
    # - Mother language can be mapped to Native.
    # - Terms like "fluent" can be mapped to C1 or C2, depending on the depth of fluency.
    # - Basic knowledge can be mapped to A1 or A2.
    # - Intermediate proficiency can be mapped to B1 or B2.

    # Please provide the required information based on the resume example you have. When providing durations, use the format "MM.YYYY - MM.YYYY". If no day is included, make day DD=01 (e.g., 04/2020 = 01.04.2020). Include details such as Name, Contact, Summary, Education, Work Experience, Project Experience, Languages & IT Skills, Hobbies, Location, and Date.


    # '''
    prompt = '''
        Please extract the following resume properties and structure into a JSON format. Ensure that the information is organized in the specified order:
    {
        "Name": "",
        "Contact": {"Email": "", "GitHub": "", "Birthdate": "", "Birthplace": "", "LinkedIn": "", "Address": "", "Phone": ""},
        "Summary": "",
        "Education": [{"Duration": "", "Institution": "", "Location": "", "Degree": "", "Focus": ""}],
        "Work Experience": [{"Duration": "", "Role": "", "Location": "", "Company": "", "Responsibilities": [""], "Skills": [""]}],
        "Project Experience": [{"Duration": "", "Title": "", "Location": "", "Institution": "", "Topic": "", "Grade": "", "Responsibilities": [""], "Skills": [""]}],
        "IT Skills": {},
        "Languages": {},
        "Hobbies": [""],
        "Location": "",
        "Date": ""
    }
    For mapping language proficiency levels, follow these guidelines:
    - Mother language can be mapped to Native.
    - Terms like "fluent" can be mapped to C1 or C2, depending on the depth of fluency.
    - Basic knowledge can be mapped to A1 or A2.
    - Intermediate proficiency can be mapped to B1 or B2.

    Please provide the required information based on the resume example you have. When providing durations, use the format "MM.YYYY - MM.YYYY" or "MM.YYYY - MM.YYYY" (e.g., 04/2020-03/2023 or 2020.05 - 2023.03 should be formatted as 04.2020 - 03.2023). Extract skills from relevant sections, and ensure that all extracted information is accurate and well-structured.
    '''
    
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
        
    openai.api_key = openai_api_key
    
    # Use the OpenAI API to process the resume
    # response = openai.Completion.create(
    #     engine="gpt-3.5-turbo",
    #     prompt=f"{prompt}\n\n{resume_text}",
    #     max_tokens=2000,
    # )
    # # Extracted properties
    # properties = response.choices[0].text.strip()
    # # Convert the properties to a dictionary
    # properties_dict = json.loads(properties)
    # Use the OpenAI API to process the resume
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}\n\n{resume_text}"},
        ],
        max_tokens=2000,
    )
    # Extracted properties
    properties = response["choices"][0]["message"]["content"].strip()
    # Convert the properties to a dictionary
    properties_dict = json.loads(properties)
  
    # try:
    #     properties_dict = json.loads(properties)
    # except json.JSONDecodeError:
    #     st.error("The model's response couldn't be parsed as JSON. Please check the response format.")
    

    st.write(f"Raw Response: {properties}")
    return properties_dict


def main_resume_extractor():
    st.title("Resume Refinement")

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
