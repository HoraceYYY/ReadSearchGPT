## require pip install 'langchain[llms]'
from langchain.document_loaders import PagedPDFSplitter
from langchain.llms import Cohere
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.cohere import CohereEmbeddings
import pinecone
from langchain.vectorstores import Pinecone

loader = PagedPDFSplitter("./Knowledge/report.pdf")
texts = loader.load_and_split()
## print (f'There are {data} characters in your document')
## print (f'There are {data[0].page_content} characters in your document')
## print (f'There are {data[1].page_content} characters in your document')
print (f'Now you have {len(texts)} documents')

embeddings = CohereEmbeddings(cohere_api_key="r1dsqZIgIGdU3YXJxqqstunEjq5ZgjAkMzwsrO39")

# initialize pinecone
pinecone.init(
    api_key="24b5f67e-eba8-4c64-8ee7-292ba39145fd",  # find at app.pinecone.io
    environment="us-west1-gcp"  # next to api key in console
)
index_name = "pinecone"

docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

llm = Cohere(cohere_api_key="r1dsqZIgIGdU3YXJxqqstunEjq5ZgjAkMzwsrO39")
chain = load_qa_chain(llm, chain_type="stuff")

query = "what is my highest gmat score?"
docs = docsearch.similarity_search(query, include_metadata=True)

chain.run(input_documents=docs, question=query)


