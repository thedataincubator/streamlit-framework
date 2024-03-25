import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai
from datetime import datetime
from json import dumps
from whatsapp_api_client_python import API
import os
import re
import asyncio
import time
from whatsapp_api_client_python import API

greenAPI = API.GreenAPI(
    "7103919868", "7f12e02c4c9b4b56b16a50efdb3d417cb4453b69d5314553ad"
)
GOOGLE_API_KEY=os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

# Create an instance of the generative AI model and start a chat session
model = genai.GenerativeModel('gemini-pro')
if 'chat' not in st.session_state:
    st.session_state['chat'] = model.start_chat(history=[])

def ai_chat(data):
    response = st.session_state['chat'].send_message(data)
    return {'role': 'assistant', 'content':response.text}
def ai(data):
    response = st.session_state['chat'].send_message(data)
    st.session_state.messages.append({"role": "assistant", "content":(response.text)})
    r = greenAPI.sending.sendMessage("919549047575@c.us", (response.text))
    with st.chat_message("assistant"):
        st.markdown(response.text)
    if st.button('Delete'):
        st.success(r.data)

import streamlit as st
st.title("Gemini")
sideb = st.sidebar
options = ["User", "AI"]
selected_option = sideb.radio("Message As:", options)
check1 = sideb.button("Delete")
if check1:
    st.session_state.messages = []
    chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    if selected_option=="User":
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        k=ai_chat(data=prompt)
        response=k['content']
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append(k)
    if selected_option=="AI":
        r = greenAPI.sending.sendMessage("919549047575@c.us", (prompt))
        st.session_state.messages.append({"role": "assistant", "content":(prompt)})
        with st.chat_message("assistant"):
            st.markdown(prompt)

if 'inital' not in st.session_state:
        st.session_state['inital']=ai_chat(data="Hi Gemini, this is Sujal. I've successfully integrated your API with the WhatsApp API, which means you're now part of a WhatsApp group where you can chat and interact with people. Your role is to engage in conversations as if we're all chatting together in a friendly, casual manner. Remember to keep your responses relevant, respectful, and helpful, just like you would in a normal chat with friends. Let's have some great conversations!")
        response=st.session_state['inital']['content']
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append(st.session_state['inital'])

from datetime import datetime
from json import dumps

async def main():
    greenAPI.webhooks.startReceivingNotifications(handler)

def handler(type_webhook: str, body: dict) -> None:
    if type_webhook == "incomingMessageReceived":
        incoming_message_received(body)

def incoming_message_received(body: dict) -> None:
    data = dumps(body, ensure_ascii=False, indent=4)
    x = re.search(r'"textMessage":.*"', data)
    message=(x.group().split(':')[1][2:(len(x.group().split(':')[1])-1)])
    with st.chat_message("user"):
        st.markdown(message)
    st.session_state.messages.append({"role": "assistant", "content":(message)})
    ai(data=message)

asyncio.run(main())
