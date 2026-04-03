# now replace querry with documents
# TEXT->VECTOR

from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name ="sentence-transformers/all-MiniLM-L6-v2")
docs = [
"Delhi is the capital of India",
"kolkata is the capital of west Bengal",
"Paris is the capital of france"
]

vector = embedding.embed_documents(docs)
print(str(vector))  
