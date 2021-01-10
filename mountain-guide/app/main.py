from typing import List
import uvicorn
from dao import DataAccessObject
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from model.User import User
from model.Range import Range

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
dao = DataAccessObject('../dbconfig.json')


@app.get('/', response_class=HTMLResponse)
def receive_main_page(request: Request):
    ranges = dao.find_all_ranges()
    return templates.TemplateResponse(name='main-page.html', context={'request': request, 'ranges': ranges})


@app.get('/login', response_class=HTMLResponse)
def receive_login_page(request: Request):
    return templates.TemplateResponse(name='log-in-page.html', context={'request': request})


@app.get('/add-section', response_class=HTMLResponse)
def receive_add_section_page(request: Request):
    ranges = dao.find_all_ranges()
    return templates.TemplateResponse(name='add-section-page.html', context={'request': request, 'ranges': ranges})


@app.get('/planned-trips', response_class=HTMLResponse)
def receive_planned_trips(request: Request):
    users = dao.find_all_users()
    ret_user = users[0]
    for user in users:
        if user.id == request.query_params['id']:
            ret_user = user
    return templates.TemplateResponse(name='planned-trips-page.html', context={'request': request, 'user': ret_user})


@app.get('/api/ranges', response_model=List[Range])
def get_all_ranges() -> List[Range]:
    return dao.find_all_ranges()


@app.get('/api/users', response_model=List[User])
def get_all_users() -> List[User]:
    return dao.find_all_users()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        content=jsonable_encoder({"errorType": "ValidationError", "messages": exc.errors()}),
        status_code=400
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

# @app.get("/items")
# def get_items():
#     return list(items.values())
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: str) -> Item:
#     return items[item_id]
#
#
# @app.post("/items")
# def add_item(item: Item) -> Item:
#     items[str(uuid.uuid1())] = item
#     return item
#
#
# @app.put("/items/{item_id}")
# def update_item(item_id: str, item: Item) -> Item:
#     items[item_id] = item
#     return item
#
