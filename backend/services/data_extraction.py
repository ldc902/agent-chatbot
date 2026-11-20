import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from utils.constants.index import DATASET_DIR, VECTORS_DIR
from .init_models import embedding_model



def load_files(dir_path):
    loader = DirectoryLoader(dir_path,
                             glob = '*.pdf',
                             loader_cls = PyPDFLoader)
    
    docs = loader.load()
    return docs

def create_chunks(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500, 
        chunk_overlap = 50  # phần trùng (giữ ngữ cảnh)
    )
    
    chunks = splitter.split_documents(docs)
    return chunks

def extract_data():
    # load dataset
    docs = load_files(dir_path = DATASET_DIR)

    # chunks
    chunks = create_chunks(docs)

    # vectors = embedding_model.embed_documents([chunk.page_content for chunk in chunks])

    # embed + create vectors
    faiss_vectors = FAISS.from_documents(chunks, embedding_model)
    
    index_faiss = os.path.join(VECTORS_DIR, "index.faiss")
    index_pkl = os.path.join(VECTORS_DIR, "index.pkl")

    if os.path.exists(index_faiss) and os.path.exists(index_pkl):
        existing_vectors = FAISS.load_local(VECTORS_DIR, embedding_model, allow_dangerous_deserialization=True)
        
        existing_vectors.merge_from(faiss_vectors)
        
    else:
        faiss_vectors.save_local(VECTORS_DIR)