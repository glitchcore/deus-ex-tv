import re

def parse_poem(content):
    poem = re.search(f"<poem>(.*?)</poem>", content, re.DOTALL)
    poem = poem.group(1)
    poem = poem.split("\n")
    poem = [re.sub("[^a-zA-Zа-яА-Яა-ჰ\s]+", "", x) for x in poem]
    poem = [x for x in poem if len(x) > 2]

    return poem


def ai_translate(ai, input, lang):
    system_prompt = [
        f'''
Translate poem to {lang}.
Keep number of lines and count of words in each line.
Start poem by tag <poem>.
End poem by tag </poem>
Do not send any explanation or description.
        '''
    ]

    system_prompt_messages = [{"role": "system", "content": p} for p in system_prompt]
    user_prompt_messages = [{"role": "user", "content": "\n".join(input)}]

    response = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=(user_prompt_messages + system_prompt_messages),
    )

    return parse_poem(response.choices[0].message.content)

def unsure_ai_poetry(ai, topics):
    system_prompt = [
        '''
Write a verse based on topic provided by the user.
The poem should be no more than six lines.
Start poem by tag <poem>.
End poem by tag </poem>
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

    en_poem = parse_poem(response_content)

    if len(en_poem) > 8 or len(en_poem) < 2:
        return None
    
    ru_poem = ai_translate(ai, en_poem, "russian")

    if len(ru_poem) != len(en_poem):
        return None
    
    ka_poem = ai_translate(ai, en_poem, "georgian")

    if len(ka_poem) != len(en_poem):
        return None
    
    return {
        "ru": ru_poem,
        "en": en_poem,
        "ka": ka_poem
    }

def ai_poetry(ai, topics):
    res = None
    while res is None:
        try:
            res = unsure_ai_poetry(ai, topics)
        except Exception:
            pass

    return res