import streamlit as st
import json

# Load the JSON data
with open('test.json', 'r') as file:
    data = json.load(file)

# Display data using Streamlit widgets
st.title("Resume Viewer")

if 'num_added_projects' not in st.session_state:
    st.session_state.num_added_projects = 0
if 'num_added_works' not in st.session_state:
    st.session_state.num_added_works = 0
if 'num_added_langs' not in st.session_state:
    st.session_state.num_added_langs = 0
if 'num_added_educations' not in st.session_state:
    st.session_state.num_added_educations = 0
if 'num_added_skills' not in st.session_state:
    st.session_state.num_added_skills = 0
# Name
st.text_input("Name", data['Name'], key="Name")

# Contact Details
st.subheader("Contact Details")
for key, value in data['Contact'].items():
    if key == "Birthdate":
        st.date_input(key, key=f"Contact_{key}", format="DD.MM.YYYY")
    elif key == "birthplace":
        # use select_box to select from a list of countries
        st.selectbox(key, value, key=f"Contact_{key}")
    else:
        st.text_input(key, value, key=f"Contact_{key}")

# Summary
st.subheader("Summary")
st.text_area("Summary", data['Summary'], key="Summary")

def display_education(edu_idx, education=None):
    cols1 = st.columns([2,2.5,1])
    cols2 = st.columns([1,1.5])
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
        duration = st.text_input(
            "Duration", duration, key=duration_key)
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

    # Display additional education entries added by the user
    for edu_idx in range(st.session_state.num_added_educations):
        new_edu = display_education(edu_idx)
        data['Education'].append(new_edu)
        # st.divider()
    
with st.expander("Education", expanded=True):
    education_section(data)


# Work Experience


def display_work(work_idx, work=None):
    cols = st.columns(3)
    with cols[0]:

        duration = st.text_input(
            "Duration", work['Duration'] if work else "", key=f"work_Duration_{work_idx}")
    with cols[1]:

        role = st.text_input(
            "Role", work['Role'] if work else "", key=f"work_Role_{work_idx}")
    with cols[2]:

        location = st.text_input(
            "Location", work['Location'] if work else "", key=f"work_Location_{work_idx}")
    company = st.text_input(
        "Company", work['Company'] if work else "", key=f"work_Company_{work_idx}")

    # duration = st.text_input("Duration", work['Duration'], key=f"Work_Duration_{work_idx}")
    # role = st.text_input("Role", work['Role'], key=f"Work_Role_{work_idx}")
    # location = st.text_input("Location", work['Location'], key=f"Work_Location_{work_idx}")
    # company = st.text_input("Company", work['Company'], key=f"Work_Company_{work_idx}")
    responsibilities = st.text_area("Responsibilities", '; '.join(work.get('Responsibilities', [])) if work else "",
                                     help="Separate each responsibility with a semicolon '';''", key=f"Work_Responsibilities_{work_idx}")
    skills = st.text_area("Skills", ', '.join(work.get('Skills', [])) if work else "",
                           help="Separate each skill with a comma '',''", key=f"Work_Skills_{work_idx}")
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
    cols = st.columns(3)
    with cols[1]:
        title = st.text_input(
            "Title", proj['Title'] if proj else "", key=f"Proj_Title_{proj_idx}")
    with cols[0]:
        duration = st.text_input(
            "Duration", proj['Duration'] if proj else "", key=f"Proj_Duration_{proj_idx}")
    with cols[2]:
        location = st.text_input(
            "Location", proj['Location'] if proj else "", key=f"Proj_Location_{proj_idx}")
    institution = st.text_input(
        "Institution", proj['Institution'] if proj else "", key=f"Proj_Institution_{proj_idx}")
    cols = st.columns([10, 1])
    with cols[0]:
        topic = st.text_input(
            "Topic", proj['Topic'] if proj else "", key=f"Proj_Topic_{proj_idx}")
    with cols[1]:
        grade = st.text_input(
            "Grade", proj['Grade'] if proj else "", key=f"Proj_Grade_{proj_idx}")
    responsibilities = st.text_area("Responsibilities", '; '.join(proj.get('Responsibilities', [])) if proj else "",
                                     help="Separate each responsibility with a semicolon '';''", key=f"Proj_Responsibilities_{proj_idx}")
    skills = st.text_area("Skills", ', '.join(proj.get('Skills', [])) if proj else "",
                           help="Separate each skill with a comma '',''", key=f"Proj_Skills_{proj_idx}")

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


with st.expander("Work Experience", expanded=True):

    work_experience_section(data)


with st.expander("Project Experience", expanded=True):

    # Execute the Project Experience section
    project_experience_section(data)


# Define a list of common languages and proficiency levels
all_languages = ['---',
    'Afrikaans', 'Albanian', 'Arabic', 'Armenian', 'Basque', 'Bengali', 'Bulgarian',
    'Catalan', 'Cambodian', 'Chinese (Mandarin)', 'Chinese (Cantonese)', 'Croatian', 'Czech', 'Danish',
    'Dutch', 'English', 'Estonian', 'Fiji', 'Finnish', 'French', 'Georgian', 'German',
    'Greek', 'Gujarati', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian',
    'Irish', 'Italian', 'Japanese', 'Javanese', 'Korean', 'Latin', 'Latvian', 'Lithuanian',
    'Macedonian', 'Malay', 'Malayalam', 'Maltese', 'Maori', 'Marathi', 'Mongolian',
    'Nepali', 'Norwegian', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua',
    'Romanian', 'Russian', 'Samoan', 'Serbian', 'Slovak', 'Slovenian', 'Spanish',
    'Swahili', 'Swedish', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tibetan', 'Tonga',
    'Turkish', 'Ukrainian', 'Urdu', 'Uzbek', 'Vietnamese', 'Welsh', 'Xhosa'
]
proficiency_levels = ['---','A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Native']

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
        skill_key = st.text_input("IT Skills", skill if skill else "", key=f"Skill_Key_{skill_idx}")
    with cols[1]:
        skill_value = st.text_input("-", ', '.join(skill[skill_key]) if skill and skill_key in skill else "", key=f"Skill_Value_{skill_idx}")
    # st.divider()
    if not skill:
        new_skill = {skill_key: [value.strip() for value in skill_value.split(',')]}
        return new_skill

def modify_languages_and_skills(data, all_languages, proficiency_levels):
    modified_main_key = "Languages & IT Skills"

    if modified_main_key != "Languages & IT Skills":
        data[modified_main_key] = data.pop("Languages & IT Skills")

    # Languages & IT Skills
    cols = st.columns([10, 1])
    with cols[0]:
    
        st.subheader("IT Skills")
        
    with cols[1]:
        if st.button("➕", key="it_skill"):
            st.session_state.num_added_skills += 1
    for idx in range(st.session_state.num_added_skills):
        display_it_skill(idx)
        
    for key, value in list(data[modified_main_key].items()):

        if key == "Languages":
            st.divider()
            cols = st.columns([10, 1])
            with cols[0]:
                st.subheader("Languages")
            with cols[1]:
                if st.button("➕",  key="lang"):
                    st.session_state.num_added_langs += 1

            cols = st.columns(2)
            for k, v in list(value.items()):
                selected_language = cols[0].selectbox("Select Language", options=all_languages, index=all_languages.index(
                    k) if k in all_languages else 0, key=f"Language_{k}")
                selected_level = cols[1].selectbox("Select Proficiency", options=proficiency_levels, index=proficiency_levels.index(
                    v) if v in proficiency_levels else 0, key=f"Proficiency_{k}")
                if selected_language != k:
                    del data[modified_main_key][key][k]
                data[modified_main_key][key][selected_language] = selected_level
            for lang_idx in range(st.session_state.num_added_langs):
                new_language = display_language(lang_idx)
                data[modified_main_key][key].update(new_language)
        else:
            cols = st.columns([1, 3])
            # Key on the left column
            modified_key = cols[0].text_input("IT Skills", key)
            
            if isinstance(value, list):
                # Values on the right column
                modified_value = cols[1].text_input(
                    '-', ', '.join(value))
                # Update the data in case of any changes
                data['Languages & IT Skills'][modified_key] = modified_value.split(
                    ', ')
                
            elif isinstance(value, dict):
         
                # for k, v in value.items():
                #     # Sub-key on the left column
                #     modified_sub_key = cols[0].text_input(
                #         f"Sub-key for {k}", k)
                #     # Values on the right column
                #     modified_sub_value = cols[1].text_input(
                #         '-', v)
                #     # Update the data in case of any changes
                #     data['Languages & IT Skills'][modified_key][modified_sub_key] = modified_sub_value
                # Display additional IT skills added by the user
                for skill_idx in range(st.session_state.num_added_skills):
                    new_skill = display_it_skill(skill_idx)
                    data['Languages & IT Skills'][modified_key].update(new_skill)


with st.expander("Languages & IT Skills", expanded=True):
    modify_languages_and_skills(data, all_languages, proficiency_levels)

# Hobbies
st.subheader("Hobbies")
hobbies = ', '.join(data['Hobbies'])
modified_hobbies = st.text_input("-", hobbies)
data['Hobbies'] = [hobby.strip() for hobby in modified_hobbies.split(',')]

st.divider()
cols = st.columns(2)
# Location
with cols[0]:
    st.text_input("Location", data['Location'], key="Location")
# Date
with cols[1]:
    st.text_input("Date", data['Date'], key="Date")
