import os
import json
import openai

# Assuming your OpenAI API key is set in your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_detected_smells(file_path='detected_smells.json'):
    """Load detected design smells from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_refactoring_suggestion(code, issue):
    """Ask OpenAI API for a refactoring suggestion based on the identified issue."""
    prompt = f"Refactor this Python code to address the following issue: {issue}\n\n### Original Code\n{code}\n###"
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=250,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["###"]
    )
    return response.choices[0].text.strip()

def apply_refactoring(file_path, refactored_code):
    """Replace the content of the file with refactored code."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(refactored_code)

def main(detected_smells_file):
    detected_smells = load_detected_smells(detected_smells_file)
    
    for file_path, issues in detected_smells.items():
        print(f"Processing {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as file:
            original_code = file.read()

        # Assume each file has a list of issues; for simplicity, we take the first one
        if issues:
            issue = issues[0]  # Simplification for example purposes
            refactored_code = get_refactoring_suggestion(original_code, issue)
            if refactored_code:
                apply_refactoring(file_path, refactored_code)
                print(f"Refactored {file_path} to address: {issue}")
            else:
                print(f"No refactoring suggestion for {file_path} on issue: {issue}")
        else:
            print(f"No issues detected for {file_path}, skipping...")

if __name__ == "__main__":
    detected_smells_file = 'detected_smells.json'  # Path to the file containing detected smells
    main(detected_smells_file)
