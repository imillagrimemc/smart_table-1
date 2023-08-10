import openai

openai.api_key = "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"


def gpt_function(query):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"paraphrase it from 3rd party in past simple. Do it from third party. Instead of i, you, we, you, they use Billy  <{query}>",
            }
        ],
    )
    chat_response = completion.choices[0].message.content
    print(f"ChatGPT: {chat_response}")
    return f"{chat_response}"


# print(gpt_function(query = "I'm going to Tashkent now"))


def gpt_answer(query: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
    )
    chat_response = completion.choices[0].message.content
    print(f"ChatGPT answer: {chat_response}")
    return f"{chat_response}"


# print(gpt_answer(query="How many states in the USA?"))
