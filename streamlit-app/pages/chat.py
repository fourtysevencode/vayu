import streamlit as st
import requests

st.title("🔰Chat with Vayu - Your AI Climate Advisor!")
st.set_page_config(page_title="Vayu Chat", page_icon="🔰")

if "messages" not in st.session_state: # so it doesnt forget the messages every rerun, st.session_state is a dict with all persistent variables over the session. (Runs on session start)
    st.session_state.messages = [] # list of messages, st.session_state.messages creates a key 'messages' and its value is initially an empty list where the chat history will be appended.

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"]) # user / assistant chat bubble creation on every rerun

if prompt := st.chat_input("Ask Vayu..."): # := walrus operator, assigns value & checks if None - Only runs if theres input
    st.session_state.messages.append({"role": "user", "content": prompt}) # saves to memory
    st.chat_message("user").write(prompt)  # render it right now before generating message

    with st.spinner("Vayu is thinking..."): # loading spinner
        res = requests.post("http://localhost:8000/chat", json={"message": prompt}) # API POST request from local host server, converts dict of prompt to JSON with the parameter 'json' and sets content type header (applications/json)
        reply = res.json()["response"] # converts json reply to python dict with .json() and extracts the response string

    st.session_state.messages.append({"role": "assistant", "content": reply}) # save reply to memory
    st.rerun() # shows the reply on rerun