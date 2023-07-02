# pip install quart quart-schema
# for testing:
# pip install pytest pytest-asyncio
# You can send a request with curl as follows (all these variations work):
#curl -s -X POST -H "Content-Type: application/json" -d "{\"task\":\"learn quart\"}" http://127.0.0.1:5000/echo
#curl -X POST http://127.0.0.1:5000/todos/ -H "content-type: application/json" -d '{"due":"2020-12-08T11:19:35.818445","task":"learn quart"}'
#curl -X POST -H "content-type: application/json" -d '{"due":"2020-12-08T11:19:35.818445","task":"learn quart"}' http://localhost:5000/todos/
#curl -X 'POST'  'http://127.0.0.1:5000/todos/' -H 'accept: application/json'  -H 'Content-Type: application/json'  -d '{
#  "due": "2023-08-02T16:54:08.146Z",
#  "task": "learning quart"
#}'
# get list of todos
#curl -X GET  http://127.0.0.1:5000/todos/
from dataclasses import dataclass
from datetime import datetime
from quart import Quart, request
from quart_schema import QuartSchema, validate_request, validate_response
from typing import List

todos = []

app = Quart(__name__)
QuartSchema(app)

@app.get("/")
async def home():
    return {"endpoints": [{"todos":"/todos"}, {"docs": "/docs"}, {"redocs": "/redocs"}]}

@app.post("/echo")
async def echo():
    print(request.is_json, request.mimetype)
    data = await request.get_json()
    return {"input": data, "extra": True}

@dataclass
class TodoIn:
    task: str
    due: datetime | None

@dataclass
class Todo(TodoIn):
    id: int



@dataclass
class TodoOut:
    todos: List[Todo]

@app.get("/todos/")
@validate_response(TodoOut)
async def get_todos() -> TodoOut:
    return TodoOut(todos=todos)


@app.post("/todos/")
@validate_request(TodoIn)
@validate_response(Todo)
async def create_todo(data: Todo) -> Todo:
    new_todo = Todo(id=len(todos) + 1, task=data.task, due=data.due)
    todos.append(new_todo)
    return new_todo

#def run() -> None:
#    app.run()

if __name__ == "__main__":
    app.run(debug=True)

