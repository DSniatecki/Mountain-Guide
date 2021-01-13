from typing import Iterable

from .DbExecutor import DbExecutor

ADD_PLANNED_TRIP = "INSERT INTO plannedtrips (name, user_id) VALUES ('{}', {});"
GET_LAST_PLANNED_TRIP_ID = "SELECT currval('plannedtrips_id_seq')"
ADD_PLANNED_TRIP_SECTIONS = "INSERT INTO plannedsections(planned_trip_id, position, section_id) VALUES {}"


class TripsDao:

    def __init__(self, db_executor: DbExecutor):
        self.db_executor = db_executor

    def create_new_planned_trip(self, trip_name: str, section_ids: Iterable[int]) -> None:
        self.db_executor.execute_query(ADD_PLANNED_TRIP.format(trip_name, 1))
        result = self.db_executor.execute_read_query(GET_LAST_PLANNED_TRIP_ID)
        trip_id = result[0][0]
        values = ', '.join([f'({trip_id},{i},{section_id})' for i, section_id in enumerate(section_ids)])
        self.db_executor.execute_query(ADD_PLANNED_TRIP_SECTIONS.format(values))
