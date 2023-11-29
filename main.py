import sys
import os.path as osp

import openai

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback


def print_bot(text):
    print(f"\033[92m{text}\033[0m")


def print_instructions():
    print_bot(
        "Press [X] to quit our chat \nPress [W] to wipe my memory \nPress [T] to see total tokens spent \nOr just ask me anything!"
    )


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
            print_instructions()

        except openai.AuthenticationError:
            print("ERROR:  API Key is invalid")
            sys.exit()

    # If a valid API key was provided, we save it locally
    with open(api_key_filename, "w") as file:
        file.write(api_key)

    return api_key


if __name__ == "__main__":
    API_KEY = load_validate_api_key()

    conversation_memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", api_key=API_KEY),
        memory=conversation_memory,
    )
    tokens_spent = 0
    money_spent = 0

    while True:
        user_input = input()

        # We check if the user is giving a command, instead of chatting with the bot
        if user_input.strip() == "x" or user_input.strip() == "X":  # Exit chat
            break
        elif user_input.strip() == "w" or user_input.strip() == "W":  # Wipe memory
            conversation_memory.clear()
            print_bot("Done, I forgot our previous chat. Ask me anything!")
            continue
        elif user_input.strip() == "t" or user_input.strip() == "T":  # Request spending
            print_bot(
                f"In this session you have currently spent {tokens_spent} tokens which is ${money_spent:.04f}"
            )
            continue

        with get_openai_callback() as cb:
            print_bot(conversation.predict(input=user_input))
            tokens_spent += cb.total_tokens
            money_spent += cb.total_cost
