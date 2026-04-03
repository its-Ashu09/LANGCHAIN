# read .txt file and convert them into document object

from langchain_community.document_loaders import TextLoader

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq( model="openai/gpt-oss-20b")
prompt = PromptTemplate(
    template = 'write a 5 line summary for the following poem - \n {poem}',
    input_variables = ['poem'] 
)
parser = StrOutputParser()
# load .txt file
loader = TextLoader('cricket.txt',encoding="utf-8")

docs = loader.load()

#  load() function calls lazy_load() it opens the file read all text and create a list of DOcument object.
#  
"""
docs = [
  Document(
    page_content="This is the text inside cricket.txt...",
    metadata={"source": "cricket.txt"}
  )
]

"""
# print(docs)
# print(docs[0])
# print(docs[0].page_content)
# print(docs[0].metadata)


chain = prompt | model | parser

print(chain.invoke({'poem':docs[0].page_content}))

