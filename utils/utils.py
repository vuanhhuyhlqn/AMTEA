import os
from solver import Solver
import logging
import re
import inspect
import hydra
import random
import string
from LLM.llm_models import *

def init_llm_model(model_name: str):
    if model_name == "gpt":
        from openai import OpenAI
        client = OpenAI()
        model = GPTModel("gpt-4o-mini", client)
        
    elif model_name == "gemini":
        from google import genai
        client = genai.Client()
        model = GeminiModel("gemini-2.5-flash", client)
        
    return model
    
def get_prompt(opt: str):
	parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
	file_path = os.path.join(parent_dir, f"LLM\\prompts\\texts\\{opt}.txt")
	prompt_file = open(file_path)
	prompt = prompt_file.read()
	prompt_file.close()
	return prompt

def get_code(solver_id, folder='cache/solvers'):
    file_path = os.path.join(folder, f"{solver_id}.py")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"No file found: {file_path}")
        return None

def save_code(code_str, folder='cache/solvers'):
    chars = string.ascii_letters + string.digits  
    rand_id = ''.join(random.choices(chars, k=4)) 
    filename = f"{rand_id}.py"
    file_path = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code_str)
    return rand_id

def delete_solver_file(solver_id, folder_path='cache/solvers'):
    file_path = os.path.join(folder_path, f"{solver_id}.py")
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    else:
        print(f"No file found: {file_path}")
        
def delete_all(folder_path='cache/solvers'):
    exclude_files = {'ga.py', 'de.py'} 
    for filename in os.listdir(folder_path):
        if filename.endswith('.py') and filename not in exclude_files:
            file_path = os.path.join(folder_path, filename)
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")