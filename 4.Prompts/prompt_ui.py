from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st;
from langchain_core.prompts import PromptTemplate,load_prompt
load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id = "zai-org/GLM-4.7",
    task = "text-generation"
)
ddp = HuggingFaceEndpoint(
    repo_id = "deepseek-ai/DeepSeek-V3.2",
    task = "text-generation"
)
model = ChatHuggingFace(llm =ddp)
st.header("Reasearch TOOL")
paper_input = st.selectbox("Select Research Paper name",["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"])
style_input = st.selectbox("Select Explanation style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 
length_input = st.selectbox("select Explanation length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )
# user_input = st.text_input("Enter your Prompt") # static user input

template = load_prompt("template.json")

prompt = template.invoke({
    'paper_input':paper_input,
    'style_input':style_input,
    'length_input':length_input
})
if st.button("Summarize"):
    result  = model.invoke(prompt)
    st.write(result.content)
