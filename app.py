# app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv
import boto3
from langchain_community.chat_models import BedrockChat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from auth import signup_user, login_user
from db import save_message, load_chat_history

# Load AWS credentials
load_dotenv()

# Claude via Bedrock
bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")
model = BedrockChat(
    client=bedrock_client,
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.7, "max_tokens": 1024}
)

# Chat prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a kind and empathetic therapist. Ask questions and help the user reflect. Refrain from diagnosing and just focus on supporting."),
    ("human", "{input}")
])
chain = prompt | model | StrOutputParser()

# Zen quote API
def get_zen_quote():
    try:
        r = requests.get("https://zenquotes.io/api/random")
        data = r.json()[0]
        return f"💬 *{data['q']}* — {data['a']}"
    except:
        return "💬 *Take a deep breath. You're here now.*"

# Summarization function
def summarize_chat(history, existing_summary=""):
    chat_text = "\n".join([f"{sender}: {msg}" for sender, msg in history])
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "You summarize therapist conversations to preserve key themes."),
        ("human", f"Here is the prior summary: {existing_summary}\n\nHere is the next section of the chat:\n{chat_text}\n\nPlease provide an updated, concise summary.")
    ])
    summary_chain = summary_prompt | model | StrOutputParser()
    return summary_chain.invoke({})

# Streamlit UI setup
st.set_page_config(page_title="Botline Bling", layout="centered")
st.title("Botline Bling 🪩🕺💃")
st.caption("This is a safe space. Take a moment for yourself. You're a real 6er. -Drake")

# Login / Signup UI
auth_mode = st.radio("Choose an option:", ["Login", "Sign Up"], horizontal=True)
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if auth_mode == "Sign Up":
    if st.button("Create Account"):
        success, msg = signup_user(username, password)
        if success:
            st.success(msg)
        else:
            st.error(msg)

if auth_mode == "Login":
    if st.button("Login"):
        if login_user(username, password):
            st.success(f"Welcome {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["history"] = load_chat_history(username)
            st.session_state["summarized_history"] = ""
        else:
            st.error("Invalid username or password")

# Main chat logic
if st.session_state.get("logged_in"):
    st.markdown("---")
    st.write("You can now talk to your 'Therapist'.")

    if "history" not in st.session_state:
        st.session_state["history"] = []
        st.session_state["summarized_history"] = ""
        quote = get_zen_quote()
        st.session_state["history"].append(("assistant", f"{quote}\n\nHow is it going?"))
        save_message(st.session_state["username"], "assistant", quote)

    user_input = st.chat_input("Talk to me...")

    # Summarize if conversation too long
    if len(st.session_state["history"]) > 20:
        old_history = st.session_state["history"][:-10]
        st.session_state["summarized_history"] = summarize_chat(
            old_history, st.session_state["summarized_history"]
        )
        st.session_state["history"] = st.session_state["history"][-10:]

    if user_input:
        st.session_state["history"].append(("user", user_input))
        save_message(st.session_state["username"], "user", user_input)

        recent_context = "\n".join([f"{s}: {m}" for s, m in st.session_state["history"]])
        full_input = f"Here’s what we’ve discussed so far: {st.session_state['summarized_history']}\n\n{recent_context}\n\nRespond to the user’s latest message."

        response = chain.invoke({"input": full_input})
        st.session_state["history"].append(("assistant", response))
        save_message(st.session_state["username"], "assistant", response)

    for sender, msg in st.session_state["history"]:
        with st.chat_message("user" if sender == "user" else "assistant"):
            st.markdown(msg)
