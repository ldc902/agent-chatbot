from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEmbeddings
from utils.constants.index import OPENAI_API_KEY, GROQ_API_KEY, HF_TOKEN
from utils.constants.embeddingModels import EMBEDDING_MODEL



def init_openai_model(model_name, **kwargs):
    return ChatOpenAI(model = model_name, temperature = 0.5, verbose = True, api_key = OPENAI_API_KEY, **kwargs)

pre_groq_model_name = ""
pre_groq_model = None

def init_groq_model(model_name, chat_mode = "normal-chat", **kwargs):
    if chat_mode == "normal-chat":
        return ChatGroq(model = model_name, temperature = 0.5, verbose = True, api_key = GROQ_API_KEY, **kwargs)
    elif chat_mode == "pdf-chat":
        global pre_groq_model_name, pre_groq_model
        
        if model_name == pre_groq_model_name:
            return pre_groq_model
        
        groq_model = ChatGroq(model = model_name, temperature = 0.0, verbose = True, api_key = GROQ_API_KEY, **kwargs)
        
        pre_groq_model_name = model_name
        pre_groq_model = groq_model
        
        return groq_model
    
embedding_model = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL)

pre_hf_model_name = ""
pre_hf_model = None

def init_hf_model(model_name, chat_mode = "normal-chat", **kwargs):
    if chat_mode == "normal-chat":
        hf_model = HuggingFaceEndpoint(
            repo_id = model_name,
            provider = "hf-inference",
            task = "text-generation",
            temperature = 0.5,
            verbose = True,
            max_new_tokens = 512,
            huggingfacehub_api_token = HF_TOKEN,
            **kwargs
        )
        
        return ChatHuggingFace(
            llm = hf_model,
        )
        
    elif chat_mode == "pdf-chat":
        global pre_hf_model_name, pre_hf_model
        
        if model_name == pre_hf_model_name:
            return pre_hf_model
        
        hf_model = HuggingFaceEndpoint(
            repo_id=model_name,
            task = "text-generation",
            temperature = 0.5,
            verbose = True,
            max_new_tokens = 512,
            huggingfacehub_api_token = HF_TOKEN,
            **kwargs
        )
        
        pre_hf_model_name = model_name
        pre_hf_model = hf_model
        
        return hf_model