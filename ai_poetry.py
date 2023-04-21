import json

def unsure_ai_poetry(ai, prev, next):
    system_prompt = [
        '''
        Write a verse on a topics provided by the user.
        ''',
        '''
        The poem should be no more than eight lines.
        Lines must be no more than three words.
        ''',
        '''
        Return ONLY json array of strings, contains poem lines.

        Do not send me nothing except json, your answer must be valid json!
        Do not send any explanation or description.
        '''
    ]

    system_prompt_messages = [{"role": "system", "content": p} for p in system_prompt]
    user_prompt_messages = [{"role": "user", "content": ". ".join([prev, next])}]

    print("user prompt:", user_prompt_messages)

    response = ai.ChatCompletion.create(
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

def ai_poetry(ai, prev, next=""):
    res = []
    while res == []:
        res = unsure_ai_poetry(ai, prev, next)
    
    # TODO: remove empty lines
    # TODO: remove all except [a-Z]

    return res