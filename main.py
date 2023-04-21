import json
import openai

import configuration

openai.api_key = configuration.api_key

def unsure_make_gpt_poetry(prev, next):
    system_prompt = [
        '''
        Write a verse on a topic provided by the user.
        User send you two topics as JSON array contains two strings. Strings can be empty.
        If exists, second topic is more significant than first.
        ''',
        "The poem should be no more than eight lines",
        '''
        Return ONLY json array of strings, contains poem lines.

        Do not send me nothing except json, your answer must be valid json!
        Do not send any explanation or description.
        '''
    ]

    system_prompt_messages = [{"role": "system", "content": p} for p in system_prompt]
    user_prompt_messages = [{"role": "user", "content": json.dumps([prev, next])}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=(user_prompt_messages + system_prompt_messages)
    )

    response_content = response.choices[0].message.content
    
    try:
        res = json.loads(response_content)
        return res
    except json.decoder.JSONDecodeError:
        print("raw answer:", response_content)
        return []

def make_gpt_poetry(prev, next=""):
    res = []
    while res == []:
        res = unsure_make_gpt_poetry(prev, next)
    
    return res

if __name__ == "__main__":
    poetry = make_gpt_poetry("void")

    for line in poetry:
        print(line)