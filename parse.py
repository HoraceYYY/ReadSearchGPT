"""
this file is based on the cohere

the process is

1. pdf -> array -> cohere embedding -> store in pinecone

2. query -> cohere embedding -> similarity search in pinecone -> result array

3. send original query and result array into cohere llm -> answer the query based on the result array -> send the answer back

"""

import PyPDF2
import numpy as np
import cohere
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pdf_file = open('./Knowledge/report.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

"""
parse pdf into json
"""
data = []
# Loop through each page in the PDF file
for page_num in range(len(pdf_reader.pages)):
    # Get the page object
    page_obj = pdf_reader.pages[page_num]

    # Extract the text from the page object
    text = page_obj.extract_text()

    # Add the text to the list
    data.append(text)

# Convert the data to JSON format
##json_data = json.dumps(data)

# Print the JSON data
## print(json_data)

"""
convert json into pandas dataframe
"""
##df = pd.read_json(json_data)
##df = df.rename(columns={0:"content"})
## print(df)

"""
pass data to embeddings
"""
co = cohere.Client(os.getenv("Cohere_KEY"))
embeddings = co.embed(texts=data,model='large', truncate="LEFT").embeddings
shape = np.array(embeddings).shape
## print(shape) ## check the shape of the array

"""
pass data into pinecone to store
"""
# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(api_key=os.getenv("Pinecone_KEY"), environment=os.getenv("Pinecone_ENV"))
index = pinecone.Index(os.getenv("Pinecone_INDEX"))

batch_size = 128

ids = [str(i) for i in range(shape[0])]
# create list of metadata dictionaries
meta = [{'text': text} for text in data]
## print(ids)
## print(meta)
to_upsert = list(zip(ids, embeddings, meta))

for i in range(0, shape[0], batch_size):
    i_end = min(i+batch_size, shape[0])
    index.upsert(vectors=to_upsert[i:i_end])

# let's view the index statistics
##print(index.describe_index_stats())

"""
sementic search
"""
query = input("Enter your ask here: ")

xq = co.embed(
    texts=[query],
    model='large',
    truncate='LEFT'
).embeddings

res = index.query(xq, top_k=5, include_metadata=True)
## print(res)

searchresults=[]
for match in res['matches']:
    searchresults.append(match['metadata']['text'])
# print(searchresults)
searchresults = " ".join(searchresults)
"""
infer answer from searching results
"""

prompt = "answer the question about " + query + " based on the information in " + searchresults

response = co.generate(  
    model='xlarge',  
    prompt = prompt,  
    max_tokens=400,  
    temperature=0.6,
    stop_sequences=["--"],
    truncate="END")

finalresult = response.generations[0].text
print(finalresult)