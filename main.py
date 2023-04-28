import openai
from time import sleep
import os
import re
import requests
import random

import configuration
from fate_gen import ai_answer
from glitch_ui import *
from offline import offline_answers

openai.api_key = configuration.api_key

if __name__ == "__main__":
    '''
    while True:
        a = ai_answer(openai, "no user input, imagine your own and improvise")
        print(f"\"{a}\",")
    '''

    while True:
        os.system('clear')
        print()
        user_input = input("  TYPE YOUR IDENTITY: ")
        user_input = re.sub("[^a-zA-Z\s]+", "", user_input)

        try:
            requests.post("http://localhost:8002", data={"prompt": user_input}, timeout=2)
        except Exception:
            pass

        print("")

        print("  [WAIT FOR MACHINE...]", end='', flush=True)

        # TODO in case of timeout get answer from static list

        answer = ai_answer(openai, user_input)

        if answer is None:
            answer = random.choice(offline_answers)

        print("\r                          \r", end='', flush=True)
        slow_print(answer)
        print()
        print()

        blink_message("  [PRESS ENTER TO CONTINUE]", 0.4)

        random_chars(0.1, 1000)
        sleep(0.2)
        os.system('clear')
        sleep(0.8)
        