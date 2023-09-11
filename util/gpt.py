import os

import openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def get_response_from_chatgpt(text_request, role: str) -> str:
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        stop=None,
        n=1,
        messages=[
        {
            'role': 'system',
            'content': f'You are {role}. Do not give dangerous information'
        },
        {
            'role': 'user',
            'content': text_request
        }]
    )
    return f"{response['choices'][0]['message']['content']}"


def count_words(text_propmpt: str) -> int:
    return len(text_propmpt.split())
