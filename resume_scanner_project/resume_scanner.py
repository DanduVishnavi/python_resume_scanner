import os
import pdfplumber
import pandas as pd
import re

# List of required skills
required_skills = ['python', 'sql', 'aws', 'excel', 'java', 'machine learning', 'communication', 'django']

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.lower()

# Function to match skills in text
def match_skills(resume_text, required_skills):
    found = []
    for skill in required_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_text):
            found.append(skill)
    return found

# Folder where all resumes are kept
resume_folder = "resumes"
shortlisted = []

# Loop through all PDFs in the folder
for filename in os.listdir(resume_folder):
    if filename.endswith(".pdf"):
        file_path = os.path.join(resume_folder, filename)
        print(f"Checking resume: {filename}")
        text = extract_text_from_pdf(file_path)
        matched_skills = match_skills(text, required_skills)
        if len(matched_skills) >= 3:  # Only shortlist if 3 or more skills matched
            shortlisted.append({
                'Name': filename,
                'Matched Skills': ', '.join(matched_skills)
            })

# Save results to Excel
if shortlisted:
    df = pd.DataFrame(shortlisted)
    df.to_excel("shortlisted_candidates.xlsx", index=False)
    print("\nShortlisting complete! Saved to 'shortlisted_candidates.xlsx'")
else:
    print("\nNo resumes matched the required skills.")