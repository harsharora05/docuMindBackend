from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
load_dotenv()

def index_file(file_path:str,unique_filename:str):
    try:
        loader = PyPDFLoader(file_path)
        doc = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
        split_docs=text_splitter.split_documents(doc)  

        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        vector_store = QdrantVectorStore.from_documents(
        split_docs,
        url= "http://localhost:6333",
        collection_name=unique_filename,
        embedding=embeddings,
        )

        return {
        "ok": True,
        "status": "Indexing completed",
        }
    except:
        return {
        "ok": False,
        "status": "Indexing Failed",
        }



