import openai

import configuration
from make_poetry import ai_poetry

openai.api_key = configuration.api_key

if __name__ == "__main__":
    poetry = ai_poetry(openai, "void")

    for line in poetry:
        print(line)