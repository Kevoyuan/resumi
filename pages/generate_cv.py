import streamlit as st
import pdfkit
import json

# Define the LaTeX template for the CV
LATEX_TEMPLATE = r"""
\documentclass{article}
\begin{document}
{content}
\end{document}
"""

def generate_pdf(latex_content):
    # Convert LaTeX to PDF
    config = pdfkit.configuration(wkhtmltopdf='/path/to/wkhtmltopdf')  # Update the path
    pdfkit.from_string(latex_content, 'out.pdf', configuration=config)

def read_json_to_latex(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Convert the JSON data to LaTeX format (this is a basic example, you can structure it as needed)
    latex_content = f"""
    {data['name']}
    {data['address']}
    {data['email']}
    ...
    """
    return latex_content

st.title("LaTeX CV Editor")

# Read content from test.json
initial_content = read_json_to_latex('test.json')

# Textarea for user to input or modify LaTeX content
user_input = st.text_area("Edit your CV in LaTeX:", LATEX_TEMPLATE.format(content=initial_content))

if st.button("Generate PDF"):
    generate_pdf(user_input)
    st.success("PDF generated! [Download here](out.pdf)")

st.write("Preview:")
st.latex(user_input)
