import os
import openai


# Assuming your OpenAI API key is set in your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client()


def apply_refactoring(file_path, refactored_code):
    """Replace the content of the file with refactored code."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(refactored_code)


def analyze_and_refactor_smells(file_path):
    """Send the content of the given file to the OpenAI API to detect design smells."""
    with open(file_path, 'r', encoding='utf-8') as file:
        code_content = file.read()

    """Get design smells"""
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
            {
            "role": "system",
            "content": "You are a software engineer working to refactor a GitHub repository by identifying design smells."
            },
            {
            "role": "user",
            "content": f"Identify design smells in the file, and suggest refactoring changes. Be precise and concise. List only (1) Identified Design Smells, and (2) Suggested Refactoring.\n\nf{code_content}"
            }
        ],
        temperature=0.8,
        max_tokens=1200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    smells = response.choices[0].message.content
    print(smells)

    """Get refactored code"""
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "You are a software engineer working to refactor a GitHub repository by identifying design smells."
        },
        {
        "role": "user",
        "content": f"Identify design smells in the file, and suggest refactoring changes. Be precise and concise. List only (1) Identified Design Smells, and (2) Suggested Refactoring.\n\n{code_content}"
        },
        {
        "role": "assistant",
        "content": smells,
        },
        {
        "role": "user",
        "content": "Provide a refactored code based on your suggestions. If any refactoring requires modification of external files, skip it. Provide the entire code without any assumptions. Do not include anything apart from the code, as the code would be copy-pasted for testing purposes."
        },
    ],
    temperature=1,
    max_tokens=5034,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    refactored_code = response.choices[0].message.content
    # Code is between ``` and ``` in the response. Keep only that part.
    refactored_code = refactored_code.split("```")[1]

    # Testing purposes: print refactored code
    print(refactored_code)

    # Apply refactoring
    apply_refactoring(file_path, refactored_code)


def main(directory):
    """Iterate over all Python files in the directory, analyze them for design smells, and attempt refactoring."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                
                print("#### FILE: ", file_path)

                # Detect and refactor design smells
                analyze_and_refactor_smells(file_path)

                # Testing purposes: exit after processing one file
                exit()

if __name__ == "__main__":
    directory_to_analyze = "."
    main(directory_to_analyze)
