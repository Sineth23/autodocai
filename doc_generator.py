#doc_generator.py

import os
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from config import model_name
from dotenv import load_dotenv
import openai

load_dotenv()
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.2)

filePrompt = """
Write a detailed technical explanation of what this code does. 
Focus on the high-level purpose of the code and how it may be used in the larger project.
Include code examples where appropriate. Keep you response between 100 and 300 words. 
DO NOT RETURN MORE THAN 300 WORDS.
Output should be in markdown format.
Do not just list the methods and classes in this file.
"""

folderPrompt = """
Write a technical explanation of what the code in this file does
and how it might fit into the larger project or work with other parts of the project.
Give examples of how this code might be used. Include code examples where appropriate.
Be concise. Include any information that may be relevant to a developer who is curious about this code.
Keep you response under 400 words. Output should be in markdown format.
Do not just list the files and folders in this folder.
"""

chatPrompt = ""


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

def generate_file_documentation(file_path, max_tokens=2048):
    with open(file_path, 'r') as file:
        code = file.read()
    chunks = chunkify(code, max_tokens)
    documentation_parts = []
    for chunk in chunks:
        prompt = filePrompt + chunk
        response = openai.Completion.create(engine=model_name, prompt=prompt, temperature=0.2, max_tokens=300)
        documentation_parts.append(response.choices[0].text.strip())
    return "\n".join(documentation_parts)


def generate_folder_documentation(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    prompt = folderPrompt + ' '.join(files)
    documentation = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0.2, max_tokens=400)
    return documentation.choices[0].text.strip()

def generate_documentation(local_dir):
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            file_path = os.path.join(root, file)
            documentation = generate_file_documentation(file_path)
            with open(file_path + '.md', 'w') as doc_file:
                doc_file.write(documentation)
        if dirs:
            documentation = generate_folder_documentation(root)
            with open(root + '/README.md', 'w') as doc_file:
                doc_file.write(documentation)

