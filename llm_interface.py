import os
import time
import backoff
from openai import OpenAI, RateLimitError
from config import API_RATE_LIMIT_PER_MINUTE, OPENAI_API_KEY_ENV, OPENAI_BASE_URL, MODEL_NAME

OPENAI_API_KEY = os.getenv(OPENAI_API_KEY_ENV)
MIN_DELAY_SECONDS = 60 / API_RATE_LIMIT_PER_MINUTE
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

@backoff.on_exception(
    backoff.expo,
    RateLimitError,
    max_tries=10,
    max_time=180,
    factor=3,
    base=10,
    jitter=backoff.full_jitter
)
def ask_llm(prompt):
    time.sleep(MIN_DELAY_SECONDS)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt 
            }
        ]
    )
    return response.choices[0].message
