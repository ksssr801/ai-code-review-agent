from app.config import Settings
from litellm import acompletion

DEFAULT_SYSTEM_PROMPT = """
You are a senior software engineer performing code reviews.

Your responsibilities:
- detect bugs
- identify security vulnerabilities
- suggest performance improvements
- improve readability and maintainability
- follow best engineering practices
"""

async def generate_response(
    user_prompt: str,
    settings: Settings,
    system_prompt: str | None = None,
    temperature: float = 0.2,
) -> str:
    system_msg = system_prompt or DEFAULT_SYSTEM_PROMPT
    response = await acompletion(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system_msg.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]
