import openai
from time import sleep
import os

import configuration
from ai_poetry import ai_poetry
from ai_describer import ai_describe

openai.api_key = configuration.api_key

if __name__ == "__main__":
    description = "void"

    while True:
        os.system('clear')
        user_input = input("TYPE YOUR IDENTITY: ")

        # TODO: clear user input, remain [0-9a-Z\.\,\:\-]

        # user_description = ai_describe(openai, user_input)

        print("user description:", user_input)

        poetry = ai_poetry(openai, description, user_input)

        print("=== poetry ===")
        for line in poetry:
            print(line)
        print()
        print()

        description = ai_describe(openai, poetry)

        print("description:", description)

        input("[press enter to continue]")