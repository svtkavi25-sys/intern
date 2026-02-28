# AI Assistant Automation

A Python-based AI Assistant project that loads a CSV dataset, accepts a user task description, and dynamically generates or executes code based on the provided prompt.

This project demonstrates a simple AI workflow automation using Python.

---

## Overview

This application performs the following steps:

1. Initializes an AI assistant
2. Loads data from a CSV file
3. Accepts a task description from the user
4. Generates and executes code automatically

---

## Project Structure

```
project-folder/
│
├── main.py              # Main script (entry point)
├── function.py          # AIassistant class implementation
├── dataset.csv          # Input dataset
└── README.md            # Project documentation
```

---

## Features

* AI assistant initialization
* CSV dataset loading
* Interactive user prompt input
* Automated code execution
* Modular Python design

---

## How the Program Works

The main script runs the AI assistant using the following workflow:

```python
from function import AIassistant

bot = AIassistant()

# Load dataset
bot.load_csv(r"C:\python\python webinnor\dataset.csv")

# Ask user for task description
bot.get_the_prompt()

# Execute generated code
bot.run_code()
```

---

## Requirements

Install required dependencies:

```bash
pip install pandas
```

(Add other libraries if used inside `function.py`.)

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repository-name.git
```

### 2. Go to project directory

```bash
cd your-repository-name
```

### 3. Run the program

```bash
python main.py
```

---

## Dataset Setup

Place your dataset file inside the project folder:

```
dataset.csv
```

Then update the path if necessary:

```python
bot.load_csv("dataset.csv")
```

---

## Customization

You can extend this project by:

* Modifying AI logic inside `function.py`
* Adding multiple datasets
* Creating a web interface using Flask or FastAPI
* Adding logging and error handling
* Connecting external AI APIs

---

## Future Improvements

* Web dashboard interface
* Chat memory support
* API integration
* Improved prompt handling
* Automatic dataset detection

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Submit a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Author

S.V.Kavi
GitHub:  https://github.com/svtkavi25-sys/intern.git

---
