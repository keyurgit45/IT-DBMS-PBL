from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_blog,
    delete_blog,
    retrieve_blog,
    retrieve_blogs,
    update_blog,
)
from server.models.blog import (
    BlogSchema,
    UpdateBlogModel,
    ErrorResponseModel,
    ResponseModel
)

router = APIRouter()

@router.post("/add", response_description="Blog data added into the database")
async def add_blog_data(blog : BlogSchema = Body(...)):
    blog = jsonable_encoder(blog)
    new_blog = await add_blog(blog)
    return ResponseModel(new_blog, "blog added successfully.")


@router.get("/", response_description="Returns All blogs from the database")
async def show_blogs():
    blogs = await retrieve_blogs()
    return ResponseModel(blogs, "blogs fetched successfully.")

@router.get("/{id}", response_description="Returns All blogs for the id given")
async def show_blog(id : str):
    blog = await retrieve_blog(id)
    return ResponseModel(blog, "blog fetched successfully.")

@router.put("/{id}", response_description="Updates Blog")
async def update_blog_id(id : str, blog : UpdateBlogModel = Body(...)):
    blog = {k: v for k, v in blog.dict().items() if v is not None}
    updated_student = await update_blog(id, data=blog)
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

@router.delete("/{id}", response_description="Blog deleted from the database")
async def delete_student_data(id: str):
    deleted_student = await delete_blog(id)
    if deleted_student:
        return ResponseModel(
            "Blog with ID: {} removed".format(id), "Blog deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Blog with id {0} doesn't exist".format(id)
    )