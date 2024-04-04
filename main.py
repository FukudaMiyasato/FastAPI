from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Item(BaseModel):
    text: str
    is_done: bool = False

items = []

app = FastAPI()


@app.get('/')
def root():
    return{'hello':'world'}

@app.post('/items')
def create_item(item: Item):
    items.append(item)
    return items


@app.get('/itemsShow')
def root():
    return items

@app.get('/item_id/{item_id}')
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail ='Item not found')