"""
this program will handle raw data to create embedding and transfer into pandas df for QA
"""

import os
import openai
from dotenv import load_dotenv
import pinecone
import numpy as npode
import tiktoken
from itertools import islice
import glob
import math


""" 
Connecting to Open AI API and assign models
"""
load_dotenv()
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")  

EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_CTX_LENGTH = 1024 ## max token length for embedding; The theoritical max at the moment is 8k, but that is too large to be passed to the gpt model for promopt which has a limit of 4k tokens
EMBEDDING_ENCODING = 'cl100k_base' ## encoding method for the embedding model

"""
Connecting to pincone API and assign index
"""
index_name = input("Enter the database you would like to choose: ")

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    api_key=os.getenv("Pinecone_KEY"),
    environment=os.getenv("Pinecone_ENV")
)

"""
open text file and read into an virable; This is a simple text file. If the input is a database, it can be loaded with pandas df
"""

def load(folder_path):
    rawdata = ""
    for file_path in glob.glob(folder_path):
        with open(file_path, 'r') as file:
            rawdata += file.read()

    return rawdata   

"""
count the number of token for the raw data
"""
def num_tokens_from_string(string: str, encoding_name = EMBEDDING_ENCODING ) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


"""
Convert the text into token
Check if the token size is within limit
Cut the tokens if it is not within limits
"""
## helpper function to cut strings into sized chunck
def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := tuple(islice(it, n))):
        yield batch

def chunked_tokens(text, encoding_name = EMBEDDING_ENCODING, chunk_length = EMBEDDING_CTX_LENGTH):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    if len(tokens) <= chunk_length:
        return tokens
    else:
        chunks_iterator = batched(tokens, chunk_length)
        yield from chunks_iterator

"""
get the chucked text into embedding and structure the oringle text and embedding to pinecone vectors onject
vectorobjects=[
        (
         "vec1",                # Vector ID 
         [0.1, 0.2, 0.3, 0.4],  # Dense vector values
         {"genre": "drama"}     # Vector metadata
        ),
        (
         "vec2", 
         [0.2, 0.3, 0.4, 0.5], 
         {"genre": "action"}
        )
    ]
"""
def len_safe_get_embedding(text, model=EMBEDDING_MODEL, max_tokens=EMBEDDING_CTX_LENGTH, encoding_name=EMBEDDING_ENCODING, average=False):
    chunk_embeddings = [] # store embedding
    chunk_text = [] # store text for meta data
    vector_id = [] # store vector id for embeddings
    chunk_lens = []

    for i, chunk in enumerate(chunked_tokens(text, encoding_name=encoding_name, chunk_length=max_tokens)):
        chunk_embeddings.append(get_embedding(chunk, model=model)) ## this is the vecot value in the pinecone vector objects
        chunk_text.append({"text" : tiktoken.get_encoding(encoding_name).decode(chunk).strip()}) ## this is the orginal text to be sore in the meta data
        vector_id.append("vec" + str(i)) ## this is vector id
        chunk_lens.append(len(chunk))

    if average: ## if we average the multiple embedding vector, I am not sure how these average vector will be used to translate back to the text for context
        chunk_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
        chunk_embeddings = chunk_embeddings / np.linalg.norm(chunk_embeddings)  # normalizes length to 1
        chunk_embeddings = chunk_embeddings.tolist()
    
    to_upsert = list(zip(vector_id,chunk_embeddings,chunk_text)) ## this is vector id, vecor value, vector metadata
    return to_upsert


"""
helper function for return the embeded value
"""
def get_embedding(text_or_tokens, model=EMBEDDING_MODEL):
    return openai.Embedding.create(input=text_or_tokens, model=model)["data"][0]["embedding"]

    
"""
this is the main function to 
"""
def main(data_folder_path):
    rawdata = load(data_folder_path) ## replace the path with the inout variable
    print("Total # of Token is: ", num_tokens_from_string(rawdata))
    print("Total # of vector should be: ", math.ceil(num_tokens_from_string(rawdata)/EMBEDDING_CTX_LENGTH))
    to_upsert = len_safe_get_embedding(rawdata) # create pinecore vector object to be upserted
    index = pinecone.Index(index_name) ## connect to index
    print(index.describe_index_stats()) # view index stats
    index.upsert(vectors=to_upsert) # upsert pinecone vector objects 

    return print("Raw data is processed and embedded in pinecone!")


if __name__ == "__main__":
    main("Raw Data/*")