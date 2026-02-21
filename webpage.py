import numpy as np
import pandas as pd
import os
import webbrowser
from google import genai

class AIassistant:
    def __init__(self):
        self.df = None
        self.generated_code = ""
        self.api_key = "AIzaSyBx8LB5t8wXU6zWGEJm8HMEGksmAYqj3PY"
        self.client = genai.Client(api_key=self.api_key)

    def load_csv(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            print(f"Loaded '{file_path}' with {self.df.shape[0]} rows.")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def get_the_prompt(self, task_description: str):
        if self.df is None:
            print("No dataset loaded.")
            return

        preview = self.df.head(20).to_csv(index=False)
        
        prompt = f"""
        You are a Web Developer. 
        Dataset Preview:
        {preview}
        
        Task: {task_description}
        
        Requirements:
        1. Clean the 'df' DataFrame.
        2. REMOVE ALL GRAPHS. Do not use plotly or any charting libraries.
        3. Create a single variable 'html_content' which is a full HTML/CSS string.
        4. Use Bootstrap 5 CDN for styling.
        5. Build a professional, responsive HTML table to display the data.
        6. Provide ONLY the python code. No explanation, no markdown backticks.
        """

        try:
            print("Generating Web Page Code...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt
            )
            self.generated_code = response.text
        except Exception as e:
            print(f"API Error: {e}")

    def run_code(self):
        if not self.generated_code:
            print("No code to execute.")
            return

        code_to_exec = self.generated_code.replace("```python", "").replace("```", "").strip()
        
        local_env = {'df': self.df, 'pd': pd, 'np': np}

        try:
            exec(code_to_exec, local_env)
            
            if 'html_content' in local_env:
                file_name = "data_webpage.html"
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(local_env['html_content'])
                
                full_path = os.path.realpath(file_name)
                print(f"Success! Web page saved at: {full_path}")
                webbrowser.open('file://' + full_path)
            else:
                print("Error: 'html_content' was not defined by the AI.")
        except Exception as e:
            print(f"Execution Error: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    bot = AIassistant()
    path = r"C:\python\python webinnor\dataset.csv" 
    
    bot.load_csv(path)
    bot.get_the_prompt("Create a clean web page with a data table and summary stats. No graphs.")
    bot.run_code()

