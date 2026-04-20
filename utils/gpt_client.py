from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()

client = None


def get_client():
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set."
            )
        client = OpenAI(api_key=api_key)
    return client

def create_message(sys_prompt: str, usr_prompt: str):
    return [
        {'role': 'system', 'content': sys_prompt},
        {'role': 'user', 'content': usr_prompt}
    ]
    
def gpt_call(
    user_prompt: str,
    system_prompt: str,
    model: str,
    max_new_tokens: int,
    temperature: float,
):
    message = create_message(system_prompt, user_prompt)
    response = get_client().responses.create(
        model=model,
        temperature=temperature,
        max_output_tokens=max_new_tokens,
        input=message
    )

    return response.output_text
