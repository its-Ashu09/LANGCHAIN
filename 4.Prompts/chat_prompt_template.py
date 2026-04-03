
#CHAT PROMPT TEMPLATE - to dynamically insert chat history or a list of messages at runtime.



from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate([
    ("system",'you are a helpful {domain} expert'),
    ("human","Explain in simple terms, what is {topic}")
])

prompt = chat_template.invoke({'domain':'cricket','topic':'batting'})

print(prompt)