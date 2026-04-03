from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id='remon-rakibul/TinyLama-1.1B-Chat-V0.3-AWQ',
    task = 'text-generation',
    pipeline_kwargs=dict(
        temperature = 0.5,
        max_new_token=100
    )
    
)
model =ChatHuggingFace(llm=llm)
result = model.invoke("what is the capital of india")
print(result.content)