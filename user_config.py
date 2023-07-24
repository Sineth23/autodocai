import os
import json

DEFAULT_USER_CONFIG = {
    "llms": []
}

USER_CONFIG_FILE = "autodoc_user_config.json"

def load_user_config():
    if os.path.exists(USER_CONFIG_FILE):
        with open(USER_CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        return DEFAULT_USER_CONFIG

def save_user_config(user_config):
    with open(USER_CONFIG_FILE, "w") as file:
        json.dump(user_config, file, indent=4)

def prompt_user_for_llms():
    available_llms = ["GPT-3.5 Turbo", "GPT-4 8K (Early Access)", "GPT-4 32K (Early Access)"]
    user_config = load_user_config()
    
    print("Available Language Models:")
    for i, llm in enumerate(available_llms, start=1):
        print(f"{i}. {llm}")
    
    while True:
        try:
            selected_indexes = input("Enter the index(es) of the Language Model(s) you want to use (comma-separated): ")
            selected_indexes = [int(idx.strip()) - 1 for idx in selected_indexes.split(",")]
            
            if not all(0 <= idx < len(available_llms) for idx in selected_indexes):
                raise ValueError("Invalid index.")
            
            selected_llms = [available_llms[idx] for idx in selected_indexes]
            user_config["llms"] = selected_llms
            save_user_config(user_config)
            print("User configuration saved.")
            return selected_llms
        except ValueError as e:
            print("Invalid input. Please try again.")
