from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq( model="openai/gpt-oss-20b")
while True:
    query = input("user: ")
    if query.lower() in ["quit",'exit','bye']:
        print("GoodBye 👋🙋‍♂️🙋‍♀️")
        break
    res = llm.invoke(query)
    print("AI: ",res.content,'\n')