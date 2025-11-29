import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = input("Please enter your Gemini API Key: ")

genai.configure(api_key=api_key)

print("\n--- Listing Available Gemini Models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}, Supported methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")
print("---------------------------------------")
