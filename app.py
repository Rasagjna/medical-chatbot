from flask import Flask,render_template,jsonify,request
from langchain_community.vectorstores import Pinecone as pc1
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from src.helper import download_hugging_face_embeddings
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.memory import ConversationSummaryMemory
from langchain.chains import RetrievalQA,ConversationalRetrievalChain,LLMChain
from langchain.chains.question_answering import load_qa_chain
from src.prompt import *
from pinecone import Pinecone
from model import llm_model
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os
app =Flask(__name__)
load_dotenv()
embeddings = download_hugging_face_embeddings()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"),environment  = os.getenv("PINECONE_API_ENV"))
index = pc.Index(os.getenv("index_name"))
docsearch = pc1.from_existing_index(os.getenv("index_name"),embeddings)
retriever = docsearch.as_retriever(search_kwargs = {"k":6})
prompt = PromptTemplate(template=prompt_template, input_variables=["context","question"])
prompt1 = PromptTemplate(template=template2,input_variables=["chat_history","question"])
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


memory = ConversationBufferMemory(
    llm=llm_model.llm, memory_key="chat_history", return_messages=True)
question_generator = LLMChain(llm=llm_model.llm,prompt = prompt1,memory=memory)
doc_chain = load_qa_chain(llm=llm_model.llm,chain_type="stuff",prompt=prompt,verbose=True)

chain = ConversationalRetrievalChain(
    question_generator = question_generator,
    retriever = retriever,
    memory=memory,
    combine_docs_chain = doc_chain,
    verbose= True
    
)
chat_history=[]

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=chain.invoke({"question": input,"chat_history":chat_history})
    print("docchain")
    print("Response : ", result["answer"])
    chat_history.append((input,result["answer"]))
    print(retriever)
    print(chat_history)
    return str(result["answer"])


if __name__ ==  "__main__":
    app.run(debug = True)