import streamlit as st
import json

# Load the JSON data
with open('test.json', 'r') as file:
    data = json.load(file)

# Display data using Streamlit widgets
st.title("Resume Viewer")

if 'num_added_projects' not in st.session_state:
    st.session_state.num_added_projects = 0

# Name
st.text_input("Name", data['Name'], key="Name")

# Contact Details
st.subheader("Contact Details")
for key, value in data['Contact'].items():
    st.text_input(key, value, key=f"Contact_{key}")

# Summary
st.subheader("Summary")
st.text_area("Summary", data['Summary'], key="Summary")

# Education
st.subheader("Education")
for idx, edu in enumerate(data['Education']):
    st.text_input("Duration", edu['Duration'], key=f"Edu_Duration_{idx}")
    st.text_input("Institution", edu['Institution'], key=f"Edu_Institution_{idx}")
    st.text_input("Location", edu['Location'], key=f"Edu_Location_{idx}")
    st.text_input("Degree", edu['Degree'], key=f"Edu_Degree_{idx}")
    st.text_input("Focus", edu.get("Focus", ""), key=f"Edu_Focus_{idx}")

# Work Experience
st.subheader("Work Experience")
for idx, work in enumerate(data['Work Experience']):
    st.text_input("Duration", work['Duration'], key=f"Work_Duration_{idx}")
    st.text_input("Role", work['Role'], key=f"Work_Role_{idx}")
    st.text_input("Location", work['Location'], key=f"Work_Location_{idx}")
    st.text_input("Company", work['Company'], key=f"Work_Company_{idx}")
    responsibilities = '; '.join(work.get('Responsibilities', []))
    modified_responsibilities = st.text_input("Responsibilities", responsibilities, help="Separate each responsibility with a semicolon '';''")
    work['Responsibilities'] = [resp.strip() for resp in modified_responsibilities.split(';')]
    
    skills = ', '.join(work.get('Skills', []))
    modified_skills = st.text_input("Skills", skills, help="Separate each skill with a comma '',''")
    work['Skills'] = [skill.strip() for skill in modified_skills.split(',')]
    st.divider()


# Project Experience
st.subheader("Project Experience")
cols = st.columns(3)
for idx, proj in enumerate(data['Project Experience']):
    with cols[1]:
        st.text_input("Title", proj['Title'], key=f"Proj_Title_{idx}")
    with cols[0]:
        st.text_input("Duration", proj['Duration'], key=f"Proj_Duration_{idx}")
    with cols[2]:
        st.text_input("Location", proj['Location'], key=f"Proj_Location_{idx}")
    st.text_input("Institution", proj['Institution'], key=f"Proj_Institution_{idx}")
    cols = st.columns([10,1])
    with cols[0]:
        st.text_input("Topic", proj['Topic'], key=f"Proj_Topic_{idx}")
    with cols[1]:
        st.text_input("Grade", proj['Grade'], key=f"Proj_Grade_{idx}")

    responsibilities = '; '.join(proj.get('Responsibilities', []))
    modified_responsibilities = st.text_input("Responsibilities", responsibilities, help="Separate each responsibility with a semicolon '';''")
    proj['Responsibilities'] = [resp.strip() for resp in modified_responsibilities.split(';')]
    
    skills = ', '.join(proj.get('Skills', []))
    modified_skills = st.text_input("Skills", skills, help="Separate each skill with a comma '',''")
    proj['Skills'] = [skill.strip() for skill in modified_skills.split(',')]
    st.divider()
    

## Additional Project Experiences added by the user
for idx in range(st.session_state.num_added_projects):
    proj_idx = len(data['Project Experience']) + idx
    cols = st.columns(3)
    with cols[1]:
        title = st.text_input("Title", key=f"Proj_Title_{proj_idx}")
    with cols[0]:
        duration = st.text_input("Duration", key=f"Proj_Duration_{proj_idx}")
    with cols[2]:
        location = st.text_input("Location", key=f"Proj_Location_{proj_idx}")
    institution = st.text_input("Institution", key=f"Proj_Institution_{proj_idx}")
    cols = st.columns([10, 1])
    with cols[0]:
        topic = st.text_input("Topic", key=f"Proj_Topic_{proj_idx}")
    with cols[1]:
        grade = st.text_input("Grade", key=f"Proj_Grade_{proj_idx}")

    responsibilities = st.text_input("Responsibilities", help="Separate each responsibility with a semicolon '';''", key=f"Proj_Responsibilities_{proj_idx}")
    skills = st.text_input("Skills", help="Separate each skill with a comma '',''", key=f"Proj_Skills_{proj_idx}")

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


        
    data['Project Experience'].append(new_proj)
    st.divider()


# add button to add additional project experience
if st.button("Add Project Experience"):
    st.session_state.num_added_projects += 1
    







        
# Define a list of common languages and proficiency levels
all_languages = [
    'Afrikaans', 'Albanian', 'Arabic', 'Armenian', 'Basque', 'Bengali', 'Bulgarian', 
    'Catalan', 'Cambodian', 'Chinese (Mandarin)','Chinese (Cantonese)', 'Croatian', 'Czech', 'Danish', 
    'Dutch', 'English', 'Estonian', 'Fiji', 'Finnish', 'French', 'Georgian', 'German', 
    'Greek', 'Gujarati', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian', 
    'Irish', 'Italian', 'Japanese', 'Javanese', 'Korean', 'Latin', 'Latvian', 'Lithuanian', 
    'Macedonian', 'Malay', 'Malayalam', 'Maltese', 'Maori', 'Marathi', 'Mongolian', 
    'Nepali', 'Norwegian', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 
    'Romanian', 'Russian', 'Samoan', 'Serbian', 'Slovak', 'Slovenian', 'Spanish', 
    'Swahili', 'Swedish', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tibetan', 'Tonga', 
    'Turkish', 'Ukrainian', 'Urdu', 'Uzbek', 'Vietnamese', 'Welsh', 'Xhosa'
]
proficiency_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Native']

modified_main_key = "Languages & IT Skills"
if modified_main_key != "Languages & IT Skills":
    data[modified_main_key] = data.pop("Languages & IT Skills")

# Languages & IT Skills
st.subheader("Languages & IT Skills")
for key, value in list(data[modified_main_key].items()):
    if key == "Languages":
        st.divider()
        cols = st.columns(2)
        for k, v in list(value.items()):
            selected_language = cols[0].selectbox("Select Language", options=all_languages, index=all_languages.index(k) if k in all_languages else 0, key=f"Language_{k}")
            selected_level = cols[1].selectbox("Select Proficiency", options=proficiency_levels, index=proficiency_levels.index(v) if v in proficiency_levels else 0, key=f"Proficiency_{k}")
            
            if selected_language != k:
                del data[modified_main_key][key][k]
            data[modified_main_key][key][selected_language] = selected_level
    else:
        cols = st.columns([1,3])
        # Key on the left column
        modified_key = cols[0].text_input(f"IT Skills", key)
        if isinstance(value, list):
            # Values on the right column
            modified_value = cols[1].text_input(modified_key, ', '.join(value))
            # Update the data in case of any changes
            data['Languages & IT Skills'][modified_key] = modified_value.split(', ')
        elif isinstance(value, dict):
            for k, v in value.items():
                # Sub-key on the left column
                modified_sub_key = cols[0].text_input(f"Sub-key for {k}", k)
                # Values on the right column
                modified_sub_value = cols[1].text_input(modified_sub_key, v)
                # Update the data in case of any changes
                data['Languages & IT Skills'][modified_key][modified_sub_key] = modified_sub_value

# ...




# Hobbies
st.subheader("Hobbies")
hobbies = ', '.join(data['Hobbies'])
modified_hobbies = st.text_input("Hobbies", hobbies)
data['Hobbies'] = [hobby.strip() for hobby in modified_hobbies.split(',')]


# Date
st.text_input("Date", data['Date'], key="Date")
