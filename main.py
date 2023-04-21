import openai

import configuration
from make_poetry import make_gpt_poetry

openai.api_key = configuration.api_key

if __name__ == "__main__":
    poetry = make_gpt_poetry(openai, "void")

    for line in poetry:
        print(line)