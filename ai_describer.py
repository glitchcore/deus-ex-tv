def unsure_ai_describe(ai, text):
    system_prompt = [
        '''
Shorten the user's message.
Write no more than 5 words.
        '''
    ]

    system_prompt_messages = [{"role": "system", "content": p} for p in system_prompt]
    user_prompt_messages = [{"role": "user", "content": text}]

    response = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=(user_prompt_messages + system_prompt_messages)
    )

    return response.choices[0].message.content

def ai_describe(ai, text):
    res = ""
    while res == "" or len(res.split(" ")) > 5:
        res = unsure_ai_describe(ai, text)

    return res