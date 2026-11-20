from pydantic import BaseModel
from langchain_core.documents import Document

class NormalChat_Request(BaseModel):
    query: str
    model_name: str
    provider: str
    allow_search: bool
    
class PDFChat_Request(BaseModel):
    query: str
    model_name: str
    
class NormalChat_Response(BaseModel):
    data: str | None
    status: bool
    
class PDFChat_Response(BaseModel):
    data: dict[str, str | list[Document]] | None
    status: bool