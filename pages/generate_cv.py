import streamlit as st
import json

from datetime import date
import canvas
from datetime import datetime
def load_json_data(filename: str):
    """Load JSON data from a given filename."""
    with open(filename, 'r') as file:
        return json.load(file)

data = load_json_data('resume_properties.json')
openai_api_key = st.secrets['OPENAI_API_KEY']
all_languages = load_json_data('languages_list.json')





# Display data using Streamlit widgets
st.title("Resume Viewer")

session_state_keys = [
    'num_added_projects', 'num_added_works', 'num_added_langs',
    'num_added_educations', 'num_added_skills'
]
def init_session_state(keys, default_value=0):
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = default_value
init_session_state(session_state_keys)

def split_name(full_name: str):
    """
    Split a full name into first and last names.
    
    Args:
    - full_name (str): The full name to be split.
    
    Returns:
    - tuple: A tuple containing the first and last names.
    """
    parts = full_name.split()
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
    return first_name, last_name


cols = st.columns([2, 1, 2])
# Name
with cols[0]:
    first_name, last_name = split_name(data['Name'])
    st.text_input("First Name", first_name, key="FirstName")
    st.text_input("Last Name", last_name, key="LastName")


# Photo
with st.sidebar:
    # uplodad photo
    uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "png"])
    if uploaded_file:
        with cols[2]:
            st.image(uploaded_file, width=150)
            st.caption("Photo")

def suggest_modification(text, openai_api_key=openai_api_key):
    prompt = '''
    give suggestions for the following resume for each section:
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
    
    

# Contact Details
def handle_birthdate(key, value, data):
    birthdate_date_object = datetime.strptime(value, "%d.%m.%Y").date()
    selected_date = st.date_input(
        key, value=birthdate_date_object, format="DD.MM.YYYY", key=f"Contact_{key}")
    data['Contact'][key] = selected_date.strftime('%d.%m.%Y')

def handle_birthplace(key, value):
    st.selectbox(key, value, key=f"Contact_{key}")

def create_contact_details(data):
    st.subheader("Contact Details")
    for key, value in data['Contact'].items():
        if key == "Birthdate":
            handle_birthdate(key, value, data)
        elif key == "birthplace":
            handle_birthplace(key, value)
        else:
            st.text_input(key, value, key=f"Contact_{key}")

with st.expander("Contact Details", expanded=False):
    create_contact_details(data)
# Summary
st.subheader("Summary")
st.text_area("Summary", data['Summary'], key="Summary")

def get_start_end_dates_from_duration(duration: str):
    # Extract start and end dates
    start_date_str, _, end_date_str = duration.partition('-')
    start_date_str = start_date_str.strip()
    end_date_str = end_date_str.strip()

    # Add day part if missing
    start_date_str = start_date_str if len(start_date_str) == 10 else f"01.{start_date_str}"
    end_date_str = end_date_str if len(end_date_str) == 10 else f"01.{end_date_str}"

    # Convert to date objects
    start_date = datetime.strptime(start_date_str, "%d.%m.%Y").date()
    end_date = datetime.strptime(end_date_str, "%d.%m.%Y").date()
    
    return start_date, end_date

def duration_to_date(duration: str, duration_key_name: str):
    if not duration:
        start_date, end_date = date.today(), date.today()
    else:
        start_date, end_date = get_start_end_dates_from_duration(duration)
    st.date_input("Duration", (start_date, end_date), format="DD.MM.YYYY", key=duration_key_name)

def display_education(edu_idx, education=None):
    cols1 = st.columns([2, 2.5, 1])
    cols2 = st.columns([1, 1.5])
    duration_key = f"Edu_Duration_{edu_idx}"
    institution_key = f"Edu_Institution_{edu_idx}"
    location_key = f"Edu_Location_{edu_idx}"
    degree_key = f"Edu_Degree_{edu_idx}"
    focus_key = f"Edu_Focus_{edu_idx}"

    duration = education.get('Duration', '') if education else ''
    institution = education.get('Institution', '') if education else ''
    location = education.get('Location', '') if education else ''
    degree = education.get('Degree', '') if education else ''
    focus = education.get('Focus', '') if education else ''

    with cols1[0]:
        duration_to_date(duration,duration_key)
    with cols1[1]:
        institution = st.text_input(
            "Institution", institution, key=institution_key)
    with cols1[2]:
        location = st.text_input(
            "Location", location, key=location_key)
    with cols2[0]:
        degree = st.text_input(
            "Degree", degree, key=degree_key)
    with cols2[1]:
        focus = st.text_input(
            "Focus", focus, key=focus_key)
    st.divider()
    if not education:  # If it's a new education entry
        new_edu = {
            'Duration': duration,
            'Institution': institution,
            'Location': location,
            'Degree': degree,
            'Focus': focus
        }
        return new_edu


def education_section(data):
    cols = st.columns([10, 1])

    with cols[0]:
        st.subheader("Education")
    with cols[1]:
        # Button to add additional education entries
        if st.button("➕", key="edu"):
            st.session_state.num_added_educations += 1

    # Display existing education entries
    for idx, edu in enumerate(data['Education']):
        display_education(idx, edu)

    # Divider for visual separation
    # st.divider()
    offset = len(data['Education'])
    # Display additional education entries added by the user
    for edu_idx in range(offset, offset + st.session_state.num_added_educations):
        new_edu = display_education(edu_idx)
        data['Education'].append(new_edu)
        # st.divider()


with st.expander("Education", expanded=False):
    education_section(data)


# Work Experience


def display_work(work_idx, work=None):
    cols = st.columns(3)

    work_duration_key = f"work_Duration_{work_idx}"
    work_Role_key = f"work_Role_{work_idx}"
    work_Location_key = f"work_Location_{work_idx}"
    work_Company_key = f"work_Company_{work_idx}"
    work_Responsibilities_key = f"Work_Responsibilities_{work_idx}"
    work_Skills_key = f"Work_Skills_{work_idx}"


    duration = work.get('Duration', '') if work else ''
    role = work.get('Role', '') if work else ''
    location = work.get('Location', '') if work else ''
    company = work.get('Company', '') if work else ''
    responsibilities = work.get('Responsibilities', []) if work else []
    skills = work.get('Skills', []) if work else []
    

    with cols[0]:
        duration_to_date(duration,work_duration_key)
 
    with cols[1]:

        role = st.text_input("Role", role, key=work_Role_key)
    with cols[2]:

        location = st.text_input(
            "Location", location, key=work_Location_key)
    company = st.text_input(    
        "Company", company, key=work_Company_key)

    responsibilities = st.text_area("Responsibilities", '; '.join(work.get('Responsibilities', [])) if work else "",
                                    help="Separate each responsibility with a semicolon '';''", key=work_Responsibilities_key)
    skills = st.text_area("Skills", ', '.join(work.get('Skills', [])) if work else "",
                          help="Separate each skill with a comma '',''", key=work_Skills_key)
    st.divider()
    if not work:  # If it's a new project
        new_work = {
            'Role': role,
            'Duration': duration,
            'Location': location,
            'Company': company,
            'Responsibilities': [resp.strip() for resp in responsibilities.split(';')],
            'Skills': [skill.strip() for skill in skills.split(',')]
        }
        return new_work


def display_existing_works(data):
    """Display all existing works from the data dictionary."""
    for idx, work in enumerate(data['Work Experience']):
        display_work(idx, work)


def display_additional_works(data):
    """Handle and display additional works added by the user."""
    for idx in range(st.session_state.num_added_works):
        work_idx = len(data['Work Experience']) + idx
        new_work = display_work(work_idx)
        data['Work Experience'].append(new_work)
        # st.divider()


def work_experience_section(data):
    """Main function to manage the "Work Experience" section."""
    cols = st.columns([10, 1])
    with cols[0]:
        st.subheader("Work Experience")
    with cols[1]:
        # Button to add additional work experience
        if st.button("➕", key="work"):
            st.session_state.num_added_works += 1
    # Display existing works
    display_existing_works(data)
    # Divider for visual separation
    # st.divider()
    # Display additional works added by the user
    display_additional_works(data)


# Project Experience
def display_project(proj_idx, proj=None):
    """Display fields for a single project and return the project data if new."""
    title = proj.get('Title', '') if proj else ''
    duration = proj.get('Duration', '') if proj else ''
    location = proj.get('Location', '') if proj else ''
    institution = proj.get('Institution', '') if proj else ''
    topic = proj.get('Topic', '') if proj else ''
    grade = proj.get('Grade', '') if proj else ''
    responsibilities = proj.get('Responsibilities', []) if proj else []
    skills = proj.get('Skills', []) if proj else []
    
    proj_title_key = f"Proj_Title_{proj_idx}"
    proj_duration_key = f"Proj_Duration_{proj_idx}"
    proj_Location_key = f"Proj_Location_{proj_idx}"
    proj_Institution_key = f"Proj_Institution_{proj_idx}"
    proj_Topic_key = f"Proj_Topic_{proj_idx}"
    proj_Grade_key = f"Proj_Grade_{proj_idx}"
    proj_Responsibilities_key = f"Proj_Responsibilities_{proj_idx}"
    proj_Skills_key = f"Proj_Skills_{proj_idx}"
    
    cols = st.columns(3)
    with cols[1]:
        title = st.text_input(
            "Title", title, key=proj_title_key)
    with cols[0]:
        duration_to_date(duration,proj_duration_key)
     
    with cols[2]:
        location = st.text_input(
            "Location", location, key=proj_Location_key)
    institution = st.text_input(
        "Institution", institution, key=proj_Institution_key)
    cols = st.columns([10, 1])
    with cols[0]:
        topic = st.text_input(
            "Topic", topic, key=proj_Topic_key)
    with cols[1]:
        grade = st.text_input(
            "Grade", grade, key=proj_Grade_key)
    responsibilities = st.text_area("Responsibilities", '; '.join(proj.get('Responsibilities', [])) if proj else "",
                                    help="Separate each responsibility with a semicolon '';''", key=proj_Responsibilities_key)
    skills = st.text_area("Skills", ', '.join(proj.get('Skills', [])) if proj else "",
                          help="Separate each skill with a comma '',''", key=proj_Skills_key)

    if not proj:  # If it's a new project
        new_proj = {
            'Title': title,
            'Duration': duration,
            'Location': location,
            'Institution': institution,
            'Topic': topic,
            'Grade': grade,
            'Responsibilities': [resp.strip() for resp in responsibilities.split(';')],
            'Skills': [skill.strip() for skill in skills.split(',')]
        }
        return new_proj


def display_existing_projects(data):
    """Display all existing projects from the data dictionary."""
    for idx, proj in enumerate(data['Project Experience']):
        display_project(idx, proj)


def display_additional_projects(data):
    """Handle and display additional projects added by the user."""
    for idx in range(st.session_state.num_added_projects):
        proj_idx = len(data['Project Experience']) + idx
        new_proj = display_project(proj_idx)
        data['Project Experience'].append(new_proj)
        st.divider()


def project_experience_section(data):
    """Main function to manage the "Project Experience" section."""
    cols = st.columns([10, 1])
    with cols[0]:
        st.subheader("Project Experience")
    with cols[1]:
        # Button to add additional project experience
        if st.button("➕",  key="proj"):
            st.session_state.num_added_projects += 1
    # Display existing projects
    display_existing_projects(data)
    # Divider for visual separation
    st.divider()
    # Display additional projects added by the user
    display_additional_projects(data)


with st.expander("Work Experience", expanded=False):

    work_experience_section(data)


with st.expander("Project Experience", expanded=False):

    # Execute the Project Experience section
    project_experience_section(data)



proficiency_levels = ['---', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Native']

modified_main_key = "Languages & IT Skills"
if modified_main_key != "Languages & IT Skills":
    data[modified_main_key] = data.pop("Languages & IT Skills")

# Languages & IT Skills
def display_language(language_idx, language=None):

        
    cols = st.columns(2)
    with cols[0]:
        selected_language = st.selectbox("Select Language", options=all_languages, index=all_languages.index(
            language) if language in all_languages else 0, key=f"Language_{language_idx}")
    with cols[1]:
        selected_level = st.selectbox("Select Proficiency", options=proficiency_levels, index=proficiency_levels.index(
            language[level]) if language and language[level] in proficiency_levels else 0, key=f"Level_{language_idx}")

    if not language:  # If it's a new language
        new_language = {
            selected_language: selected_level
        }
        return new_language


def display_it_skill(skill_idx, skill=None):
    cols = st.columns([1, 3])
    with cols[0]:
        skill_key = st.text_input(
            "IT Skills", skill if skill else "", key=f"Skill_Key_{skill_idx}")
    with cols[1]:
        skill_value = st.text_input(
            "-", ', '.join(skill[skill_key]) if skill and skill_key in skill else "", key=f"Skill_Value_{skill_idx}")
    # st.divider()
    if not skill:
        new_skill = {skill_key: [value.strip()
                                 for value in skill_value.split(',')]}
        return new_skill


def modify_languages(data, all_languages, proficiency_levels):
    """Handle the languages modification."""
    st.divider()
    cols = st.columns([10, 1])
    with cols[0]:
        st.subheader("Languages")
    with cols[1]:
        if st.button("➕", key="lang"):
            st.session_state.num_added_langs += 1

    cols = st.columns(2)
    for k, v in list(data["Languages & IT Skills"]["Languages"].items()):
        selected_language = cols[0].selectbox("Select Language", options=all_languages,
                                              index=all_languages.index(
                                                  k) if k in all_languages else 0,
                                              key=f"Language_{k}")
        selected_level = cols[1].selectbox("Select Proficiency", options=proficiency_levels,
                                           index=proficiency_levels.index(
                                               v) if v in proficiency_levels else 0,
                                           key=f"Proficiency_{k}")
        if selected_language != k:
            del data["Languages & IT Skills"]["Languages"][k]
        data["Languages & IT Skills"]["Languages"][selected_language] = selected_level

    for lang_idx in range(st.session_state.num_added_langs):
        new_language = display_language(lang_idx)
        data["Languages & IT Skills"]["Languages"].update(new_language)


def modify_it_skills(data):
    """Handle the IT skills modification."""
    cols = st.columns([10, 1])
    with cols[0]:
        st.subheader("IT Skills")
    with cols[1]:
        if st.button("➕", key="it_skill"):
            st.session_state.num_added_skills += 1

    for key, value in list(data["Languages & IT Skills"].items()):
        if key != "Languages":
            cols = st.columns([1, 3])
            modified_key = cols[0].text_input("IT Skills", key)
            if isinstance(value, list):
                modified_value = cols[1].text_input('-', ', '.join(value))
                data['Languages & IT Skills'][modified_key] = modified_value.split(
                    ', ')
    for idx in range(st.session_state.num_added_skills):
        display_it_skill(idx)


def modify_languages_and_skills_optimized(data, all_languages, proficiency_levels):
    """Optimized modify_languages_and_skills function."""
    modify_it_skills(data)
    modify_languages(data, all_languages, proficiency_levels)


with st.expander("Languages & IT Skills", expanded=False):
    modify_languages_and_skills_optimized(
        data, all_languages, proficiency_levels)


# Hobbies
def display_hobbies(data):
    st.subheader("Hobbies")
    hobbies = ', '.join(data['Hobbies'])
    modified_hobbies = st.text_input("-", hobbies)
    data['Hobbies'] = [hobby.strip() for hobby in modified_hobbies.split(',')]


with st.expander("Hobbies", expanded=False):
    display_hobbies(data)

st.divider()
cols = st.columns(2)
# Location
with cols[0]:
    st.text_input("Location", data['Location'], key="Location")
# Date
with cols[1]:
    st.date_input("Date", value=date.today(), format="DD.MM.YYYY", key="Date")
canvas.signiture()
