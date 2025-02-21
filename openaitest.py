import openai
from config import apikey

openai.api_key = apikey

print(f"API Key : {openai.api_key}")

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",  # Or gpt-4 if you have access
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},  # Optional system message
        {"role": "user", "content": "Hello"}  # Your prompt
    ]
)

print(response.choices[0].message.content) # Extract and print the generated text