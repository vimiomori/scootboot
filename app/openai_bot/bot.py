import os
import openai

MODEL1 = "davinci:ft-personal-2022-12-11-09-16-26" # trained without delimiters
MODEL2 = "davinci:ft-personal-2022-12-11-08-21-53" # trained with delimiters

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

remove_list = ["\n\n###\n\n", "\r", "\t", "END OF LINE", "ENDING", "END"]

def get_response(prompt):
    response = openai.Completion.create(model=MODEL1, prompt=prompt, temperature=0.9, max_tokens=25)
    text = response["choices"][0]["text"]
    for remove in remove_list:
        text = text.replace(remove, "")

    text = text.split("\n")
    return [{"type": "text", "response": t} for t in text if t != ""]
