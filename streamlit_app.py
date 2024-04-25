import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os 

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = st.text_input("Enter your API key", type="password")
        api_key = st.session_state["api_key"]
    api_key = st.session_state["api_key"]

print("API KEY")
print(api_key)
client = MistralClient(api_key=api_key)

# Initialize the model in session state if it's not already set
if "mistral_model" not in st.session_state:
    st.session_state["mistral_model"] = "mistral-large-latest"

model_options = ('mistral-small-latest', 'mistral-medium-latest', 'mistral-large-latest')
st.session_state["mistral_model"] = st.selectbox('Select a model', model_options, index=model_options.index(st.session_state["mistral_model"]), key="model_select")

st.title("Genetic Variant Analysis Bot")

def response_generator():
    chat_response = client.chat(
        model=st.session_state.mistral_model,
        messages=st.session_state.messages,
    )

    return chat_response.choices[0].message.content

first_prompt = "Hello 👋. I'm your personal assistant for genetic variant analysis. I have access to all the tools listed in the widely accepted framework from Richards et al 2015. Please explain the task you would like me to help with:"

if "messages" not in st.session_state:
    st.session_state.messages = []

if not "system_prompt" in st.session_state:
    st.session_state["system_prompt"] = "You are an expert in genomic medicine here to help me with my tasks in genetic variant analysis. "

if st.session_state["system_prompt"] and not any(message.role == "system" for message in st.session_state.messages):
    st.session_state.messages.insert(0, ChatMessage(role="system", content=st.session_state["system_prompt"]))
    st.session_state.messages.insert(1, ChatMessage(role="assistant", content=first_prompt))

for message in st.session_state.messages:
    if message.role != 'system':  
        with st.chat_message(message.role):
            st.markdown(message.content) 

if prompt := st.chat_input("Explain task..."):
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat_stream(model=st.session_state.mistral_model, messages=st.session_state.messages):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "|")
        
        message_placeholder.markdown(full_response)
        st.session_state.messages.append(ChatMessage(role="assistant", content=full_response))