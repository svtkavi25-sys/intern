import numpy as np
import pandas as pd
import os
import webbrowser
from google import genai

class AIassistant:
    def __init__(self):
        self.df = None
        self.generated_code = ""
        # IMPORTANT: Replace with your actual Gemini API Key
        self.api_key = "AIzaSyBx8LB5t8wXU6zWGEJm8HMEGksmAYqj3PY"
        self.client = genai.Client(api_key=self.api_key)

    def load_csv(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            print(f"Loaded '{file_path}' with {self.df.shape} rows.")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def get_the_prompt(self, task_description: str):
        if self.df is None: return
        preview = self.df.describe(include='all').to_string()

        prompt = f"""
        You are a Data Storyteller. 
        DATASET CONTEXT: {preview}
        
        TASK: {task_description}

        REQUIREMENTS:
        1. Create TWO variables: 'html_main' (The Story) and 'html_stats' (Detailed Text Breakdown).
        2. NO IMAGES, NO GRAPHS, NO TABLES.
        3. Use Bootstrap 5 for both.
        4. Link them together: In 'html_main', add a link to 'page_stats.html'. In 'html_stats', add a link back to 'page_main.html'.
        5. OUTPUT: Provide ONLY the python code defining these two variables. No explanation.
        """

        try:
            print("Generating multiple web pages...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt
            )
            self.generated_code = response.text.replace("```python", "").replace("```", "").strip()
        except Exception as e:
            print(f"API Error: {e}")

    def run_code(self):
        if not self.generated_code: return

        local_env = {'df': self.df, 'pd': pd, 'np': np}

        try:
            exec(self.generated_code, local_env)
            
            # Save Page 1: Main Story
            if 'html_main' in local_env:
                with open("page_main.html", "w", encoding="utf-8") as f:
                    f.write(local_env['html_main'])
                webbrowser.open('file://' + os.path.realpath("page_main.html"))

            # Save Page 2: Detailed Stats
            if 'html_stats' in local_env:
                with open("page_stats.html", "w", encoding="utf-8") as f:
                    f.write(local_env['html_stats'])
                print("Success! Created 'page_main.html' and 'page_stats.html'.")
                
        except Exception as e:
            print(f"Execution Error: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    bot = AIassistant()
    path = r"C:\python\python webinnor\piam-indians-diabates.csv"
    
    bot.load_csv(path)
    bot.get_the_prompt("Create a main narrative page and a secondary detailed text summary page.")
    bot.run_code()
