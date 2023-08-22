import tiktoken

def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

text='''
    Extract the properties from the resume and structure them in JSON format using the exact following keys and sub-keys:

    {
        "Name": "",
        "Contact": {
            "Email": "",
            "GitHub": "",
            "Birthdate": "",
            "Birthplace": "",
            "LinkedIn": "",
            "Address": "",
            "Phone": ""
        },
        "Summary": "",
        "Education": [
            {
                "Duration": "",
                "Institution": "",
                "Location": "",
                "Degree": "",
                "Focus": ""
            }
        ],
        "Work Experience": [
            {
                "Duration": "",
                "Role": "",
                "Location": "",
                "Company": "",
                "Responsibilities": [""],
                "Skills": [""]
            }
        ],
        "Project Experience": [
            {
                "Duration": "",
                "Title": "",
                "Location": "",
                "Institution": "",
                "Topic": "",
                "Grade": "",
                "Responsibilities": [""],
                "Skills": [""]
            }
        ],
        "Languages & IT Skills": {
            "Programming": [""],
            "CAD": [""],
            "FEM": [""],
            "Machine Learning": [""],
            "Deep Learning": [""],
            "Tools": [""],
            "Languages": {
                "Language Name": "Proficiency"
            }
        },
        "Hobbies": [""],
        "Location": "",
        "Date": ""
    }
    '''

print(num_tokens_from_string(text, "davinci"))