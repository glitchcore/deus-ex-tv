import openai
from time import sleep
import random
import os

import configuration
from ai_poetry import ai_poetry
from ai_describer import ai_describe

openai.api_key = configuration.api_key

TOPIC_LEN = 5

if __name__ == "__main__":
    topics = ["nothing"]

    while True:
        os.system('clear')
        user_input = input("TYPE YOUR IDENTITY: ")

        # TODO: clear user input, remain [0-9a-Z\.\,\:\-]

        topics += [ai_describe(openai, user_input)]
        topics = topics[-TOPIC_LEN:]

        poetry = ai_poetry(openai, topics)

        print("=== poetry ===")
        for line in poetry:
            print(line)
        print()
        print()

        # add random line as a topic
        try:
            topics += [random.choice(poetry)]
            topics = topics[-TOPIC_LEN:]
        except Exception:
            print(poetry)

        input("[press enter to continue]")