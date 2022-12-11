import os
import openai

MODEL = "davinci:ft-personal-2022-12-11-08-21-53"

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

remove_list = ["\n\n###\n\n", "\r", "\t", "END"]

def get_response(prompt):
    response = openai.Completion.create(model=MODEL, prompt=prompt, temperature=0.9, max_tokens=25)
    text = response["choices"][0]["text"]
    for remove in remove_list:
        text = text.replace(remove, "")

    text = text.split("\n")
    return [{"type": "text", "response": t} for t in text if t != ""]
