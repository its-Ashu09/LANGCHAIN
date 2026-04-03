from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage
load_dotenv()

ddp = HuggingFaceEndpoint(
    repo_id = "deepseek-ai/DeepSeek-V3.2",
    task = "text-generation"
)
model = ChatHuggingFace(llm=ddp) 
chat_history = [SystemMessage(content="You are a helpful AI asistant")]

while True:
   user_input  = input("You: ")
   chat_history.append(HumanMessage(content=user_input))
   if user_input=="exit":
      break
   result =  model.invoke(chat_history)
   chat_history.append(AIMessage(content=result.content))
   print("AI: ",result.content)

print(chat_history)