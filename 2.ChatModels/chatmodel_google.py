from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv() # for loading  API key from .env file.

model = ChatGoogleGenerativeAI( model="gemini-2.5-flash")
result = model.invoke("what is my name?? my name is ashu")
print(result.content)