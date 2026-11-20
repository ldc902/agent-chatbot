import uuid
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import MemorySaver
from langchain_tavily import TavilySearch
from utils.constants.templates import NORMAL_CHAT_TEMPLATE, PROVIDERS

search_tool = TavilySearch(max_results = 2)
memory = MemorySaver()
thread_id = str(uuid.uuid4())

def create_prompt (
    state: AgentState,
    config: RunnableConfig,
) -> list[AnyMessage]:
    user_name = config["configurable"].get("user_name")
    query = f"User's name is {user_name}. {NORMAL_CHAT_TEMPLATE}"
    
    return [{"role": "system", "content": query}] + state["messages"]  

pre_model = ""
pre_agent = None

def init_agent(model_name, provider, allow_search: bool = False):
    global pre_model, pre_agent
    
    if model_name == pre_model:
        return pre_agent
    
    pre_model = model_name
    
    initialized_model = PROVIDERS[provider]["init_func"](model_name)
    tools = []
    
    if allow_search:
        tools.append(search_tool)
        
    agent = create_react_agent(
        model = initialized_model,
        tools = tools,
        prompt = create_prompt,
        checkpointer = memory
    )
    
    pre_agent = agent
    
    return agent
