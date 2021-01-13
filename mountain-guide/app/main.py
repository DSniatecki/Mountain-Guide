from typing import List
import uvicorn
from dao import DataAccessObject
from fastapi import FastAPI, Request, Form
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from model.User import User
from model.Range import Range
from model.Destination import Destination
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
dao = DataAccessObject('../dbconfig.json')


@app.get('/', response_class=HTMLResponse)
def receive_main_page(request: Request):
    ranges = dao.find_all_ranges()
    return templates.TemplateResponse(name='main-page.html', context={'request': request, 'ranges': ranges})


@app.get('/destination/{destination_id}', response_class=HTMLResponse)
def receive_main_page(request: Request, destination_id: int, ):
    destination = dao.find_destination(destination_id)
    return templates.TemplateResponse(name='edit-destination-page.html',
                                      context={'request': request, 'destination': destination})


@app.post('/destination/{destination_id}', response_class=HTMLResponse)
def receive_main_page(request: Request,
                      destination_id: int,
                      name: str = Form('name'),
                      height: float = Form('height'),
                      isOpen: str = Form('isOpen')):
    destination_to_update = Destination(id=destination_id, name=name, height=height, isOpen=(isOpen == 'true'))
    updated_destination = dao.update_destination(destination_id, destination_to_update)
    return templates.TemplateResponse(name='edit-destination-page.html',
                                      context={'request': request, 'destination': updated_destination,
                                               'wasUpdated': True})


class CurrentTour(BaseModel):
    lengthKM: float
    gotPoints: int


@app.get('/tour/{raw_sections_ids}', response_class=HTMLResponse)
def receive_main_page(request: Request, raw_sections_ids: str):
    section_ids = [int(section) for section in raw_sections_ids.split(",")]
    current_tour_sections, possible_next_tour_sections = dao.find_tour_sections(section_ids)
    current_tour = CurrentTour(lengthKM=0.0, gotPoints=0)
    for current_tour_section in current_tour_sections:
        current_tour.lengthKM += (current_tour_section.length / 1000.0)
        current_tour.gotPoints += current_tour_section.gotPoints

    current_tour.lengthKM = round(current_tour.lengthKM, 2)

    return templates.TemplateResponse(name='tour-creator-page.html',
                                      context={'request': request,
                                               'currentTourSections': current_tour_sections,
                                               'possibleNextTourSections': possible_next_tour_sections,
                                               'currentTour': current_tour,
                                               'currentTourSectionIds': raw_sections_ids,
                                               'tourSectionIdsWithoutLast': ','.join([str(x) for x in section_ids[:-1]])
                                               })


@app.post('/save/tour/{raw_sections_ids}', response_class=HTMLResponse)
def receive_main_page(request: Request, raw_sections_ids: str, tour_name: str = Form('name')):
    section_ids = [int(raw_sections_ids.split(",")[0])]
    dao.save_tour(tour_name, section_ids)
    current_tour_sections, possible_next_tour_sections = dao.find_tour_sections(section_ids)
    current_tour = CurrentTour(lengthKM=round((current_tour_sections[0].length / 1000.0), 2),
                               gotPoints=current_tour_sections[0].gotPoints)
    return templates.TemplateResponse(name='tour-creator-page.html',
                                      context={'request': request,
                                               'currentTourSections': section_ids,
                                               'possibleNextTourSections': possible_next_tour_sections,
                                               'currentTour': current_tour,
                                               'wasSaved': True,
                                               'currentTourSectionIds': section_ids[0]
                                               })


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
