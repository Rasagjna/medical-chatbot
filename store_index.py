from src.helper import load_pdf,text_split,download_hugging_face_embeddings
from langchain_community.vectorstores import Pinecone as pc1
from  pinecone import Pinecone 
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"),environment  = os.getenv("PINECONE_API_ENV"))
index = pc.Index(os.getenv("index_name"))
extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()
docsearch = pc1.from_texts([t.page_content for t in text_chunks],embeddings,index_name=os.getenv("index_name"))