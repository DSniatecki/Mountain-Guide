from typing import List
from .DbExecutor import DbExecutor
from model.Destination import Destination
from model.Range import Range
from model.Section import Section
from model.Zone import Zone

RECEIVE_ALL_RANGES = """
SELECT r.id, r.name, r.country, z.id, z.name, d.id, d.name, d.height, d.is_open
FROM ranges r
         JOIN zones z on r.id = z.range_id
         JOIN destinations d on z.id = d.zone_id;
"""


def _create_range_from_range_row(range_row):
    return Range(id=range_row[0], name=range_row[1], country=range_row[2])


def _create_destination_from_destination_row(range_row):
    return Destination(id=range_row[5], name=range_row[6], height=range_row[7], isOpen=range_row[8])


def _create_zone_from_zone_row(range_row):
    return Zone(id=range_row[3], name=range_row[4])


RECEIVE_ALL_SECTIONS = "SELECT * FROM sections;"


def _create_section_from_section_row(destinations_map, section_row):
    return Section(
        id=section_row[0],
        name=section_row[1],
        length=section_row[2],
        gotPoints=section_row[3],
        startDestination=destinations_map[section_row[5]],
        endDestination=destinations_map[section_row[6]],
        isOpen=section_row[7],
        openingDate=section_row[8],
        closureDate=section_row[9]
    )


class RangesDao:

    def __init__(self, db_executor: DbExecutor):
        self.db_executor = db_executor

    def find_all_ranges(self) -> List[Range]:
        ranges_r = self.db_executor.execute_read_query(RECEIVE_ALL_RANGES)
        section_r = self.db_executor.execute_read_query(RECEIVE_ALL_SECTIONS)
        range_map, zone_sections = self._extract_zones_ranges_maps(ranges_r, section_r)
        return self._map_maps_to_ranges(range_map, zone_sections)

    def _extract_zones_ranges_maps(self, rows, section_rows):
        destinations_map = {}
        zone_sections = {}
        range_map = {}
        for range_row in rows:
            range = _create_range_from_range_row(range_row)
            zone = _create_zone_from_zone_row(range_row)
            destination = _create_destination_from_destination_row(range_row)
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

        for section_row in section_rows:
            zone_id = section_row[4]
            section = _create_section_from_section_row(destinations_map, section_row)
            existing_zone_sections = zone_sections.get(zone_id)
            if existing_zone_sections is None:
                zone_sections[zone_id] = [section]
            else:
                existing_zone_sections.append(section)

        return range_map, zone_sections

    def _map_maps_to_ranges(self, range_map, zone_sections):
        ranges = []
        for range, zones in range_map.items():
            for zone, destinations in zones.items():
                zone.sections = zone_sections.get(zone.id, [])
                range.zones.append(zone)
                for destination in destinations:
                    zone.destinations.append(destination)
            ranges.append(range)
        return ranges
