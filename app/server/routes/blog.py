import re
from typing import List
from fastapi import Body, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.encoders import jsonable_encoder
from server.auth.jwttoken import verify_token
from starlette.responses import JSONResponse
import motor.motor_asyncio
from server.database import (
    add_blog,
    delete_blog,
    retrieve_blog,
    retrieve_userblog,
    retrieve_blogs,
    update_blog,
)
from server.models.blog import (
    BlogSchema,
    UpdateBlogModel,
    ErrorResponseModel,
    ResponseModel
)


MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.blogapp

blogapp = FastAPI(title="Blogs API")
# router = APIRouter()

@blogapp.middleware('http')
async def verify_login(request: Request, call_next):
    if(request.cookies.get('_token')):
        token = request.cookies.get('_token')
        username = verify_token(token, HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        ) )
        user = await database['users'].find_one({"username": username.username})
        uid = str(user['_id'])
        request.headers.__dict__["_list"].append(("uid".encode(), uid.encode()))
        
        # response.set_cookie('_u',username , httponly=True, expires=30 * 60,secure=True)
        response = await call_next(request)
        return response
    else:
        return JSONResponse(content={
            "message": "Please LogIn to access Database."
        }, status_code=401)


@blogapp.post("/add", response_description="Blog data added into the database", tags=["Blog"])
async def add_blog_data(request: Request, title: str, content: str, description: str, keywords: List[str] = Query(None) ):
    blog = BlogSchema(title=title, content= content, description=description, author="", user="", likes=0, keywords=keywords)
    uid = request.headers.get('uid')
    blog = jsonable_encoder(blog)
    new_blog = await add_blog(blog, uid)
    return ResponseModel(new_blog, "blog added successfully.")


@blogapp.get("/",summary="Show all Blogs", response_description="Returns All blogs from the database", tags=["Blog"])
async def show_blogs():
    blogs = await retrieve_blogs()
    return ResponseModel(blogs, "blogs fetched successfully.")

@blogapp.get("/myblogs",summary="Show blogs of Logged in user", response_description="Returns All blogs for the id given", tags=["Blog"])
async def show_blog(request: Request):
    uid = request.headers.get('uid')
    blog = await retrieve_userblog(uid)
    return ResponseModel(blog, "blog fetched successfully.")

@blogapp.get("/{id}", response_description="Returns All blogs for the id given", tags=["Blog"])
async def show_blog(id : str):
    blog = await retrieve_blog(id)
    return ResponseModel(blog, "blog fetched successfully.")

@blogapp.put("/{id}", response_description="Updates Blog", tags=["Blog"])
async def update_blog_id(request: Request, id : str, blog : UpdateBlogModel = Body(...) ):
    blog = {k: v for k, v in blog.dict().items() if v is not None }
    uid = request.headers.get('uid')
    updated_student = await update_blog(id,uid, data=blog )
    if updated_student:
        return ResponseModel(
            "Blog with ID: {} update is successful".format(id),
            "Blog updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Blog data.",
    )

@blogapp.delete("/{id}",summary="Deletes a blog", response_description="Blog deleted from the database", tags=["Blog"])
async def delete_student_data(request: Request, id: str):
    uid = request.headers.get('uid')
    deleted_student = await delete_blog(id, uid)
    if deleted_student:
        return ResponseModel(
            "Blog with ID: {} removed".format(id), "Blog deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Blog with id {0} doesn't exist".format(id)
    )

