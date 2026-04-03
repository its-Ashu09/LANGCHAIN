# there are three types of messages
# 1. System messages = first instruction in which you assign a role to AI
# 2. AI messages
# 3. Human messages

from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
load_dotenv()
ddp = HuggingFaceEndpoint(
    repo_id = "deepseek-ai/DeepSeek-V3.2",
    task = "text-generation"
)
model = ChatHuggingFace(llm=ddp) 

messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="Tell me about langchain")
    
]
result=model.invoke(messages)

messages.append(AIMessage(content=result.content))

print(messages)
