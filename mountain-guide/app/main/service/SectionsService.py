from datetime import date

from dao.SectionsDao import SectionsDao
from dao.DestinationsDao import DestinationsDao
from dao.RangesDao import RangesDao

from model.Section import Section


class SectionsService:

    def __init__(self, sections_dao: SectionsDao, destinations_dao: DestinationsDao, ranges_dao: RangesDao):
        self.sections_dao = sections_dao
        self.destinations_dao = destinations_dao
        self.ranges_dao = ranges_dao

    def add_section(self, sec: {}, zone_id: int):
        is_valid = self._check_section_is_valid(sec, zone_id)
        if is_valid:
            opening_date = sec['opening_date']
            if type(sec['opening_date']) != date:
                opening_date = None
            closing_date = sec['closing_date']
            if type(sec['closing_date']) != date:
                closing_date = None
            is_sec_open = (sec['is_open'] == 'true')
            section_to_add = Section(id=0,
                                     name=sec['name'],
                                     length=sec['length'],
                                     gotPoints=sec['got_points'],
                                     startDestination=self.destinations_dao.find_destination(
                                         sec['start_destination']),
                                     endDestination=self.destinations_dao.find_destination(
                                         sec['end_destination']),
                                     isOpen=is_sec_open,
                                     openingDate=opening_date,
                                     closureDate=closing_date)
            self.sections_dao.add_section(section_to_add, zone_id)
        return self.find_zone_with_sections(zone_id), is_valid

    def _check_section_is_valid(self, sec: {}, zone_id: int):
        is_valid = True
        if sec['start_destination'] == -1 or sec['end_destination'] == -1:
            is_valid = False
        else:
            zone_sections = self.sections_dao.get_sections_data_from_zone(zone_id)
            for section in zone_sections:
                if section['name'].lower() == sec['name'].lower() and section['is_open']:
                    is_valid = False
        return is_valid

    def find_zone_with_sections(self, zone_id: int):
        ranges = self.ranges_dao.find_all_ranges()
        for range in ranges:
            for zone in range.zones:
                if zone.id == zone_id:
                    return zone
