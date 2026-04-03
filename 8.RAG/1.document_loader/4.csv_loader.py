from langchain_community.document_loaders import CSVLoader
loader = CSVLoader(file_path='social_network_ads.csv')
docs = loader.load()
# for each row a document object created
print(len(docs))

print(docs[0])