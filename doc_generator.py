import os
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from config import model_name
from dotenv import load_dotenv

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

def generate_file_documentation(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    prompt = PromptTemplate(filePrompt) + code
    documentation = llm.create_completion(prompt, temperature=0.2, max_tokens=300)
    return documentation

def generate_folder_documentation(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    prompt = PromptTemplate(folderPrompt) + ' '.join(files)
    documentation = llm.create_completion(prompt, temperature=0.2, max_tokens=400)
    return documentation


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

