#doc_generator.py

import os
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from config import model_name
from dotenv import load_dotenv
from file_utils import create_directory, move_files_to_directory
import openai

load_dotenv()
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.2)

filePrompt = """
# Title/Heading: File Documentation

Introduction: Provide a brief introduction to the code file. Explain its purpose, functionality, and any important background information.

Usage: Describe how to use the code file. Provide examples and usage scenarios to help users understand how it should be utilized.

Functions/Methods: If the code file contains functions or methods, document each of them individually. Include the function name, purpose, input parameters, return values, and any important details about how to use them.

Classes: If the code file contains classes, document each class individually. Describe the purpose of the class, its attributes, methods, and any relevant information about how to work with the class.

Examples: Provide code examples to demonstrate the usage of the code file. Show how the code should be structured and provide explanations for each step.

Dependencies: List any dependencies or required libraries/packages for the code file.

Additional Information: Include any additional information that may be useful for understanding or working with the code file. This can include troubleshooting tips, known issues, or any special considerations.
"""

folderPrompt = """
# Title/Heading: Folder Documentation

Introduction: Provide a brief introduction to the code folder. Explain its purpose, functionality, and any important background information.

Usage: Describe how to use the code folder. Provide examples and usage scenarios to help users understand how it should be utilized.

Files: List all the files in the folder and provide a brief description of each file's purpose.

Classes: If the code folder contains classes, document each class individually. Describe the purpose of the class, its attributes, methods, and any relevant information about how to work with the class.

Functions/Methods: If the code folder contains shared functions or methods, document each of them individually. Include the function name, purpose, input parameters, return values, and any important details about how to use them.

Examples: Provide code examples to demonstrate the usage of the code files in the folder. Show how the code should be structured and provide explanations for each step.

Dependencies: List any dependencies or required libraries/packages for the code files in the folder.

Additional Information: Include any additional information that may be useful for understanding or working with the code folder. This can include troubleshooting tips, known issues, or any special considerations.
"""



chatPrompt = ""
MAX_TOKENS = 3800  # OpenAI maximum is 4096. Leave some room for the prompt.

def is_text_file(file_path):
    text_extensions = ['.txt', '.md', '.py', '.java', '.cpp', '.h', '.html', '.css', '.js']
    ext = os.path.splitext(file_path)[1]
    return ext.lower() in text_extensions

def chunkify(input_text, max_tokens):
    words = input_text.split(' ')
    chunks = []
    current_chunk = ''
    for word in words:
        if len((current_chunk + ' ' + word).split(' ')) <= max_tokens:
            current_chunk += ' ' + word
        else:
            chunks.append(current_chunk)
            current_chunk = word
    chunks.append(current_chunk)
    return chunks

def generate_file_documentation(file_path):
    if not is_text_file(file_path):
        print(f'Skipping non-text file: {file_path}')
        return None
    with open(file_path, 'r', errors='ignore') as file:
        code = file.read()
        chunks = chunkify(code, MAX_TOKENS)
    documentation_parts = []
    for chunk in chunks:
        prompt = f'{filePrompt} {chunk}'
        try:
            response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0.2, max_tokens=300)
            documentation_parts.append(response.choices[0].text.strip())
        except Exception as e:
            print(f"An error occurred: {e}")
    documentation = '\n\n'.join(documentation_parts)
    return documentation.strip()



def generate_folder_documentation(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    prompt = folderPrompt + ' '.join(files)
    documentation = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0.2, max_tokens=400)
    return documentation.choices[0].text.strip()
    
def generate_documentation(local_dir):
    autodocs_dir = os.path.join(local_dir, 'autodocs')
    create_directory(autodocs_dir)
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            file_path = os.path.join(root, file)
            documentation = generate_file_documentation(file_path)
            # Only write to the file if documentation is not None
            if documentation is not None:
                with open(file_path + '.md', 'w') as doc_file:
                    doc_file.write(documentation)
        if dirs:
            documentation = generate_folder_documentation(root)
            # Only write to the file if documentation is not None
            if documentation is not None:
                with open(root + '/README.md', 'w') as doc_file:
                    doc_file.write(documentation)
    move_files_to_directory(local_dir, autodocs_dir)


