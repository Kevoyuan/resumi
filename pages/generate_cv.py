import streamlit as st
import json

# Load the JSON data
with open('test.json', 'r') as file:
    data = json.load(file)

# Display data using Streamlit widgets
st.title("Resume Viewer")

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
    for r_idx, resp in enumerate(work.get('Responsibilities', [])):
        st.text_input("Responsibility", resp, key=f"Work_Resp_{idx}_{r_idx}")
    for s_idx, skill in enumerate(work.get('Skills', [])):
        st.text_input("Skill", skill, key=f"Work_Skill_{idx}_{s_idx}")

# Project Experience
st.subheader("Project Experience")
for idx, proj in enumerate(data['Project Experience']):
    st.text_input("Duration", proj['Duration'], key=f"Proj_Duration_{idx}")
    st.text_input("Title", proj['Title'], key=f"Proj_Title_{idx}")
    st.text_input("Location", proj['Location'], key=f"Proj_Location_{idx}")
    for a_idx, aff in enumerate(proj.get('Affiliation', [])):
        st.text_input("Affiliation", aff, key=f"Proj_Aff_{idx}_{a_idx}")
    st.text_input("Topic", proj.get("Topic", ""), key=f"Proj_Topic_{idx}")
    st.text_input("Grade", proj.get("Grade", ""), key=f"Proj_Grade_{idx}")
    for d_idx, detail in enumerate(proj.get('Responsibilities', [])):
        st.text_input("Detail", detail, key=f"Proj_Detail_{idx}_{d_idx}")
    for s_idx, skill in enumerate(proj.get('Skills', [])):
        st.text_input("Skill", skill, key=f"Proj_Skill_{idx}_{s_idx}")

# ...

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

# Languages & IT Skills
st.subheader("Languages & IT Skills")
for key, value in data['Languages & IT Skills'].items():
    if key == 'Languages':
        # Special handling for "Languages" subsection
        modified_key = st.text_input(f"Key for {key}", key)
        cols = st.columns(2)
        
        # Iterate over a copy of the dictionary items
        for k, v in list(value.items()):
            # Use k as part of the unique key for the select boxes
            # Select language from a predefined list
            selected_language = cols[0].selectbox("Select Language", options=all_languages, index=all_languages.index(k) if k in all_languages else 0, key=f"Language_{k}")
            # Select proficiency level from a predefined list
            selected_level = cols[1].selectbox("Select Proficiency", options=proficiency_levels, index=proficiency_levels.index(v) if v in proficiency_levels else 0, key=f"Proficiency_{k}")
            
            # Delete the original language key if it's changed
            if selected_language != k:
                del data['Languages & IT Skills'][modified_key][k]
            
            # Update the data with selected values
            data['Languages & IT Skills'][modified_key][selected_language] = selected_level
    else:
        cols = st.columns(2)
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
for idx, hobby in enumerate(data['Hobbies']):
    st.text_input("Hobby", hobby, key=f"Hobby_{idx}")

# Date
st.text_input("Date", data['Date'], key="Date")
