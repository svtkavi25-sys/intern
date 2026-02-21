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
            print(f"Loaded '{file_path}' with {self.df.shape[0]} rows.")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def get_the_prompt(self, task_description: str):
        if self.df is None: return

        # Send summary statistics so the AI understands the 'story' of the data
        preview = self.df.describe(include='all').to_string()

        prompt = f"""
        You are a Data Storyteller and Web Developer.
        DATASET CONTEXT: {preview}
        TASK: {task_description}

        REQUIREMENTS (CRITICAL):
        1. NO IMAGES OR GRAPHS: Do not use <img> tags or charting libraries.
        2. NO TABLES OR RAW DATA: Convert numerical findings into a human-readable text narrative.
        3. STRUCTURE: Create a clean, modern "Text-Based Report" using Bootstrap 5. 
           Use <div class="container">, <h1 class="display-4">, and <p class="lead"> tags.
        4. STYLE: Use a professional color palette (e.g., dark text on a light gray background).
        5. OUTPUT: Provide ONLY the python code that defines the variable 'html_content'. No explanation, no backticks.
        """

        try:
            print("Generating Text-Based Narrative Report...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt
            )
            # Remove any potential markdown wrapping from AI response
            self.generated_code = response.text.replace("```python", "").replace("```", "").strip()
        except Exception as e:
            print(f"API Error: {e}")

    def run_code(self):
        if not self.generated_code:
            print("No code available. Please check your API quota or connection.")
            return

        local_env = {'df': self.df, 'pd': pd, 'np': np}

        try:
            # Execute the AI-generated logic to build 'html_content'
            exec(self.generated_code, local_env)
            
            if 'html_content' in local_env:
                file_name = "text_data_story.html"
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(local_env['html_content'])
                
                full_path = os.path.realpath(file_name)
                print(f"Success! Text Report saved at: {full_path}")
                webbrowser.open('file://' + full_path)
            else:
                print("Error: The AI code failed to define 'html_content'.")
        except Exception as e:
            print(f"Execution Error: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    bot = AIassistant()
    # Path to your dataset
    path = r"C:\python\python webinnor\dataset.csv" 
    
    bot.load_csv(path)
    # Triggering the clean text-only narrative mode
    bot.get_the_prompt("Create a professional text-only data story. No images, no graphs, and no raw data tables.")
    bot.run_code()
