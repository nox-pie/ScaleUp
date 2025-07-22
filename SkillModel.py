import google.generativeai as genai
from PromptBuilder import build_prompt
import json

def get_model_response(messages, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    chat = model.start_chat()

    # Always prepend system prompt
    system_prompt = build_prompt()
    chat_input = [system_prompt] + [msg["content"] for msg in messages]

    response = chat.send_message(chat_input)
    return response.text
