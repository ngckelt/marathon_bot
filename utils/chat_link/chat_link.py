import json


def update_chat_link(chat_link: str):
    with open('utils/chat_link/chat_link.json', 'w') as f:
        data = {'chat_link': chat_link}
        f.write(json.dumps(data))


def get_chat_link():
    with open('utils/chat_link/chat_link.json') as f:
        data = json.loads(f.read())
        return data.get("chat_link")

