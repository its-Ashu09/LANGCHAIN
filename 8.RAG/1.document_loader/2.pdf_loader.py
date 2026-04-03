#  pdf loader loads a pdf of multiple pages.
#  make document object for each pages
# if a pdf contains 23 pages then it makes 23 document object and compose them in list.

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('dl_curriculum.pdf')

docs = loader.load()

# docs = [document1,document2,document3,document4,---------------------------,document23]
"""docs = [
  Document1(
    page_content="This is the text inside cricket.txt...",
    metadata={"source": "dl_curriculum.pdf"}
  )
  Document2(
    page_content="This is the text inside cricket.txt...",
    metadata={"source": "dl_curriculum.pdf"}
  )
  and so on till document23
]

"""

print(docs)
print(len(docs))

# print(docs[0].page_content)
# print(docs[1].page_content)
print(docs[0].metadata)
