import time
from fastapi import FastAPI, HTTPException, Request, status, Response
from server.auth.jwttoken import verify_token
from server.routes.blog import blogapp as BlogApp
from server.routes.user import userapp as UserRouter
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(BlogRouter, tags=["Blog"], prefix="/blog")
app.mount('/auth', UserRouter)
app.mount('/blogs', BlogApp)
# 
@app.get("/", tags=["Root"])
async def read_root(request : Request):
    print(request.headers)
    return {"message": "Welcome to this fantastic app!"}



