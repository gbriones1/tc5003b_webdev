import enum
from typing import Optional

from pydantic import BaseModel
from fastapi import FastAPI

class CreateItem(BaseModel):
    name: str
    description: Optional[str] = ""
    price: Optional[float] = 0.0

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    price: Optional[float] = 0.0

class ModelName(str, enum.Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items")
async def read_item(q: Optional[str] = None):
    return {"item_id": q}

@app.post("/items")
async def create_item(item: CreateItem):
    new_id = 1
    #import pdb; pdb.set_trace()
    #return_item = Item(id=new_id, name=item.name, description=item.description, price=item.price)
    new_item = item.dict()
    new_item["id"] = new_id
    return_item = Item(**new_item)
    return return_item

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}