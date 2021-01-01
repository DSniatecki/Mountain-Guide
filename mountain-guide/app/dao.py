import json
import time
from typing import List

import psycopg2
import logging
from queries import RECEIVE_ALL_RANGES, RECEIVE_ALL_SECTIONS
from model.Destination import Destination
from model.Range import Range
from model.Section import Section
from model.Zone import Zone


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
        raise e


def read_from_file(file_name):
    with open(file_name) as file:
        return file.read()


class DataAccessObject:

    def __init__(self, db_config_file_path):
        conf = json.loads(read_from_file(db_config_file_path))
        self.db_connector = psycopg2.connect(
            database=conf['dbname'],
            user=conf['user'],
            password=conf['password'],
            host=conf['host'],
            port=conf['port'],
        )
        logging.info('Connection to PostgreSQL DB was successfully established')

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
