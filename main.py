from fastapi import FastAPI, HTTPException, Body, Path, Query
from pydantic import BaseModel,Field
from typing import Optional,List
from fastapi.responses import HTMLResponse,JSONResponse
from config.database import Session,engine,Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

Base.metadata.create_all(bind=engine)

class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field(min_length=3, max_length=25)
    overview: str
    year: int
    rating: float
    category: str

    class Config:
        schema_extra={
            "example":{
                "id":1,
                "title":"Descripción de la película",
                "year":2022
            }
        }

items = []

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = '0.0.1'

db=Session()

@app.get('/', tags=['Home'])
def root():
    return HTMLResponse('<h1>HOLA</h1>')


@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies()-> List[Movie]:

    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
    

@app.get('/movies/{id}', tags =['movies'])
def get_movie(id:int = Path(ge=1,le=2000)):
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404,content={'message':'sin resultado'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category:str=Query(min_length=5,max_length=15)):
    movies = jsonable_encoder(db.query(MovieModel).all)
    data= [item for item in movies if item['category'] == category]
    return JSONResponse(content=data)


@app.post('/movies', tags=['movies'])
def create_movie(movie :Movie):
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={'message':'se creó'})

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