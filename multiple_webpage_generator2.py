import numpy as np
import pandas as pd
import os
import webbrowser
from google import genai

class AIassistant:
    def __init__(self):
        self.df = None
        self.generated_code = ""
        # IMPORTANT: Ensure your Gemini API Key is valid
        self.api_key = "AIzaSyBx8LB5t8wXU6zWGEJm8HMEGksmAYqj3PY"
        self.client = genai.Client(api_key=self.api_key)

    def load_csv(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            print(f"Loaded '{file_path}' with {self.df.shape[0]} rows and {self.df.shape[1]} columns.")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def get_the_prompt(self, task_description: str):
        if self.df is None:
            print("No dataset loaded.")
            return

        # Provides a statistical summary so the AI can write meaningful health narratives
        preview = self.df.describe(include='all').to_string()

        prompt = f"""
        You are a Health Data Scientist and Web Developer.
        DATASET CONTEXT (Pima Indians Diabetes Summary):
        {preview}

        TASK: {task_description}

        REQUIREMENTS (CRITICAL):
        1. CREATE TWO PAGES: Define two variables 'html_main' (The Story) and 'html_stats' (Detailed Analysis).
        2. NO TABLES OR RAW DATA: Convert numerical findings into professional medical insights.
        3. INTEGRATE IMAGES: Use <img> tags with high-quality source URLs from LoremFlickr.
           Format: <img src="https://loremflickr.com[keyword]" 
                       class="img-fluid rounded mb-4 shadow" 
                       onerror="this.src='https://picsum.photos'; this.onerror=null;">
           (AI: Replace [keyword] with medical terms like 'diabetes', 'health', or 'medicine').
        4. STRUCTURE: Use Bootstrap 5 for both pages. Include large headings, cards, and clean typography.
        5. LINKING: Add a prominent button in 'html_main' to open 'page_stats.html' and vice-versa.
        6. OUTPUT: Provide ONLY the python code that defines these two variables. No explanation, no markdown backticks.
        """

        try:
            print("Generating Visual Story and Detailed Analysis Pages...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt
            )
            # Remove any potential markdown wrapping from AI response
            clean_code = response.text.replace("```python", "").replace("```", "").strip()
            self.generated_code = clean_code
        except Exception as e:
            print(f"API Error: {e}")

    def run_code(self):
        if not self.generated_code:
            print("No code available. Please check your API quota.")
            return

        local_env = {'df': self.df, 'pd': pd, 'np': np}

        try:
            # Execute the AI-generated logic to build the two HTML variables
            exec(self.generated_code, local_env)
            
            # Save and open Page 1: Narrative Story
            if 'html_main' in local_env:
                main_file = "page_main1.html"
                with open(main_file, "w", encoding="utf-8") as f:
                    f.write(local_env['html_main'])
                print(f"Success! Page 1 saved: {os.path.realpath(main_file)}")
                webbrowser.open('file://' + os.path.realpath(main_file))

            # Save Page 2: Detailed Clinical Breakdown
            if 'html_stats' in local_env:
                stats_file = "page_stats1.html"
                with open(stats_file, "w", encoding="utf-8") as f:
                    f.write(local_env['html_stats'])
                print(f"Success! Page 2 saved: {os.path.realpath(stats_file)}")
                
        except Exception as e:
            print(f"Execution Error: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    bot = AIassistant()
    # Path to your local CSV file
    path = r"C:\python\python webinnor\piam-indians-diabates.csv" 
    
    bot.load_csv(path)
    # The prompt triggers both storytelling and imagery for medical reporting
    bot.get_the_prompt("Create a professional health story page and a secondary detailed analysis page using medical imagery.")
    bot.run_code()
