import json

import uvicorn
from dao.DbExecutor import DbExecutor
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ServicesFactory import ServicesFactory

with open('../../dbconfig.json') as file:
    db_config = json.loads(file.read())

services_factory = ServicesFactory(DbExecutor(db_config))

ranges_service = services_factory.create_ranges_service()
trips_service = services_factory.create_trips_service()
destinations_service = services_factory.create_destinations_service()

app = FastAPI()
app.mount("/static", StaticFiles(directory="../resources/images/"), name="static")
templates = Jinja2Templates(directory="../resources/templates/")


@app.get('/', response_class=HTMLResponse)
def receive_main_page(request: Request):
    ranges = ranges_service.find_all_ranges()
    return templates.TemplateResponse(name='main-page.html', context={'request': request, 'ranges': ranges})


@app.get('/destination/{destination_id}', response_class=HTMLResponse)
def receive_main_page(request: Request, destination_id: int, ):
    destination = destinations_service.find_destination(destination_id)
    context = {'request': request, 'destination': destination}
    return templates.TemplateResponse(name='edit-destination-page.html', context=context)


@app.post('/destination/{destination_id}', response_class=HTMLResponse)
def receive_main_page(request: Request,
                      destination_id: int,
                      name: str = Form('name'),
                      height: float = Form('height'),
                      isOpen: str = Form('isOpen')):
    dest = destinations_service.update_destination(destination_id, {'name': name, 'height': height, 'isOpen': isOpen})
    context = {'request': request, 'destination': dest, 'wasUpdated': True}
    return templates.TemplateResponse(name='edit-destination-page.html', context=context)


@app.get('/trip/{raw_sections_ids}', response_class=HTMLResponse)
def receive_main_page(request: Request, raw_sections_ids: str):
    section_ids = [int(section) for section in raw_sections_ids.split(",")]
    trip_building_stage = trips_service.create_trip_building_stage(section_ids)
    context = {'request': request,
               'tripBuildingStage': trip_building_stage,
               'currentTripSectionIds': raw_sections_ids,
               'tripSectionIdsWithoutLast': ','.join([str(x) for x in section_ids[:-1]])
               }
    return templates.TemplateResponse(name='trip-creator-page.html',
                                      context=context)


@app.post('/save/trip/{raw_sections_ids}', response_class=HTMLResponse)
def receive_main_page(request: Request, raw_sections_ids: str, trip_name: str = Form('trip_name')):
    section_ids = [int(section) for section in raw_sections_ids.split(",")]
    trips_service.create_new_planned_trip(trip_name, section_ids)
    trip_building_stage = trips_service.create_trip_building_stage(section_ids)
    context = {'request': request,
               'tripBuildingStage': trip_building_stage,
               'wasSaved': True,
               'currentTripSectionIds': raw_sections_ids,
               'tripSectionIdsWithoutLast': ','.join([str(x) for x in section_ids[:-1]])
               }
    return templates.TemplateResponse(name='trip-creator-page.html', context=context)


@app.get('/add-section', response_class=HTMLResponse)
def receive_add_section_page(request: Request):
    ranges = ranges_service.find_all_ranges()
    return templates.TemplateResponse(name='add-section-page.html', context={'request': request, 'ranges': ranges})


# @app.get('/planned-trips', response_class=HTMLResponse)
# def receive_planned_trips(request: Request):
# TODO - Ustaliliśmy, że jeden user więc raczej to jest już niepotrzebne
# users = ranges_dao.find_all_users()
# ret_user = users[0]
# for user in users:
#     if user.id == request.query_params['id']:
#         ret_user = user
# return templates.TemplateResponse(name='planned-trips-page.html', context={'request': request, 'user': ret_user})

@app.exception_handler(404)
def custom_http_exception_handler(request, exc):
    return templates.TemplateResponse(name='error-page.html', context={'request': request})


@app.exception_handler(Exception)
def validation_exception_handler(request, exc):
    return templates.TemplateResponse(name='error-page.html', context={'request': request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
