from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_groq import ChatGroq
from dotenv import load_dotenv   
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch,RunnableLambda
# RunnableBranch: conditional routing (if/else logic).
# RunnableLambda: wraps a Python function as a runnable.
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Literal
load_dotenv()
# llm = HuggingFaceEndpoint(
#     repo_id="google/gemma-2-2b-it",
#     task="text-generation"
# )
# model1 = HuggingFaceEndpoint(llm=llm)

model = ChatGroq( model="openai/gpt-oss-20b")

parser = StrOutputParser()

class Feedback(BaseModel):
     sentiment: Literal['positive', 'negative'] = Field(description='Give the sentiment of the feedback')


parser2 = PydanticOutputParser(pydantic_object=Feedback)

prompt1 = PromptTemplate(
    template='Classify the sentiment of the following feedback text into postive or negative \n {feedback} \n {format_instruction}',
    input_variables=['feedback'],
    partial_variables={'format_instruction':parser2.get_format_instructions()}
)
#  classifier chain classifies the feedback is positive or negative
classifier_chain = prompt1 | model | parser2

#  prompt for positive sentiment
prompt2 = PromptTemplate(
    template='Write an appropriate response to this positive feedback \n {feedback}',
    input_variables=['feedback']
)

#  prompt for negative sentiment
prompt3 = PromptTemplate(
    template='Write an appropriate response to this negative feedback \n {feedback}',
    input_variables=['feedback']
)


branch_chain = RunnableBranch(
    #  it is like if(),else if() and else()
    #  x  = output of previous chain(which is positive or negative)
     (lambda x:x.sentiment=='positive',prompt2 | model | parser),
     (lambda x:x.sentiment=='negative',prompt3 | model | parser),
     RunnableLambda(lambda x: "could not find sentiment")
)


chain = classifier_chain | branch_chain
result =  chain.invoke({'feedback':'This is a  bad phone'})
print(result)

# chain.get_graph().print_ascii()