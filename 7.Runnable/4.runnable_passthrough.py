
#  in runnable sequence we creeate a joke and find explanation of joke and print the explanation

# need of passthrough--> we want  print the joke and explanation both

# prompt1->model->create a joke
# createdjoke]->model->explain -> print explanation                       ] ->
        #    ] ->passthrough->print joke

from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv   
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough
load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)
parser = StrOutputParser()

prompt1 = PromptTemplate(
    template='Write a joke about {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Explain the following joke - {text}',
    input_variables=['text']
)
# generating joke
joke_gen_chain = RunnableSequence(prompt1, model, parser)


parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(), # input --> as it is output
    'explanation': RunnableSequence(prompt2, model, parser)
})

final_chain = RunnableSequence(joke_gen_chain, parallel_chain)
# final chain result-> it is a dictionary like this
# {
#   "joke": "Why did the cat sit on the computer? ...",
#   "explanation": "The joke is funny because cats chase mice..."
# }
result = final_chain.invoke({'topic':'cricket'})

print(result)