#!/usr/bin/env python
# coding: utf-8

# In[1]:


from dotenv import load_dotenv
load_dotenv()


# In[21]:


from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings,ChatHuggingFace
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate


# YouTubeTranscriptApi → used to fetch subtitles
# 
# TranscriptsDisabled → exception raised when a video has no captions
# 
# Note -- indexing means document ingestion(document loader)

# STEP1a-->> Indexing (Document Ingestion)

# In[ ]:


video_id = "Gfr50f6ZBvo" # only the ID, not full URL
try:
    #Creates an instance of YouTubeTranscriptApi() and calls .fetch() on it.
     fetched_transcript = YouTubeTranscriptApi().fetch(video_id,languages=["en"])
     """
     fetched_transcript look like as-->
     Transcript([
     {'text': 'Hello everyone', 'start': 0.0, 'duration': 2.0},
     {'text': 'Welcome to this video', 'start': 2.0, 'duration': 3.0},
     ])

     """
     transcript_list  = fetched_transcript.to_raw_data()
     """
     list is like this-->
     transcript_list = [
       {"text": "Hello everyone", "start": 0.0, "duration": 2.3},
       {"text": "Welcome to this video", "start": 2.3, "duration": 3.1},
     ]
     """

     # print(transcript_list)

     #  join all chunks in a text plane
    #  chunk["text"] → extracts only the text field
     transcript = " ".join(chunk["text"] for chunk in transcript_list)
     print(transcript)


except TranscriptsDisabled:
    print("No captions available for this video.")


# Step 1b-Indexing(Text Splitting)

# In[13]:


splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunks = splitter.create_documents([transcript]) 
#  chunks is a list of document object
"""
Chunks:
[ Document(page_content=chunk1),
  Document(page_content=chunk2),
  Document(page_content=chunk3), ... ]
"""
len(chunks)
chunks[1].page_content


# Step 1c & 1d - Indexing (Embedding Generation and Storing in Vector Store)

# In[15]:


embedding = HuggingFaceEmbeddings(
model_name ="sentence-transformers/all-MiniLM-L6-v2"
)

# creating FAISS vector store and store all embeddings of each chunks
vector_store = FAISS.from_documents(chunks,embedding)


# In[ ]:


vector_store.index_to_docstore_id
# Each embedding gets a unique ID internally,
# which is used to track it in the index.


# In[ ]:


vector_store.get_by_ids(['477f1c0a-dceb-4f8b-925d-75f36ea9f3c2'])


# Step 2 - Retrieval
# 

# In[ ]:


retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
# vector store ko retriever ka interface de diya.
# retriever.invoke('summarize the whole video')


# Step 3 - Augmentation

# In[22]:


llm =ChatGroq( model="openai/gpt-oss-120b",temperature=0.2)


# In[24]:


question = "is the topic of nuclear fusion discussed in this video? if yes then what was discussed"
retrieved_docs = retriever.invoke(question)


# In[25]:


retrieved_docs


# In[23]:


prompt = PromptTemplate(
    template="""
You are a helpful assistant.
Answer ONLY from the provided transcript context.
if the context is insufficient, just say you don't know.

{context}
Question: {question}

""",
input_variables= ['context','question']

)


# In[ ]:


context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
context_text
# list of retrieve_docs ke sare documents ko ek plane text bna diya


# In[27]:


final_prompt= prompt.invoke({"context":context_text,"question":question})
print(final_prompt)


# Step 4 - Generation

# In[29]:


answer = llm.invoke(final_prompt)
answer.content


# Here we see we have to invoke all the components individually so we need to form a chain

# In[33]:


from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser


# In[31]:


def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text


# In[34]:


parallel_chain = RunnableParallel({
    'context':retriever | RunnableLambda(format_docs),
    'question':RunnablePassthrough()
})


# In[ ]:


# parallel_chain.invoke('who is Demis')


# In[36]:


parser = StrOutputParser()


# In[37]:


main_chain = parallel_chain | prompt | llm | parser


# In[40]:


main_chain.invoke('what is the photosynthesis')

