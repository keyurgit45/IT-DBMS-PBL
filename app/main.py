from fastapi import FastAPI
from server.routes.blog import router as BlogRouter

app = FastAPI()

app.include_router(BlogRouter, tags=["Blog"], prefix="/blog")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}