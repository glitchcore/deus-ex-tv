def unsure_ai_describe(ai, poetry_array):
    system_prompt = [
        '''
        Shorten the user's message.
        Write no more than 5 words.
        '''
    ]

    system_prompt_messages = [{"role": "system", "content": p} for p in system_prompt]
    user_prompt_messages = [{"role": "user", "content": " ".join(poetry_array)}]

    response = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=(user_prompt_messages + system_prompt_messages)
    )

    return response.choices[0].message.content

def ai_describe(ai, poetry_array):
    res = ""
    while res == "" or len(res.split(" ")) > 3:
        res = unsure_ai_describe(ai, poetry_array)

    return res