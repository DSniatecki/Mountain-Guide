import json
import time
from typing import List, Iterable
import psycopg2
import logging
from queries import RECEIVE_ALL_RANGES, RECEIVE_ALL_SECTIONS, RECEIVE_DESTINATION_BY_ID, UPDATE_DESTINATION_BY_ID, \
    RECEIVE_ALL_USERS, ADD_PLANNED_TOUR, GET_LAST_PLANNED_TOUR_ID, ADD_PLANNED_TOUR_SECTIONS
from model.Destination import Destination
from model.Range import Range
from model.Section import Section
from model.Zone import Zone
from model.TourSection import TourSection
from model.PlannedTrip import PlannedTrip
from model.User import User


def execute_query(connection, query):
    read_start = time.time()
    cursor = connection.cursor()
    logging.info(f'Executing query: {query} ...')
    try:
        cursor.execute(query)
        connection.commit()
        read_time = time.time() - read_start
        logging.info(f'DB operation completed. Operation time: {round(read_time, 4)} seconds.')
    except Exception as e:
        logging.error(f'The error: {e} occurred')
        raise e


def execute_read_query(connection, query):
    read_start = time.time()
    cursor = connection.cursor()
    logging.info(f'Executing query: {query} ...')
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        read_time = time.time() - read_start
        logging.info(f'Read operation completed. Number of rows: {len(result)}. '
                     f'Operation time: {round(read_time, 4)} seconds.')
        return result
    except Exception as e:
        logging.error(f'The error: {e} occurred')
        connection.commit()
        raise e


def read_from_file(file_name):
    with open(file_name) as file:
        return file.read()


class DataAccessObject:

    def __init__(self, db_config_file_path):
        conf = json.loads(read_from_file(db_config_file_path))
        while True:
            conn = psycopg2.connect(
                database=conf['dbname'],
                user=conf['user'],
                password=conf['password'],
                host=conf['host'],
                port=conf['port'],
            )
            cur = conn.cursor()
            try:
                cur.execute('select 1;')
            except psycopg2.OperationalError:
                continue
            self.db_connector = conn
            break
        logging.info('Connection to PostgreSQL DB was successfully established')

    def find_tour_sections(self, section_ids: Iterable[int]) -> (List[TourSection], List[TourSection]):
        all_ranges = self.find_all_ranges()
        possible_next_tour_sections = []
        tour_sections = {}
        for range in all_ranges:
            for zone in range.zones:
                for section in zone.sections:
                    if section.id in section_ids:
                        tourSection = TourSection(
                            id=section.id,
                            name=section.name,
                            country=range.country,
                            rangeName=range.name,
                            zoneName=zone.name,
                            startDestination=section.startDestination,
                            endDestination=section.endDestination,
                            gotPoints=section.gotPoints,
                            length=section.length,
                            isOpen=section.isOpen
                        )
                        tour_sections[section.id] = tourSection
        all_tour_sections = []
        for section_id in section_ids:
            all_tour_sections.append(tour_sections[section_id])

        last_tour_section = all_tour_sections[-1]
        final_destination = last_tour_section.endDestination
        for range in all_ranges:
            for zone in range.zones:
                for section in zone.sections:
                    if section.startDestination.id == final_destination.id:
                        tourSection = TourSection(
                            id=section.id,
                            name=section.name,
                            country=range.country,
                            rangeName=range.name,
                            zoneName=zone.name,
                            startDestination=section.startDestination,
                            endDestination=section.endDestination,
                            gotPoints=section.gotPoints,
                            length=section.length,
                            isOpen=section.isOpen
                        )
                        possible_next_tour_sections.append(tourSection)

        return (all_tour_sections, possible_next_tour_sections)

    def find_destination(self, destination_id: int) -> Destination:
        query = RECEIVE_DESTINATION_BY_ID.format(destination_id)
        row = execute_read_query(self.db_connector, query)
        dest_tup = row[0]
        return Destination(id=dest_tup[0], name=dest_tup[1], height=dest_tup[3], isOpen=dest_tup[4])

    def update_destination(self, dest_id: int, dest: Destination) -> Destination:
        update_query = UPDATE_DESTINATION_BY_ID.format(dest.name, dest.height, dest.isOpen, dest_id)
        execute_query(self.db_connector, update_query)
        return self.find_destination(dest_id)

    def save_tour(self, tour_name: str, section_ids: Iterable[int]) -> None:
        execute_query(self.db_connector, ADD_PLANNED_TOUR.format(tour_name, 1))
        result = execute_read_query(self.db_connector, GET_LAST_PLANNED_TOUR_ID)
        tour_id = result[0][0]
        values = ', '.join([f'({tour_id},{i},{section_id})' for i, section_id in enumerate(section_ids)])
        execute_query(self.db_connector, ADD_PLANNED_TOUR_SECTIONS.format(values))

    def find_all_ranges(self) -> List[Range]:
        rows = execute_read_query(self.db_connector, RECEIVE_ALL_RANGES)
        destinations_map = {}
        zone_sections = {}
        range_map = {}
        for range_row in rows:
            range = Range(id=range_row[0], name=range_row[1], country=range_row[2])
            zone = Zone(id=range_row[3], name=range_row[4])
            destination = Destination(id=range_row[5], name=range_row[6], height=range_row[7], isOpen=range_row[8])
            destinations_map[destination.id] = destination
            temp_range = range_map.get(range)
            if temp_range is None:
                range_map[range] = {zone: [destination]}
            else:
                temp_zone = temp_range.get(zone)
                if temp_zone is None:
                    range_map[range][zone] = [destination]
                else:
                    temp_zone.append(destination)

        section_rows = execute_read_query(self.db_connector, RECEIVE_ALL_SECTIONS)
        for section_row in section_rows:
            zone_id = section_row[4]
            section = Section(id=section_row[0],
                              name=section_row[1],
                              length=section_row[2],
                              gotPoints=section_row[3],
                              startDestination=destinations_map[section_row[5]],
                              endDestination=destinations_map[section_row[6]],
                              isOpen=section_row[7],
                              openingDate=section_row[8],
                              closureDate=section_row[9])
            existing_zone_sections = zone_sections.get(zone_id)
            if existing_zone_sections is None:
                zone_sections[zone_id] = [section]
            else:
                existing_zone_sections.append(section)

        ranges = []
        for range, zones in range_map.items():
            for zone, destinations in zones.items():
                zone.sections = zone_sections.get(zone.id, [])
                range.zones.append(zone)
                for destination in destinations:
                    zone.destinations.append(destination)
            ranges.append(range)

        return ranges

    def find_all_users(self) -> List[User]:
        rows = execute_read_query(self.db_connector, RECEIVE_ALL_USERS)
        users_map = {}
        for trip_row in rows:
            user = User(id=trip_row[0], login=trip_row[1], email=trip_row[2], password=trip_row[3], role=trip_row[4])
            trip = PlannedTrip(id=trip_row[5], name=trip_row[6])

            temp_user = users_map.get(user)
            if temp_user is None:
                users_map[user] = {trip: [(trip_row[7], trip_row[8])]}
            else:
                temp_trip = temp_user.get(trip)
                if temp_trip is None:
                    users_map[user][trip] = [(trip_row[7], trip_row[8])]
                else:
                    temp_trip.append((trip_row[7], trip_row[8]))

        ranges = self.find_all_ranges()
        section_map = {}
        for range in ranges:
            for zone in range.zones:
                for section in zone.sections:
                    section_map[section.id] = section

        users = []
        for user, trips in users_map.items():
            for trip, planned_sections in trips.items():
                planned_sections.sort(key=lambda x: x[0])
                for planned_section in planned_sections:
                    trip.sections.append(section_map[planned_section[1]])
                user.plannedTrips.append(trip)
            users.append(user)

        return users
