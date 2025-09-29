import google.generativeai as genai
from PromptBuilder import build_prompt

def get_model_response(messages, api_key):
    """
    Sends a list of chat messages to Gemini model and returns the assistant's reply.
    Includes a structured system prompt at the beginning for consistent behavior.
    """
    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")
        chat = model.start_chat()

        # Always prepend system prompt
        system_prompt = build_prompt()
        chat_input = [system_prompt] + [msg["content"] for msg in messages]

        response = chat.send_message(chat_input)
        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"

