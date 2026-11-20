import uvicorn
from fastapi import FastAPI, APIRouter
from routes import pdfChat_routes, nomalChat_routes, upload_routes


app = FastAPI(title="LangGraph AI Agent")

api_router = APIRouter(prefix="/api")

api_router.include_router(pdfChat_routes.router, prefix="/chat")
api_router.include_router(nomalChat_routes.router, prefix="/chat")
api_router.include_router(upload_routes.router)

app.include_router(api_router)

@app.get("/")
def run_main():
    return {"message": "API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 3001)