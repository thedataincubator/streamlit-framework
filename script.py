from whatsapp_api_client_python import API
from json import dumps
import re
import json
import os
import google.generativeai as genai
import boto3
import threading
import time
from botocore.exceptions import ClientError

# Fetch AWS credentials from environment variables
aws_access_key_id = os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY')
bucket_name = os.environ.get('BUCKETEER_BUCKET_NAME')
s3_file_key = 'variables.json'

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Create an S3 client using the session
s3 = session.client('s3')

def load_data():
    try:
        response = s3.get_object(Bucket=bucket_name, Key=s3_file_key)
        data = response['Body'].read()
        return json.loads(data)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return {"messages": [], "dicmd": {}}
        else:
            # Other errors: raise them
            raise

def save_data(data):
    s3.put_object(Bucket=bucket_name, Key=s3_file_key, Body=json.dumps(data))

# Example usage
disk = load_data()
messages = disk.get("messages")
dicmd = disk.get("dicmd")

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
    messages.append({"role": "assistant", "content":(response.text), "id":None})
    disk["messages"] = messages
    save_data(data=disk)

def ai(data):
    response =chat.send_message(data)
    r = greenAPI.sending.sendMessage("919549047575@c.us", (response.text))
    messages.append({"role": "assistant", "content":(response.text), "id":r.data['idMessage']})
    disk["messages"] = messages
    save_data(data=disk)

def sendo(message):
    r = greenAPI.sending.sendMessage("919549047575@c.us", message)
    messages.append({"role": "assistant", "content":message, "id":r.data['idMessage']})
    disk["messages"] = messages
    save_data(data=disk)

def delid(id):
    try:
        response = greenAPI.serviceMethods.deleteMessage(chatId="919549047575@c.us", idMessage=id)
        response.data = json.loads(response.text)
    except Exception as e:
        print("deleted successfully")

def checkforthing():
    if dicmd!={}:
        for k in d.keys():
            if k[0:6]=='delete':
                delid(id=dicmd[k])
            if k[0:10]=='userprompt':
                ai_chat(data=dicmd[k])
            if k[0:8]=='aiprompt':
                sendo(message=dicmd[k])
        disk["dicmd"]={}
        save_data(data=disk)
    

def periodic_task():
    while True:
        checkforthing()
        time.sleep(5)

def main():
    threading.Thread(target=periodic_task, daemon=True).start()
    greenAPI.webhooks.startReceivingNotifications(handler)

def handler(type_webhook: str, body: dict) -> None:
    if type_webhook == "incomingMessageReceived":
        incoming_message_received(body)

def incoming_message_received(body: dict) -> None:
    data = dumps(body, ensure_ascii=False, indent=4)
    x = re.search(r'"textMessage":.*"', data)
    message=(x.group().split(':')[1][2:(len(x.group().split(':')[1])-1)])
    messages.append({"role": "user", "content":message})
    disk["messages"] = messages
    save_data(data=disk)
    ai(data=message)
    print(message)

if __name__ == '__main__':
    main()
