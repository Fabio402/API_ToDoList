from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ToDo(BaseModel):
    name: str
    done: bool
    limit_time: Optional[date]

class DataBase:
    to_do_list = []

app = FastAPI()

@app.post('/insert')
def add(to_do: ToDo):
    try:
        DataBase.to_do_list.append(to_do)
        return{'status': 'sucess'}
    except Exception as e:
        return{'status': 'Error: '+e}

@app.post('/edit')
def edit(to_do: ToDo):
    try:
        DataBase.to_do_list = list(map(lambda data: to_do if data.name == to_do.name else data, DataBase.to_do_list))
        return{'status': 'sucess'}
    except Exception as e:
        return{'status': 'Error: '+e}

@app.post('/delete')
def delete(id: int):
    try:
        DataBase.to_do_list.pop(id)
    except Exception as e:
        return{'status: Error'+e}

@app.post('/list')
def show(op: int = 0):
    if op == 0:
        return DataBase.to_do_list
    elif op == 1:
        return list(filter(lambda data: data.done == False, DataBase.to_do_list))
    elif op == 2:
        return list(filter(lambda data: data.done == True, DataBase.to_do_list))

