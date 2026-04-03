import streamlit as st
from Backend import build_chain

st.set_page_config(page_title="YouTube Chatbot", layout="centered")

st.title("🎥 YouTube Video Chatbot")
st.write("Ask questions from any YouTube video")

video_id = st.text_input("📌 Enter YouTube Video ID")

if "chain" not in st.session_state:
    st.session_state.chain = None

if st.button("Process Video"):
    if video_id:
        with st.spinner("Processing video transcript..."):
            try:
                st.session_state.chain = build_chain(video_id)
                st.success("Video processed successfully ✅")
            except Exception as e:
                st.error(str(e))
    else:
        st.warning("Please enter a video ID")

question = st.text_input("❓ Ask your question")

if st.button("Get Answer"):
    if st.session_state.chain and question:
        with st.spinner("Thinking..."):
            answer = st.session_state.chain.invoke(question)
        st.markdown("### 💬 Answer")
        st.write(answer)
    else:
        st.warning("Please process a video and ask a question first")
