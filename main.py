from git_utils import clone_github_repo
from doc_generator import generate_documentation
from file_utils import create_directory, move_files_to_directory
from config import model_name
import os
# Now you can use OPENAI_API_KEY and MODEL_NAME in your script
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    github_url = input("Enter a GitHub repository URL to clone: ")
    local_dir = github_url.split('/')[-1].replace('.git', '')
    
    if clone_github_repo(github_url, local_dir):
        print("Repository cloned.")
        generate_documentation(local_dir)
        print("Documentation generated.")
        #create_directory('autodocs')
        move_files_to_directory(local_dir, 'autodocs')
        print("Documentation moved to autodocs directory.")

if __name__ == '__main__':
    main()
