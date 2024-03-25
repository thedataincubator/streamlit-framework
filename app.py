import streamlit as st

import streamlit as st
import uuid as uuid4
import random
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, PickleType
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database setup
DATABASE_URL = os.environ.get('DATABASE_URL')  # Replace with your actual database URL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the base class for declarative class definitions
Base = declarative_base()

session = SessionLocal()
class Data(Base):
    __tablename__ = 'data'  # Name of the table in the database
    id = Column(Integer, primary_key=True)  # Primary key column
    message = Column(PickleType)  # Column to store a pickled list
    dicmd = Column(PickleType)  # Column to store a pickled dictionary
# Create an instance of the Data class
record = session.query(Data).first()
if record:
    # Import the dicmd dictionary
    dicmd = record.dicmd
    record.message.extend([{"role": "user", "content": 'Hi', "id":None}, {"role": "assistant", "content": 'Hii,sujal', "id":'BAE5CC52E94351C2'}, {"role": "user", "content": 'halo', "id":None}, {"role": "assistant", "content": 'Hisujal', "id":None}])
    session.commit()
    messages=record.message
    if dicmd is None:
        dicmd_dict = {}
    if messages is None:
        messages=[]
print(dicmd, messages)
d={}

st.title("Gemini")
sideb = st.sidebar
options = ["User", "AI"]
selected_option = sideb.radio("Message As:", options)
check1 = sideb.button("Delete")
if check1:
    d[f'Reset-{uuid4.uuid4()}']='Reset'

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
