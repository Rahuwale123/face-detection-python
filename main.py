from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.search import search_router
from app.routes.store import store_router

load_dotenv()
app = FastAPI()

app.include_router(search_router)
app.include_router(store_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
