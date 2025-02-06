from openai import OpenAI
from sys import argv

if len(argv) < 3:
    print("Usage: `python script.py base_url api_key`")
    exit()

client = OpenAI(
    base_url = argv[1],
    api_key = argv[2],
)
print(client.models.list())
