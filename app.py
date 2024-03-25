import streamlit as st

import streamlit as st
import uuid as uuid4
import random
from sqlalchemy import Column, Integer, String, PickleType

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    message = Column(PickleType, default=[])
    dicmd = Column(PickleType, default={})

# Create the table in the database
Base.metadata.create_all(engine)


d={}

st.title("Gemini")
sideb = st.sidebar
options = ["User", "AI"]
selected_option = sideb.radio("Message As:", options)
check1 = sideb.button("Delete")
if check1:
    d[f'Reset-{uuid4.uuid4()}']='Reset'

messages = [{"role": "user", "content": 'Hi', "id":None}, {"role": "assistant", "content": 'Hii,sujal', "id":'BAE5CC52E94351C2'}, {"role": "user", "content": 'halo', "id":None}, {"role": "assistant", "content": 'Hisujal', "id":None}]
# Display chat messages from history on app rerun
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if message["role"]=="assistant":
        if message["id"]!=None:
            if st.button(f'Del-{message["id"]}'):
                d[f'delete{message["id"]}']=message["id"]
                print(d)

if prompt := st.chat_input("What is up?"):
    if selected_option=="User":
        d[f'userprompt-{uuid4.uuid4()}']=prompt
        print(d)
    if selected_option=="AI":
        d[f'aiprompt-{uuid4.uuid4()}']=prompt
        print(d)
