from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from config import model_name
from dotenv import load_dotenv

def generate_documentation(local_dir):
    load_dotenv()
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.2)

    # This is where you would implement the function to generate the documentation.
    # The implementation of this function depends on your exact requirements and the structure of your code.
    # For example, you could iterate through the files in the repository, call a function to generate
    # the documentation for each file, and write the documentation to a .md file in the local directory.
