import numpy as np
import pandas as pd
import plotly.express as px
import joblib
import io
import os
import webbrowser
import contextlib
from google import genai

class AIassistant:
    def __init__(self):
        self.df = None
        self.generated_code = ""
        self.output_text = ""
        # Using the API key you provided
        api_key = "AIzaSyCnl3FwhEMLRUGYPGKvO0ifQhJZ3UfFCPQ"
        self.client = genai.Client(api_key=api_key)

    def load_csv(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            print(f"Loaded '{file_path}' with {self.df.shape[0]} rows and {self.df.shape[1]} columns.")
        except Exception as e:
            print(f"Error occurred during loading: {e}")

    def get_the_prompt(self, task_description: str):
        if self.df is None:
            print("Load the dataset first using load_csv()..")
            return

        preview = self.df.head(15).to_csv(index=False)
        
        prompt = f"""
        You are a Data Scientist that specializes in Interactive Web Dashboards.
        Dataset Preview:
        {preview}
        Task: {task_description}
        Requirements:
        1. Clean and preprocess the 'df' DataFrame.
        2. Create 3+ interactive visualizations using 'plotly.express' (px).
        3. Create a single variable named 'html_content' which is a full HTML/CSS string.
        4. Use Bootstrap CDN for styling.
        5. Embed charts using 'fig.to_html(full_html=False, include_plotlyjs="cdn")'.
        6. Provide ONLY the python code. No explanation.
        """

        # REMOVED RETRY LOOP: Single direct attempt
        try:
            print("Generating Dashboard Code...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt
            )
            self.generated_code = response.text
        except Exception as e:
            print(f"API Error: {e}")

    def run_code(self):
        if not self.generated_code:
            print("No code available. Check your API quota or key.")
            return

        code_to_exec = self.generated_code.replace("```python", "").replace("```", "").strip()
        local_env = {'df': self.df, 'pd': pd, 'px': px, 'np': np}

        try:
            exec(code_to_exec, local_env)
            
            if 'html_content' in local_env:
                file_name = "data_dashboard.html"
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(local_env['html_content'])
                
                full_path = os.path.realpath(file_name)
                print(f"Success! Dashboard saved at: {full_path}")
                webbrowser.open('file://' + full_path)
            else:
                print("Error: The AI code did not define 'html_content'.")
        except Exception as e:
            print(f"Execution Error: {e}")

# --- EXECUTION ---
bot = AIassistant()
path = r"C:\python\python webinnor\dataset.csv" 

bot.load_csv(path)
bot.get_the_prompt("Perform full EDA and create a professional dashboard.")
bot.run_code()
