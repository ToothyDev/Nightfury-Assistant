from discord import Color
from discord import OptionChoice
from openai import AsyncOpenAI

import config


class Colors:
    tailfin = 0xB62724

    color_options = [
        OptionChoice(name="Red", value=Color.red().value),
        OptionChoice(name="Green", value=Color.green().value),
        OptionChoice(name="Blue", value=Color.blue().value),
        OptionChoice(name="Yellow", value=Color.yellow().value),
        OptionChoice(name="Purple", value=Color.purple().value),
        OptionChoice(name="Orange", value=Color.orange().value),
        OptionChoice(name="Gray", value=Color.dark_gray().value),
        OptionChoice(name="Pink", value=Color.nitro_pink().value),
        OptionChoice(name="Random", value=Color.random().value)
    ]


async def send_to_ai(prompt: str) -> str:
    sys_prompt = """
    You are a helper AI in Discord. Your job is to respond to the given prompt, usually a question, concisely.
    Ideally you should respond in a single sentence, unless the question is more complex.
    """
    client = AsyncOpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)
    chat_completion = await client.chat.completions.create(messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": prompt}
    ],
        model=config.llm_model_name)
    return chat_completion.choices[0].message.content
