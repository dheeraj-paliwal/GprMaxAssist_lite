# gprMaxAssist_lite 🤖

A free and computationally cheaper chatbot to assist users with gprMax simulations, leveraging open-source Large Language Models (LLMs).

## ✨ Project Overview

This project aims to build upon previous work in developing an AI chatbot for gprMax. The key goal is to create a lightweight and accessible chatbot using open-source LLMs like Lama and DeepSeek, offering a free alternative to existing solutions.

The chatbot will be capable of:

* Answering questions related to gprMax usage and commands. 🤔
* Providing guidance on building gprMax models. 🏗️
* (Future Goal) Automatically generating gprMax models based on instructions. 🚀

This chatbot is developed using Python.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/dheeraj-paliwal/GprMaxAssist_lite](https://github.com/dheeraj-paliwal/GprMaxAssist_lite)
    cd GprMaxAssist_lite
    ```

2.  **Ensure you have Python installed** (version 3.6 or later recommended).

3.  **(Optional but Recommended) Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

4.  **(Optional) Install dependencies (if you add any later):**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

Run the chatbot script from your terminal:

```bash
python gprMaxAssist_lite.py

Once the chatbot starts, you can interact with it by typing natural language questions or commands.
 * Type help to see a list of available commands and how to interact. ❓
 * Describe your gprMax simulation setup (e.g., "domain size is 1.0 by 0.5 by 0.2 meters").
 * Ask questions about gprMax commands or concepts.
 * Type show setup to see the current simulation parameters you've defined.
 * Type done to generate the basic gprMax input file commands based on your setup. ✅
 * Type exit to close the chatbot. 👋
📂 Project Structure
GprMaxAssist_lite/
├──gprMaxAssist_lite.py           # The main Python script for the chatbot
├── README.md
└── .gitignore



💡 Future Work
 * Implement more sophisticated Natural Language Understanding (NLU) using libraries like spaCy or NLTK.
 * Integrate with open-source LLMs (Lama, DeepSeek) for more intelligent responses and model building capabilities.
 * Expand the knowledge base to cover more gprMax commands and features.
 * Support more complex geometry definitions and simulation parameters.
 * Develop the functionality to automatically generate full gprMax input files.
 * Potentially explore a web-based user interface using frameworks like Gradio or Streamlit.
