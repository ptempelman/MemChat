# RillaChat
An AI powered chatbot with memory that runs in the terminal. 


## Prerequisites
This project assumes the following to be already installed. 
* Python (version >3.8)
* pip (Python package manager)

## Setup
After the repository is cloned, open a terminal inside the main project folder. We recommend the user to make a virtual environment to install the dependencies.

#### 1. Create a virtual environment
```bash
python3 -m venv .venv
```

#### 2. Activate the virtual environment
* On Windows:
```bash
.venv\Scripts\activate
```


* On MacOS and Linux:
```bash
source .venv/bin/Activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the application
```bash
python3 main.py
```
The application will then prompt you for your OpenAI api key which you can find [here](https://platform.openai.com/api-keys). 