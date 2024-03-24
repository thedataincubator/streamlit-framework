import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai
from datetime import datetime
from json import dumps
from whatsapp_api_client_python import API
import os
import re
import threading
GOOGLE_API_KEY=os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

# Create an instance of the generative AI model and start a chat session
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def ai_chat(data):
    response = chat.send_message(data)
    return {'role': 'assistant', 'content':response.text}
def ai(data):
    response = chat.send_message(data)
    response = greenAPI.sending.sendMessage("919549047575@c.us", (response.text))
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response.text})

greenAPI = API.GreenAPI(
    "7103919868", "7f12e02c4c9b4b56b16a50efdb3d417cb4453b69d5314553ad"
)
def main():
    ai_chat(data="Hi Gemini, I've integrated your API with the WhatsApp API, and you're now connected to a WhatsApp group. You have the capability to interact with the group members by sending and receiving messages. Feel free to engage in conversations and provide assistance as needed. Enjoy your new environment and happy chatting!. Make sure to be short like we do in chatting")
    greenAPI.webhooks.startReceivingNotifications(handler)


def handler(type_webhook: str, body: dict) -> None:
    if type_webhook == "incomingMessageReceived":
        incoming_message_received(body)


def incoming_message_received(body: dict) -> None:
    data = dumps(body, ensure_ascii=False, indent=4)
    x = re.search(r'"textMessage":.*"', data)
    message=(x.group().split(':')[1][2:(len(x.group().split(':')[1])-1)])
    if message:
        with st.chat_message("user"):
                    st.markdown(message)
        st.session_state.messages.append({"role": "user", "content": message})
        ai(data=f'New message recieved from Sujal: {message}')

listener_thread = threading.Thread(target=main, daemon=True)
listener_thread.start()

import streamlit as st

st.title("Gemini")
sideb = st.sidebar
check1 = sideb.button("Delete")
if check1:
    st.session_state.messages = []
    chat = model.start_chat(history=[])
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    k=ai_chat(data=prompt)
    response=k['content']
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append(k)
listener_thread = threading.Thread(target=main, daemon=True)
listener_thread.start()
