import streamlit as st
import random
import time
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os 

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = st.text_input("Enter your API key", type="password")
    api_key = st.session_state["api_key"]
else:
    if expected_password := os.getenv("PASSWORD"):
        password = st.text_input("What's the secret password?", type="password")
        # Check if the entered key matches the expected password
        if password != expected_password:
            api_key = ''
            st.error("Unauthorized access.")
            reset_state()  # This line will reset the script
        else:
            api_key = os.getenv("MISTRAL_API_KEY")


client = MistralClient(api_key=api_key)

# Initialize the model in session state if it's not already set
if "mistral_model" not in st.session_state:
    st.session_state["mistral_model"] = "mistral-large-latest"

model_options = ('mistral-small-latest', 'mistral-medium-latest', 'mistral-large-latest')
st.session_state["mistral_model"] = st.selectbox('Select a model', model_options, index=model_options.index(st.session_state["mistral_model"]), key="model_select")

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

if st.session_state["system_prompt"] and not any(message.role == "system" for message in st.session_state.messages):
    st.session_state.messages.insert(0, ChatMessage(role="system", content=st.session_state["system_prompt"]))

for message in st.session_state.messages:
    if message.role != "system":  
        with st.chat_message(message.role):
            st.markdown(message.content) 

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