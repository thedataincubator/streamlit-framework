import streamlit as st
import uuid
import json
import os
import boto3
import json
import os
from botocore.exceptions import ClientError

# Fetch AWS credentials from environment variables
aws_access_key_id = os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY')

# Initialize a boto3 client with the credentials from environment variables
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

bucket_name = os.environ.get('BUCKETEER_BUCKET_NAME')
s3_file_key = 'variables.json'

def load_data():
    """Load data from an S3 bucket."""
    try:
        response = s3.get_object(Bucket=bucket_name, Key=s3_file_key)
        data = response['Body'].read()
        return json.loads(data)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            st.error('file not found')
            return {"messages": [], "dicmd": {}}
        else:
            # Other errors: raise them
            raise

def save_data(data):
    """Save data to an S3 bucket."""
    print(data)
    s3.put_object(Bucket=bucket_name, Key=s3_file_key, Body=json.dumps(data))

# Example usage
disk = load_data()
print(disk)
messages = disk.get("messages", [])
dicmd = disk.get("dicmd", {})

st.title("Gemini")
sideb = st.sidebar
options = ["User", "AI"]
selected_option = sideb.radio("Message As:", options)
check1 = sideb.button("Delete")
st.success(messages)
if check1:
    dicmd[f'Reset-{uuid.uuid4()}'] = 'Reset'
    save_data(data=disk)  # Save changes to JSON file
    st.rerun()  # Rerun the app to reflect changes

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if message["role"] == "assistant":
        if message["id"] != None:
            if st.button(f'Del-{message["id"]}'):
                dicmd[f'delete{message["id"]}'] = message["id"]
                save_data(data=disk)  # Save changes to JSON file

if prompt := st.chat_input("What is up?"):
    if selected_option == "User":
        dicmd[f'userprompt-{uuid.uuid4()}'] = prompt
    elif selected_option == "AI":
        dicmd[f'aiprompt-{uuid.uuid4()}'] = prompt
    save_data(data=disk)  # Save changes to JSON file
