# LLM orchestration + conversation logic
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_persuasive_response(financial_summary: dict, convinced=False):
    system_prompt = (
        "You are a calm financial advisor. "
        "Use numbers to persuade. Do not hallucinate."
    )

    user_prompt = f"""
    Financial Facts:
    {financial_summary}

    If the user seems convinced, move toward pre-approval.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    message = response.choices[0].message.content

    if convinced:
        message += (
            "\n\nBased on your income, you are pre-qualified. "
            "Would you like me to generate your pre-approval certificate?"
        )

    return message
