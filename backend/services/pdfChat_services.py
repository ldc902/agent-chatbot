from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import Runnable
from utils.constants.templates import PDF_CHAT_TEMPLATE
from utils.constants.index import VECTORS_DIR
from services.init_models import embedding_model
from langchain.memory import ConversationBufferMemory
from pathlib import Path
from .data_extraction import extract_data



def load_faiss():
    if any(Path(VECTORS_DIR).iterdir()):
        faiss_vectors = FAISS.load_local(VECTORS_DIR, embedding_model, allow_dangerous_deserialization = True)
        
        return faiss_vectors
    
    else:
        return
    
# load faiss vectors
faiss_vectors = load_faiss()

def reload_faiss():
    global faiss_vectors
    
    faiss_vectors = load_faiss()

def create_pdfChat_prompt():
    pdfChat_prompt = PromptTemplate(
        template = PDF_CHAT_TEMPLATE, input_variables = ["context", "chat_history", "question"]
    )
    
    return pdfChat_prompt

pdfChat_prompt = create_pdfChat_prompt()

def create_buffer_memory():
    buffer_memory = ConversationBufferMemory( 
        memory_key = "chat_history",     
        input_key = "question",          
        output_key = "answer",           
        return_messages = True
    )
    
    return buffer_memory

buffer_memory = create_buffer_memory()

def get_response(query: str, qa_chain: Runnable) -> tuple[str, list]:
    result = qa_chain.invoke({'question': query})
    response = result["answer"]
    sources = result.get("source_documents", [])
    return response, sources
