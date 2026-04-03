from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from langchain_core.documents import Document


from dotenv import load_dotenv
load_dotenv()

doc1 = Document(
        page_content="Virat Kohli is one of the most successful and consistent batsmen in IPL history. Known for his aggressive batting style and fitness, he has led the Royal Challengers Bangalore in multiple seasons.",
        metadata={"team": "Royal Challengers Bangalore"}
    )
doc2 = Document(
        page_content="Rohit Sharma is the most successful captain in IPL history, leading Mumbai Indians to five titles. He's known for his calm demeanor and ability to play big innings under pressure.",
        metadata={"team": "Mumbai Indians"}
    )
doc3 = Document(
        page_content="MS Dhoni, famously known as Captain Cool, has led Chennai Super Kings to multiple IPL titles. His finishing skills, wicketkeeping, and leadership are legendary.",
        metadata={"team": "Chennai Super Kings"}
    )
doc4 = Document(
        page_content="Jasprit Bumrah is considered one of the best yorker king in T20 cricket. Playing for Mumbai Indians, he is known for his yorkers and death-over expertise.",
        metadata={"team": "Mumbai Indians"}
    )
doc5 = Document(
        page_content="Ravindra Jadeja is a dynamic all-rounder who contributes with both bat and ball. Representing Chennai Super Kings, his quick fielding and match-winning performances make him a key player.",
        metadata={"team": "Chennai Super Kings"}
    )

docs  = [doc1, doc2, doc3, doc4, doc5]


vector_store = Chroma(
    embedding_function= HuggingFaceEmbeddings(model_name ="sentence-transformers/all-MiniLM-L6-v2"),
    persist_directory='my_chroma_db',
    collection_name='sample'
)
# add documents
vector_store.add_documents(docs)

# view documents
# result =vector_store.get(include=['embeddings','documents','metadatas'])

#  delete documents
# vector_store.delete(ids=[       
#     #   add id in list which you want to delete , you can add multiple Ids.
#     # 'afe02aed-73d3-4f6c-a4ef-5e8b4fc82105', 'ddafe612-8625-4227-9b36-821276a513f3', 'af1fa62a-3803-4987-a109-903bc52a1af3', 'b1933f97-2ed1-4f51-b203-c24d777919ef', '698a775c-1c16-45e7-a8da-452b7148737e', 'e3713271-7a36-416a-9839-35317a23c338', '22b8bee3-cede-48c3-b79d-a7f4540623b7', '0a63bf6d-db7a-44ab-a41a-52146cbdc544', '02d05e21-0457-4b9d-8ca3-55a4a28edb76', '8b6649ad-d119-4ec4-81b1-409bdda0ccb4'            
                         
#                          ])
# print(result)


# search documents
vector_store.similarity_search(
    query='Who among these are a bowler?',
    k=2
)

# search with similarity score
# result1 =vector_store.similarity_search_with_score(
#     query='give the name of a allrounder player name who is known for batting and bowling both?',
#     k=1# k means how many number of most similar document to be return.
# )

# meta-data filtering
# filtering  = vector_store.similarity_search_with_score(
#     query="",
#     filter={"team": "Chennai Super Kings"}
# )

# update documents
# updated_doc1 = Document(
#     page_content="Virat Kohli, the former captain of Royal Challengers Bangalore (RCB), is renowned for his aggressive leadership and consistent batting performances. He holds the record for the most runs in IPL history, including multiple centuries in a single season. Despite RCB not winning an IPL title under his captaincy, Kohli's passion and fitness set a benchmark for the league. His ability to chase targets and anchor innings has made him one of the most dependable players in T20 cricket.",
#     metadata={"team": "Royal Challengers Bangalore"}
# )

# result = vector_store.update_document(document_id='b917a97c-3547-46a7-81c8-1bbea9adf30c', document=updated_doc1)
result =vector_store.get(include=['embeddings','documents','metadatas'])
# print(filtering)
print(result)
# print(result1)
