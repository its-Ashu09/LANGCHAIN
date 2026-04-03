#  for basic URL.


from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

parser =StrOutputParser()
prompt = PromptTemplate(
    template='Answer the following question \n {question} from the following text - \n {text}',
    input_variables=['question','text']
)

url = "https://www.flipkart.com/daniel-clarion-dc-1104-blk-hmtr-quartz-day-date-working-stylish-analog-watch-boys-men/p/itmcd63c415a8e5a?pid=WATGWZQEB9KGGU4Z&lid=LSTWATGWZQEB9KGGU4ZKSW95X&marketplace=FLIPKART&store=r18%2Ff13&srno=b_1_1&otracker=browse&fm=organic&iid=en_VYkl1sIdM1CCvSKtTUvlCNugRXP6a4bci2nTjL1AUdVFTHKB8aGFAGbiQOJ8ZUSvZojg2CX4h5Wo7vKloFPKpA%3D%3D&ppt=None&ppn=None&ssid=wapjssyw1c0000001767969146801"
loader = WebBaseLoader(url)

docs = loader.load()

chain = prompt | model | parser
result =chain.invoke({'question':'what is the product we are talking about?','text':docs[0].page_content})
print(result)