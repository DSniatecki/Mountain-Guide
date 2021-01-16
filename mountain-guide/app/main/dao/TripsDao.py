from typing import Iterable, List
from .DbExecutor import DbExecutor
from model.PlannedTrip import PlannedTrip

ADD_PLANNED_TRIP = "INSERT INTO plannedtrips (name, user_id) VALUES ('{}', {});"
GET_LAST_PLANNED_TRIP_ID = "SELECT currval('plannedtrips_id_seq')"
ADD_PLANNED_TRIP_SECTIONS = "INSERT INTO plannedsections(planned_trip_id, position, section_id) VALUES {}"
RECEIVE_ALL_PLANNED_TRIPS = """
SELECT  trip.id, trip.name, section.position, section.section_id  
FROM plannedtrips trip JOIN plannedsections section ON trip.id = section.planned_trip_id
WHERE trip.user_id = {};
"""


def _create_trip_from_trip_row(trip_row):
    return PlannedTrip(id=trip_row[0], name=trip_row[1])


def _extract_trips_sections_map(rows):
    trips_sections = {}
    for trip_row in rows:
        trip = _create_trip_from_trip_row(trip_row)
        temp_trip = trips_sections.get(trip)
        if temp_trip is None:
            trips_sections[trip] = [(trip_row[2], trip_row[3])]
        else:
            temp_trip.append((trip_row[2], trip_row[3]))
    return trips_sections


class TripsDao:

    def __init__(self, db_executor: DbExecutor):
        self.db_executor = db_executor

    def create_new_planned_trip(self, trip_name: str, section_ids: Iterable[int]) -> None:
        self.db_executor.execute_query(ADD_PLANNED_TRIP.format(trip_name, 1))
        result = self.db_executor.execute_read_query(GET_LAST_PLANNED_TRIP_ID)
        trip_id = result[0][0]
        values = ', '.join([f'({trip_id},{i},{section_id})' for i, section_id in enumerate(section_ids)])
        self.db_executor.execute_query(ADD_PLANNED_TRIP_SECTIONS.format(values))

    def find_all_planned_trips(self):
        result = self.db_executor.execute_read_query(RECEIVE_ALL_PLANNED_TRIPS.format(1))
        return _extract_trips_sections_map(result)
