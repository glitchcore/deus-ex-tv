import openai
from time import sleep
import os
import sqlite3

import configuration
from ai_poetry import ai_poetry
from ai_describer import ai_describe
from fate_gen import ai_answer
from glitch_ui import *

openai.api_key = configuration.api_key

TOPIC_LEN = 5

if __name__ == "__main__":
    conn = sqlite3.connect(configuration.db)

    topics = ["nothing"]

    while True:
        os.system('clear')
        print()
        user_input = input("  TYPE YOUR IDENTITY: ")

        # TODO: clear user input, remain [0-9a-Z\.\,\:\-]

        c = conn.cursor()
        c.execute('''INSERT INTO user_requests (request) VALUES (?)''', (user_input,))
        conn.commit()

        print("")

        print("  [WAIT FOR MACHINE...]", end='', flush=True)

        # TODO in case of timeout get answer from static list
        
        answer = ai_answer(openai, user_input)

        print("\r                          \r", end='', flush=True)
        slow_print(answer)
        print()
        print()

        '''topics += [ai_describe(openai, user_input)]
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
            '''

        blink_message("  [PRESS ENTER TO CONTINUE]", 0.4)

        random_chars(0.1, 1000)
        sleep(0.2)
        os.system('clear')
        sleep(0.8)
        