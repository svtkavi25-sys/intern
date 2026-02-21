import pandas as pd
import numpy as np
import plotly.express as px
import os
import webbrowser
import re
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

    def get_the_prompt(self, task_description=None):
        if self.df is None:
            print("Load the dataset first.")
            return
        if not task_description:
            task_description = input("Enter the EDA/Dashboard task description: ")

        preview = self.df.head(15).to_csv(index=False)
        prompt = f"""
        Dataset Preview: {preview}
        Task: {task_description}
        Requirements:
        1. Clean 'df'.
        2. Create 3+ interactive visualizations (px).
        3. Define 'html_content' as a full HTML/CSS string.
        4. Provide ONLY python code.
        """
        try:
            print("Generating Dashboard Code...")
            response = self.client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            self.generated_code = response.text
        except Exception as e:
            print(f"API Error: {e}")

    def run_code(self): # Remove file_name parameter to handle it inside
        if not self.generated_code:
            print("No code available.")
            return

        # 1. Force the prompt to wait. Adding \n helps clear visual clutter.
        raw_name = input("\n>>> Enter the name for your HTML file: ").strip()
        
        # 2. If user just presses Enter, give it a default name
        if not raw_name:
            file_name = "data_dashboard.html"
        else:
            # Remove illegal characters like < > : " / \ | ? *
            clean_name = re.sub(r'[<>:"/\\|?*]', '', raw_name).strip()
            # Ensure it ends with .html
            file_name = f"{clean_name}.html" if not clean_name.lower().endswith(".html") else clean_name

        # 3. Execute logic
        code_to_exec = self.generated_code.replace("```python", "").replace("```", "").strip()
        local_env = {'df': self.df, 'pd': pd, 'px': px, 'np': np}

        try:
            exec(code_to_exec, local_env)
            html_data = local_env.get('html_content') or local_env.get('html_main')
            
            if html_data:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(html_data)
                
                full_path = os.path.abspath(file_name)
                print(f"Success! Dashboard saved at: {full_path}")
                webbrowser.open('file://' + full_path)
            else:
                print("Error: AI did not define 'html_content'.")
        except Exception as e:
            print(f"Execution Error: {e}")
