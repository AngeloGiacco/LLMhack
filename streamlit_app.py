import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os 
from tools import *
import json


api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = st.text_input("Enter your API key", type="password")
        api_key = st.session_state["api_key"]
    api_key = st.session_state["api_key"]

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
    st.session_state["system_prompt"] = "You are an expert in genomic medicine here to help me with my tasks in genetic variant analysis. You should help me to analyse the clinical significance of a variant. Please follow the standards set out in the Sue Richards et al 2015 paper and the framework adopted by the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. Please aim to stablish the variant's frequency in the population, determine the variant's impact on protein function and evaluate the variant's clinical significance. Make use of the tools available"

if st.session_state["system_prompt"] and not any(message.role == "system" for message in st.session_state.messages):
    st.session_state.messages.insert(0, ChatMessage(role="system", content=st.session_state["system_prompt"]))
    st.session_state.messages.insert(1, ChatMessage(role="assistant", content=first_prompt))

for message in st.session_state.messages:
    if message.role != 'system':  
        with st.chat_message(message.role):
            st.markdown(message.content) 

if prompt := st.chat_input("Explain genomic variant analysis task..."):
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    
    completion = client.chat(model=st.session_state.mistral_model, messages=st.session_state.messages, tools=tools_json, tool_choice="auto").choices[0]
    print(completion)
    st.session_state.messages.append(completion.message)
    if completion.message.tool_calls is not None and len(completion.message.tool_calls) > 0:  
        print("USE TOOLS")
        for tool in  completion.message.tool_calls:
            function_name = tool.function.name
            with st.chat_message("assistant"):
                st.write(f"Please wait, I'm using the tool {function_name[5:]} to find out more...")
            arguments = tool.function.arguments

            args_dict = json.loads(arguments)

            print(f"Calling {function_name} with {args_dict}")

            output = json.dumps(eval(function_name)(**args_dict))
            tool_message = ChatMessage(role="tool", function_name=function_name, content=output)
            print(f"received output from {function_name}: {output}")
            st.session_state.messages.append(tool_message)
        
        print("here")
        completion = client.chat(model=st.session_state.mistral_model, messages=st.session_state.messages, tools=tools_json, tool_choice="none").choices[0]
        st.session_state.messages.append(completion.message)
        chat_response = completion.message.content
        with st.chat_message("assistant"):
            st.write(chat_response)
    else:
        print("PRINT")
        chat_response = completion.message.content
        with st.chat_message("assistant"):
            st.write(chat_response)
        