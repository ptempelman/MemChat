import sys
import os.path as osp

import openai
from openai import OpenAI

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI


def print_bot(text):
    print(f"\033[92m{text}\033[0m")


def load_validate_api_key():
    api_key_filename = "openai_api_key.txt"

    # If a valid API key has never been entered before, we create an empty file
    if not osp.exists(api_key_filename):
        with open(api_key_filename, "w") as file:
            file.write("")

    with open(api_key_filename, "r") as file:
        api_key = file.read()
        # If the API key file is empty, we prompt the user to give theirs
        if not api_key:
            print("WARNING:  No OpenAI key was loaded, please provide yours:")
            api_key = input()

        # After a key has been provided, we validate the key by prompting an LLM with it
        try:
            chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=api_key)
            introduction = chat_model.predict(
                "Very briefly introduce yourself as RillaBot, the personal AI-powered sales assistant"
            )
            print_bot(introduction)

        except openai.AuthenticationError:
            print("ERROR:  API Key is invalid")
            sys.exit()

    # If a valid API key was provided, we save it locally
    with open(api_key_filename, "w") as file:
        file.write(api_key)

    return api_key


if __name__ == "__main__":
    API_KEY = load_validate_api_key()

    conversation = ConversationChain(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", api_key=API_KEY),
        memory=ConversationBufferMemory(),
    )

    while True:
        user_input = input()
        print_bot(conversation.predict(input=user_input))
