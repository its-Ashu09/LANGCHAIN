from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

load_dotenv()

embedding = HuggingFaceEmbeddings(model_name ="sentence-transformers/all-MiniLM-L6-v2")

documents = [
    "virat kohli is an indian cricketer known for his agressive batting",
    "Ms Dhoni is known for his name captain cool",
    "Sachin tendulkar also known as the god of cricket",
    "Rohit sharma is known for his batting and record breaking",
    "jasprit bumrah is and indian fast bowler known for his action"

]

query = "MS dhoni"

doc_embeddings  = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)

scores = cosine_similarity([query_embedding],doc_embeddings)[0]  # ek list bnegi jisme 5 similaraty score honge jiski value sbse jyda hogi whi chaiye.
index,scores = sorted(list(enumerate(scores)),key=lambda x:x[1])[-1]

print(documents[index])






