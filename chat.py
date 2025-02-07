#!/usr/bin/python

from sys import argv
system = ' '.join(argv[1:])
print(f"System prompt is \"{system}\"\n")
from openai import OpenAI
client = OpenAI(
    base_url= "http://172.31.4.136:8000/v1",
    api_key = "sk-no-key-required"
)
print(client.models.list())
prompt = ""
while True:
    user = input("\n>>> ")
    if user == "exit":
        exit()
    if user == "prompt":
        print("====================================")
        print(prompt)
        print("====================================")
        continue
    prompt = f"{prompt}\nUser: \"{user}\""
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        max_tokens=4000,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content
    print(response)
    prompt = prompt + "\n\nMe: " + response.replace('\n', ' ') + '\n'

    '''
    curl -s http://172.31.4.136:8000/v1/chat/completions -H 'Content-Type: application/json' -d '{
      "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
      "messages": [{"role": "user", "content": "Explain how test doubles work with pytest"}]
    }' | jq
    '''
