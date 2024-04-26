import json
import requests
import os


if not os.path.exists("chats"):
    os.makedirs("chats")

counter = 0
while os.path.exists(f"chats/chat_{counter}.md"):
    counter += 1

prompt_number = 0
while True:

    prompt = input(">>> ")
    if prompt == "/bye":
        break
    prompt_number += 1

    with open(f"chats/chat_{counter}.md", "a") as f:
        f.write("### Prompt\n")
        f.write(prompt + "\n\n")

    if prompt_number == 1:
        os.system(f"code chats/chat_{counter}.md")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt},
        stream=True,
    )

    with open(f"chats/chat_{counter}.md", "a") as f:
        f.write("### Response\n")

    for line in response.iter_lines():
        if line:
            json_line = json.loads(line.decode())
            with open(f"chats/chat_{counter}.md", "a") as f:
                f.write(json_line["response"])

    with open(f"chats/chat_{counter}.md", "a") as f:
        f.write("\n\n")
