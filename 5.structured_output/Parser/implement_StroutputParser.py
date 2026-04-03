# in this we do not use parser directly but we create a situation why parsers are important



from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)


#1st prompt-> we want detailed report on a topic

template1 = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)




#2nd prompt ->summary

template2 = PromptTemplate(
 template ='write a 5 line summary on the following text. /n {text}',
 input_variables=['text']   
)

# use Parser
parser = StrOutputParser()
#  template1->model->parser(structured ouput)->template2 ->model(2nd times model calling)->parser
chain = template1 | model | parser | template2 | model | parser
result = chain.invoke({'topic':'black hole'})

print(result)