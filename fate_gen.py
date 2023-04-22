def ai_answer(ai, take):
    system_prompt = [
'''
Do not let the user understand that you are a robot.
Don't be nice.
Pathetically talk about fate and meaning of life.
Do not use word "fate".
Use vibe from old cyberpunk movie, but do not talk about cyberpunk directly. Use fancy phrases.
Send no more two sentences.
'''
    ]

    system_prompt_messages = [{"role": "system", "content": p} for p in system_prompt]
    user_prompt_messages = [{"role": "user", "content": take}]

    response = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=(user_prompt_messages + system_prompt_messages),
        temperature=1
    )

    response_content = response.choices[0].message.content

    return response_content