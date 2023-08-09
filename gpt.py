import openai

openai.api_key = "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"


def gpt_function(query="I'm going to Tashkent now"):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": f"paraphrase it from 3rd party in past simple. Do it from third party. Instead of i, you, we, you, they use Billy  <{query}>"}
        ]
    )
    chat_response = completion.choices[0].message.content
    print(f'ChatGPT: {chat_response}')
    return f"{chat_response}"

