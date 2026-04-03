from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq( model="openai/gpt-oss-20b")
import streamlit as st
st.title("🤖 Ask Buddy AI QnA Bot")
st.markdown("My QnA Bot with langchain and Hugging face model !")

if "messages" not in st.session_state:
    st.session_state.messages = []      # if a history list is not already exist then make a history list messages.

for message in st.session_state.messages:
    role = message['role']
    content = message['content']
    st.chat_message(role).markdown(content)

query = st.chat_input("Ask anything ?")

if query:
    st.session_state.messages.append({"role":'user',"content":query}) # chat history list me dictionary pass kr rhe hai.
    st.chat_message("user").markdown(query)
    res = llm.invoke(query)
    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append({"role":'ai',"content":res.content})