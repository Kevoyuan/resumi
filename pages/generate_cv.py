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

# Languages & IT Skills
st.subheader("Languages & IT Skills")
for key, value in data['Languages & IT Skills'].items():
    if key == 'Languages':
        # Special handling for "Languages" subsection
        # modified_key = st.text_input(f"IT Skills", key)
        cols = st.columns(2)
        for k, v in value.items():
            lang_key = cols[0].text_input(f"Languages", k)
            lang_value = cols[1].text_input(lang_key, v)
            # Update the data in case of any changes
            data['Languages & IT Skills']["Languages"][lang_key] = lang_value
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
