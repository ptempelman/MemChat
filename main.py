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


def load_api_key(api_key_filename):
    # If a valid API key has never been entered before, we create a placeholder file
    if not osp.exists(api_key_filename):
        with open(api_key_filename, "w") as file:
            file.write("")

    with open(api_key_filename, "r") as file:
        api_key = file.read()
        # If the API key file is empty, we prompt the user to give theirs
        if not api_key:
            print("Please provide your OpenAI API key:")
            api_key = input()
        return api_key


def validate_api_key(api_key):
    # After a key has been provided, we validate the key by using it to prompt an LLM
    try:
        chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=api_key)
        introduction = chat_model.predict(
            "Very briefly introduce yourself as RillaBot, the personal AI-powered sales assistant"
        )
        print_bot(introduction)
        print_instructions()
        return True

    except openai.AuthenticationError:
        error_message = "ERROR:  API Key is invalid"
        print(f"\033[91m{error_message}\033[0m")
        return False


def retrieve_api_key():
    api_key_filename = "openai_api_key.txt"

    api_key = load_api_key(api_key_filename)

    if validate_api_key(api_key):
        # If a valid API key was provided, we save it locally
        with open(api_key_filename, "w") as file:
            file.write(api_key)
    else:
        # If no valid API key was provided, we try again
        return retrieve_api_key()

    return api_key


def handle_command(command, conversation_memory, tokens_spent, money_spent):
    if command == "x":  # Exit chat
        sys.exit()
    elif command == "w":  # Wipe memory
        conversation_memory.clear()
        print_bot("Done, I forgot our previous chat. Ask me anything!")
    elif command == "t":  # Display spending
        print_bot(
            f"This session you have spent {tokens_spent} tokens which is ${money_spent:.04f}"
        )


if __name__ == "__main__":
    API_KEY = retrieve_api_key()

    conversation_memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", api_key=API_KEY),
        memory=conversation_memory,
    )
    tokens_spent = 0
    money_spent = 0

    while True:
        user_input = input()

        command = user_input.strip().lower()
        if len(command) == 1 and command in ["x", "w", "t"]:
            # If the user is giving a command, we handle that command
            handle_command(command, conversation_memory, tokens_spent, money_spent)
        else:
            # If the user is just chatting, we continue the conversation
            with get_openai_callback() as cb:
                print_bot(conversation.predict(input=user_input))
                tokens_spent += cb.total_tokens
                money_spent += cb.total_cost
