import sys
import os.path as osp

import openai

from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI


def print_bot(text):
    """Prints given text in a lime green colour.

    Args:
        text (str): text to be printed in bot format
    """
    print(f"\033[92m{text}\033[0m")


def print_instructions():
    """Prints the session management instructions."""
    print_bot(
        "Press [X] to quit our chat \n"
        + "Press [W] to wipe my memory \n"
        + "Press [T] to see total tokens spent \n"
        + "Or just ask me anything!"
    )


def load_api_key(api_key_filename):
    """
    Attempts to load a locally saved API key, if it
    does not exist we prompt the user to give one.

    Args:
        api_key_filename (str): indicates the file where the API key would be saved locally

    Returns:
        str: OpenAI API key
    """
    if not osp.exists(api_key_filename):
        with open(api_key_filename, "w", encoding="utf-8") as file:
            file.write("")

    with open(api_key_filename, "r", encoding="utf-8") as file:
        api_key = file.read()
        # If the API key file is empty, we prompt the user to give theirs
        if not api_key:
            print("To start the chat, please provide your OpenAI API key:")
            api_key = input()
        return api_key


def validate_api_key(api_key):
    """Validates a key by using it to prompt an LLM.

    Args:
        api_key (str): OpenAI API key

    Returns:
        bool: returns true if the key is valid
    """
    try:
        chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=api_key)
        introduction = chat_model.predict(
            "Very briefly introduce yourself as RillaBot, the personal AI-powered sales assistant"
        )
        print_bot(introduction)
        return True

    except openai.AuthenticationError:
        error_message = "ERROR:  API Key is invalid"
        print(f"\033[91m{error_message}\033[0m")
        return False


def retrieve_api_key():
    """
    Retrieves an API key from a local file or by prompting the user,
    keeps trying until a valid key is provided.

    Returns:
        str: OpenAI API key
    """
    api_key_filename = "openai_api_key.txt"

    api_key = load_api_key(api_key_filename)

    if validate_api_key(api_key):
        # If a valid API key was provided, we save it locally and provide instructions
        with open(api_key_filename, "w", encoding="utf-8") as file:
            file.write(api_key)
        print_instructions()
    else:
        # If no valid API key was provided, we try again
        return retrieve_api_key()

    return api_key


def handle_command(command, chat_memory, total_tokens_spent, total_money_spent):
    """Handles a user session management command.

    Args:
        command (str): user input that controls session management
        chat_memory (ConversationBufferMemory): the chat memory to be wiped
        tokens_spent (float): the tokens spent in this session
        money_spent (float): the money spent in this session
    """
    if command == "x":  # Exit chat
        sys.exit()
    elif command == "w":  # Wipe memory
        chat_memory.clear()
        print_bot("Done, I forgot our previous chat. Ask me anything!")
    elif command == "t":  # Display spending
        print_bot(
            f"This session you have spent {total_tokens_spent} tokens"
            + f" which is ${total_money_spent:.04f}"
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

        user_command = user_input.strip().lower()
        if len(user_command) == 1 and user_command in ["x", "w", "t"]:
            # If the user is giving a command, we handle that command
            handle_command(user_command, conversation_memory, tokens_spent, money_spent)
        else:
            # If the user is just chatting, we continue the conversation
            with get_openai_callback() as cb:
                print_bot(conversation.predict(input=user_input))
                tokens_spent += cb.total_tokens
                money_spent += cb.total_cost
