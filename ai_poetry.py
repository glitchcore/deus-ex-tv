import re

def unsure_ai_poetry(ai, topics):
    system_prompt = [
        '''
Write a verse based on topic provided by the user.
The poem should be no more than eight lines.
Write poem in english, russian, and georgian.
Start poem in russian by tag <ru>
End poem in russian by tag </ru>
Start poem in english by tag <en>
End poem in english by tag </en>
Start poem in georgian by tag <ka>
End poem in geirgian by tag </ka>
Do not send any explanation or description.
        '''
    ]

    system_prompt_messages = [{"role": "system", "content": p} for p in system_prompt]
    user_prompt_messages = [{"role": "user", "content": ". ".join(topics)}]

    print("user prompt:", user_prompt_messages)

    response = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=(user_prompt_messages + system_prompt_messages),
        temperature=1
    )

    response_content = response.choices[0].message.content

    def content_to_poem(content, lang):
        poem = re.search(f"<{lang}>(.*?)</{lang}>", content, re.DOTALL)
        poem = poem.group(1)
        poem = poem.split("\n")
        poem = [re.sub("[^a-zA-Zа-яА-Яა-ჰ\s]+", "", x) for x in poem]
        poem = [x for x in poem if len(x) > 2]

        return poem
    
    try:
        res = {
            "ru": content_to_poem(response_content, "ru"),
            "en": content_to_poem(response_content, "en"),
            "ka": content_to_poem(response_content, "ka"),
        }

        if len(res["ru"]) != len(res["en"]) or len(res["ru"]) != len(res["ka"]):
            return None
        
        return res
    except Exception:
        return None

def ai_poetry(ai, topics):
    res = None
    while res is None:
        res = unsure_ai_poetry(ai, topics)
    
    # TODO: remove all except [a-Z]

    return res