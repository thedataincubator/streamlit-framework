import streamlit as st
import pathlib
import textwrap
import os
import google.generativeai as genai
GOOGLE_API_KEY=os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

# Create an instance of the generative AI model and start a chat session
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def ai_chat(data):
    response = chat.send_message(data)
    return {'role': 'assistant', 'content':response.text}
st.title("Gemini")
sideb = st.sidebar
check1 = sideb.button("Delete")
if check1:
    st.session_state.messages = []
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    st.success(str(message))
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
    # Add assistant response to chat history
    st.session_state.messages.append(k)
