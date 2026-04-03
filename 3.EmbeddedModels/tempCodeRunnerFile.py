from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

load_dotenv()

embedding = HuggingFaceEmbeddings(model_name ="sentence-transformers/all-MiniLM-L6-v2")

documents = [
    "virat kohli is an indian cricketer known for his agressive batting",
    "Ms Dhoni is a former indian captain famous for his calmness",
    "Sachin tendulkar also known as the god of cricket",