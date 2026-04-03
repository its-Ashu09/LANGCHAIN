from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "zai-org/GLM-4.7",
    task = "text-generation"
)
ddp = HuggingFaceEndpoint(
    repo_id = "deepseek-ai/DeepSeek-V3.2",
    task = "text-generation"
)
model = ChatHuggingFace(llm=ddp) 
print("according to deapseek")
result = model.invoke("what is the capital of india")
print(result.content)
model = ChatHuggingFace(llm=llm) 
print("according to Zai")
result = model.invoke("what is the capital of india")
print(result.content)