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
# Title: File Documentation

Introduction: Provide a brief introduction about the code file. Explain its purpose, functionality, and any important background information.

Usage: Describe how to use the code file. Provide examples and usage scenarios to help users understand how it should be utilized.

Functions/Methods: For each function or method in the code file, provide the following details - function name, purpose, input parameters, return values, and any important details about how to use them.

Classes: For each class in the code file, provide the following details - class name, purpose, attributes, methods, and any relevant information about how to work with the class.

Examples: Provide code examples demonstrating how to use the various features of the code file.

"""

folderPrompt = """
# Title: Folder Documentation

Introduction: Provide a brief introduction about the code folder. Explain its purpose, functionality, and any important background information.

Usage: Describe how to use the code folder. Provide examples and usage scenarios to help users understand how it should be utilized.

Files: List all the files in the folder and provide a brief description of each file's purpose.

Classes: For each class in the code folder, provide the following details - class name, purpose, attributes, methods, and any relevant information about how to work with the class.

Functions/Methods: For each shared function or method in the code folder, provide the following details - function name, purpose, input parameters, return values, and any important details about how to use them.

Examples: Provide code examples demonstrating how to use the various features of the code folder.


"""



chatPrompt = ""
MAX_TOKENS = 3800  # OpenAI maximum is 4096. Leave some room for the prompt.

def is_text_file(file_path):
    text_extensions = ['.txt', '.md', '.py', '.java', '.cpp', '.h', '.html', '.css', '.js']
    ext = os.path.splitext(file_path)[1]
    return ext.lower() in text_extensions


def chunkify(input_text, max_tokens):
    lines = input_text.split('\n')
    chunks = []
    current_chunk = ''
    for line in lines:
        if len((current_chunk + ' ' + line).split(' ')) <= max_tokens:
            current_chunk += ' ' + line
        else:
            chunks.append(current_chunk)
            current_chunk = line
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


import re

#def chunkify1(input_text, language, max_tokens):
 #   function_patterns = {
 #       'python': re.compile(r"(def [\w_]+\(.+\):)"),
 #       'javascript': re.compile(r"(function [\w_]+\(.+\) \{)"),
 #       # Add other languages here
 #   }

    #if language not in function_patterns:
    #    raise ValueError(f"Unsupported language: {language}")
    
   # parts = function_patterns[language].split(input_text)
    
    #chunks = []
    #current_chunk = ''

    #for part in parts:
     #   if len((current_chunk + ' ' + part).split(' ')) <= max_tokens:
           # current_chunk += ' ' + part
      #  else:
       #     chunks.append(current_chunk)
        #    current_chunk = part
    
   # chunks.append(current_chunk)
    #return chunks
