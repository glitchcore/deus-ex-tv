import re

def unsure_ai_poetry(ai, topics):
    system_prompt = [
        '''
Write a verse based on topic provided by the user.
The poem should be no more than eight lines.
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

    poem = re.search('<poem>(.*?)</poem>', response_content, re.DOTALL)
    poem = poem.group(1)
    poem = poem.split("\n")
    poem = [x for x in poem if len(x) > 2]
    
    return poem

def ai_poetry(ai, topics):
    res = []
    while res == [] or type(res) != list:
        res = unsure_ai_poetry(ai, topics)
    
    # TODO: remove empty lines
    # TODO: remove all except [a-Z]

    return res