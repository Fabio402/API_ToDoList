from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ToDo(BaseModel):
    name: str
    done: bool
    limitTime: Optional[date]

class DataBase:
    toDoList = []

app = FastAPI()

@app.post('/insert')
def add(toDo: ToDo):
    try:
        DataBase.toDoList.append(toDo)
        return{'status': 'sucess'}
    except Exception as e:
        return{'status': 'Error: '+e}

@app.post('/list')
def show(op: int = 0):
    if op == 0:
        return DataBase.toDoList
    elif op == 1:
        return list(filter(lambda data: data.done == False, DataBase.toDoList))
    elif op == 2:
        return list(filter(lambda data: data.done == True, DataBase.toDoList))

@app.post('/edit')
def edit(toDo: ToDo):
    try:
        DataBase.toDoList = list(map(lambda data: toDo if data.name == toDo.name else data, DataBase.toDoList))
        return{'status': 'sucess'}
    except Exception as e:
        return{'status': 'Error: '+e}