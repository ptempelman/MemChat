import sys

import openai
from openai import OpenAI

from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI


def print_bot(text):
    print(f"\033[92m{text}\033[0m")


if __name__ == "__main__":
    with open("openai_api_key.txt", "r") as file:
        API_KEY = file.read()
        if not API_KEY:
            print(
                "ERROR:  No OpenAI key was provided, please add yours to openai_api_key.txt"
            )
            sys.exit()
        else:
            try:
                chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=API_KEY)
                introduction = chat_model.predict(
                    "Very briefly introduce yourself as RillaBot, the personal AI-powered sales assistant"
                )
                print_bot(introduction)

            except openai.AuthenticationError:
                print("ERROR:  API Key is invalid")
                sys.exit()

    while True:
        chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=API_KEY)

        user_input = input()

        print_bot(chat_model.predict(user_input))
