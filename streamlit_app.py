import streamlit as st
import random
import time
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os 

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

st.title("Genetic Variant Analysis Bot")

with st.chat_message("user"):
    st.write("Hello 👋. I'm your personal assistant for genetic variant analysis. I have access to all the tools listed in the widely accepted framework from Richards et al 2015. Please explain the task you would like me to help with:")

def response_generator():
    response = "hi what can i do?"
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Explain task..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    st.session_state.messages.append({"role": "assistant", "content": response})