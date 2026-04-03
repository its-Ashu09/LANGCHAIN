from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader


loader = DirectoryLoader(
    path='Books',
    glob = '*.pdf',
    loader_cls=PyPDFLoader
)

docs  = loader.load()
# docs  = loader.lazy_load() --> it loads firstly document1 then delete them then loads document2 then delete them and so on
# print(len(docs))
# for documents in docs:
#  print(documents.metadata)
print(docs[0].page_content)