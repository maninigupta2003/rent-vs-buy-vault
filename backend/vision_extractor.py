# GPT-4o Vision processing logic
import base64
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_financials(file_bytes: bytes):
    encoded = base64.b64encode(file_bytes).decode()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract numeric financial data ONLY. "
                    "Return valid JSON with salary numbers. "
                    "Ignore names, IBANs, addresses."
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract salary information"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}
                ]
            }
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content
