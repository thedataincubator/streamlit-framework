from whatsapp_api_client_python import API
from json import dumps
import re
import json
import os
import google.generativeai as genai
json_file_path = '/tmp/variables.json'

# Function to load data from JSON file
def load_data():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    else:
        return {"messages": [], "dicmd": {}}

# Function to save data to JSON file
def save_data(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file)

# Load existing data
data = load_data()
messages = data.get("messages", [])
dicmd = data.get("dicmd", {})

greenAPI = API.GreenAPI(
    "7103919868", "7f12e02c4c9b4b56b16a50efdb3d417cb4453b69d5314553ad"
)

GOOGLE_API_KEY=os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

# Create an instance of the generative AI model and start a chat session
model = genai.GenerativeModel('gemini-pro')
chat= model.start_chat(history=[])

def ai_chat(data):
    response =chat.send_message(data)
    return {'role': 'assistant', 'content':response.text}
def ai(data):
    response =chat.send_message(data)
    r = greenAPI.sending.sendMessage("919549047575@c.us", (response.text))
    messages.append({"role": "assistant", "content":(response.text)})
    save_data(data)

def main():
  greenAPI.webhooks.startReceivingNotifications(handler)


def handler(type_webhook: str, body: dict) -> None:
    if type_webhook == "incomingMessageReceived":
        incoming_message_received(body)

def incoming_message_received(body: dict) -> None:
    data = dumps(body, ensure_ascii=False, indent=4)
    x = re.search(r'"textMessage":.*"', data)
    message=(x.group().split(':')[1][2:(len(x.group().split(':')[1])-1)])
    messages.append({"role": "user", "content":message})
    ai(data=message)
    print(message)

if __name__ == '__main__':
    main()
