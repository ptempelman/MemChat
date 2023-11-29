from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

if __name__ == "__main__":
    while True:
        user_input = input()

        print(f"Interesting that you said {user_input}")
