from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field

load_dotenv()

# Define the model
llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)


class Person(BaseModel):
    name: str = Field(description='Name of the person')
    age: int = Field(gt=18, description='Age of the person')
    city: str = Field(description='Name of the city the person belongs to')
    profession:str=Field(description="profession of person")


parser=PydanticOutputParser(pydantic_object=Person) #pydantic structured output parser


template = PromptTemplate(
    template='Generate the name, age , city  and working profession of a fictional {place} person \n {format_instruction}',
    input_variables=['place'],
    partial_variables={'format_instruction':parser.get_format_instructions()} # got filled automatically before run time
)
print(template)
chain = template | model | parser

final_result = chain.invoke({'place':'India'})

print(final_result.name)