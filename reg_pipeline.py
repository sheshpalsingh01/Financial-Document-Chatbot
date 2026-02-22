import os
import dotenv
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader, TextLoader, PyMuPDFLoader, UnstructuredPDFLoader
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

load_dotenv()

# load api key
api_key = os.getenv("NVIDIA_API_KEY")

def build_reg_chain(file_path):
    

 file_extension = os.path.splitext(file_path)[1].lower()

#uploade the file

 if file_extension ==".pdf":
    loader = PyMuPDFLoader(file_path=file_path)
 elif file_extension ==".txt":
    loader = TextLoader(file_path=file_path)
 elif file_extension ==".csv":
    loader = CSVLoader(file_path=file_path)
 else:
    raise ValueError("Unsupported file type")
    
 data =loader.load()

## Split the text

 split_docs = RecursiveCharacterTextSplitter(
     chunk_size=1000,
     chunk_overlap=100
     )
 split_docs = split_docs.split_documents(data)


## Embedding, store, retriever
 embedding = NVIDIAEmbeddings(nvidia_api_key=api_key)
 llm = ChatNVIDIA(model="nvidia/nemotron-3-nano-30b-a3b",nvidia_api_key=api_key)

 vectorstore= FAISS.from_documents(documents=split_docs,embedding=embedding)
 retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5},
    search_type="mmr"
    )
 
 
## retrieve chain
 prompt = ChatPromptTemplate.from_template(
    
    """You are a financial analysis assistant. 
    Answer strictly from provided context.
    If information is missing, say "Not found in document."

    FORMAT RULES:
    - Use clear headings
    - Use bullet points or short paragraphs
    - Avoid unnecessary tables unless explicitly requested
    - Keep answers concise and readable
    - No decorative markdown like **bold everywhere**
    - also detail explaination by this
    
    Focus specifically on:
    - Numerical values
    - Growth rates
    - Percentages
   - Financial metrics.
   Do not omit numeric details. 
   
    Context:
    {retrieved_text}
    
    Question:
    {user_question}
    """
)

 retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5},
    search_type="mmr"
    )

 def format_docs(docs):
    if not docs:
        return "No relevant Context found"
    return "\n\n".join(doc.page_content for doc in docs)

 ## Chain
 chain = (
    {
        "retrieved_text": retriever | RunnableLambda(format_docs),
        "user_question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
 )
 
 return chain

# vectorstore.save_local("faiss_index")
# FAISS.load_local('faiss_index',embeddings=embedding)



  
   

   

 