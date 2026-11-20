from langchain_core.messages.ai import AIMessage
from fastapi import APIRouter
from schemas.chatSchemas import NormalChat_Request, NormalChat_Response
from services.normalChat_services import init_agent, thread_id
from services import clean_output_text


router = APIRouter()

@router.post("/normal-chat", response_model = NormalChat_Response)
def chat(request: NormalChat_Request):
    query = request.query
    provider = request.provider.lower()
    model_name = request.model_name
    allow_search = request.allow_search
    
    agent = init_agent(model_name, provider, allow_search)
    
    result = agent.stream(
        input = {"messages": [{"role": "user", "content": query}]}, 
        config = {"configurable": {"user_name": "Cuong Badboy", "thread_id": thread_id}},
        stream_mode = "values"
    )
    
    # result = agent.invoke(...)
    # last_message = result["messages"][-1]
    
    # lặp qua mỗi node
    for step in result:
        last_message = step["messages"][-1]
        # print(last_message.text())
        # print(last_message)
        
        if hasattr(last_message, "content"):
            cleaned_text = clean_output_text(last_message.content)
        
    if isinstance(last_message, AIMessage):
        return {"data": cleaned_text, "status": True}
    else:
        print("No message found!!!")
        return {"data": "", "status": False}