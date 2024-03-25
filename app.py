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
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# Initialize the base class for declarative class definitions
Base = declarative_base()
class Data(Base):
    __tablename__ = 'data'  # Name of the table in the database
    id = Column(Integer, primary_key=True)  # Primary key column
    message = Column(PickleType)  # Column to store a pickled list
    dicmd = Column(PickleType)

session = SessionLocal()
record = session.query(Data).first()
if record:
    dicmd = record.dicmd
    messages=record.message
st.success(dicmd)
st.success(messages)
st.title("Gemini")
sideb = st.sidebar
options = ["User", "AI"]
selected_option = sideb.radio("Message As:", options)
check1 = sideb.button("Delete")
if check1:
    dicmd[f'Reset-{uuid4.uuid4()}']='Reset'
    session.commit()

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if message["role"]=="assistant":
        if message["id"]!=None:
            if st.button(f'Del-{message["id"]}'):
                dicmd[f'delete{message["id"]}']=message["id"]
                print(dicmd)

if prompt := st.chat_input("What is up?"):
    if selected_option=="User":
        dicmd[f'userprompt-{uuid4.uuid4()}']=prompt
        print(dicmd)
    if selected_option=="AI":
        dicmd[f'aiprompt-{uuid4.uuid4()}']=prompt
        print(dicmd)
