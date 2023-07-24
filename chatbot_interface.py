from langchain import LanguageModelChain

def chatbot_interface(prompt, language_model_chain):
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = language_model_chain.process_text(prompt + user_input)
        print("Chatbot:", response)
