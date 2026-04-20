from dotenv import load_dotenv
import os
import asyncio

from openai import OpenAI, AsyncOpenAI
from openai._exceptions import BadRequestError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    response = client.responses.create(
        model=model,
        temperature=temperature,
        max_output_tokens=max_new_tokens,
        input=message
    )

    return response.output_text