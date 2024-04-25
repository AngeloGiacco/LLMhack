import streamlit as st
import random

st.title("Genetic Variant Analysis Bot")

with st.chat_message("user"):
    st.write("Hello 👋. I'm your personal assistant for genetic variant analysis. I have access to all the tools listed in the widely accepted framework from Richards et al 2015. Please explain the task you would like me to help with:")

def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
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