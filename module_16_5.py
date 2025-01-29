from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def Get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/user/{user_id}'")
async def Get_Users(request: Request, user_id: int) -> HTMLResponse:
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

@app.post("/user/{username}/{age}")
def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter Username')],
                    age: Annotated[int, Path(ge=18, le=80, description='Enter Age')]) -> User:
    user_id = max((user.id for user in users), default=0) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: Annotated[int, Path(ge=1,le=100, description='Enter User ID', example=1)],
                   username: Annotated[str, Path(min_length=5, max_length=20, description='Enter Username')],
                   age: Annotated[int, Path(ge=18, le=80, description='Enter Age')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
def delete_user(user_id: Annotated[int, Path(ge=1,le=100, description='Enter User ID', example="1")]) -> str:
    try:
        users.pop(user_id)
        return f"User id = {user_id} deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


#uvicorn module_16_5:app --reload
#http://127.0.0.1:8000/docs