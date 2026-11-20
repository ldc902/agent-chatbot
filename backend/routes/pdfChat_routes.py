from langchain.chains import ConversationalRetrievalChain
from fastapi import APIRouter
from schemas.chatSchemas import PDFChat_Request, PDFChat_Response
from services.pdfChat_services import get_response, pdfChat_prompt, buffer_memory
from services import init_groq_model, clean_output_text
import services.pdfChat_services as pdfChat_services
from pathlib import Path
from utils.constants.index import VECTORS_DIR




router = APIRouter()

@router.post("/pdf-chat", response_model = PDFChat_Response)
def chat_pdf(request: PDFChat_Request):
    model_name = request.model_name
    query = request.query
    
    groq_model = init_groq_model(model_name, chat_mode="pdf-chat")
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm = groq_model,
        retriever = pdfChat_services.faiss_vectors.as_retriever(search_kwargs={'k':3}), # truy xuất 3 chunks gần nhất
        memory = buffer_memory,
        output_key = "answer",
        combine_docs_chain_kwargs = {"prompt": pdfChat_prompt},
        return_source_documents = True,
    )
    
    response, sources = get_response(query, qa_chain)
    cleaned_text = clean_output_text(response)
    
    return {"data": {"response": cleaned_text, "sources": sources}, "status": True}

@router.get("/files/check")
def check_folder():
    is_exist = any(Path(VECTORS_DIR).iterdir())

    return {
        "status": is_exist,
    }