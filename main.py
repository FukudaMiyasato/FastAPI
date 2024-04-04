from fastapi import FastAPI, HTTPException, Body, Path, Query
from pydantic import BaseModel,Field
from typing import Optional,List
from fastapi.responses import HTMLResponse,JSONResponse
from config.database import Session,engine,Base
from models.movie import Movie as MovieModel


Base.metadata.create_all(bind=engine)

class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field(min_length=5, max_length=15)
    overview: str
    year: int
    rating: float
    category: str

    class Config:
        schema_extra={
            "example":{
                "id":1,
                "title":"Descripción de la película",
                "year":2022,

            }
        }

items = []

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = '0.0.1'

movies =[
    {
        "id":1,
        "title":'Avatar',
        "overview":"En un exuberante planeta",
        "year":"2009",
        "rating": 7.8,
        "category":"Accion"
    },
    {
        "id":2,
        "title":'Avatar 2',
        "overview":"En un exuberante planeta",
        "year":"2009",
        "rating": 7.8,
        "category":"Accion"
    }
]
@app.get('/', tags=['Home'])
def root():
    return HTMLResponse('<h1>HOLA</h1>')


@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies()-> List[Movie]:
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags =['movies'])
def get_movie(id:int = Path(ge=1,le=2000)):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category:str=Query(min_length=5,max_length=15)):
    data= [item for item in movies if item['category'] == category]
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'])
def create_movie(movie :Movie):
    db=Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content=movies)
@app.put('/movies/{id}', tags=['movies'])
def update_movie(id:int,movie:Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category

            return JSONResponse(content={'message':'pelicula modificada'})
        

@app.delete('/movies/{id}',tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id']== id:
            movies.remove(item)
            return JSONResponse(content={'message':'pela eliminada'})