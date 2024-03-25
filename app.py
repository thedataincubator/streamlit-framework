import streamlit as st
import uuid
import json
import os

# Path to the JSON file
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

st.title("Gemini")
sideb = st.sidebar
options = ["User", "AI"]
selected_option = sideb.radio("Message As:", options)
check1 = sideb.button("Delete")
st.success(messages)
if check1:
    dicmd[f'Reset-{uuid.uuid4()}'] = 'Reset'
    save_data(data)  # Save changes to JSON file
    st.rerun()  # Rerun the app to reflect changes

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if message["role"] == "assistant":
        if message["id"] != None:
            if st.button(f'Del-{message["id"]}'):
                dicmd[f'delete{message["id"]}'] = message["id"]
                save_data(data)  # Save changes to JSON file

if prompt := st.chat_input("What is up?"):
    if selected_option == "User":
        dicmd[f'userprompt-{uuid.uuid4()}'] = prompt
    elif selected_option == "AI":
        dicmd[f'aiprompt-{uuid.uuid4()}'] = prompt
    save_data(data)  # Save changes to JSON file
