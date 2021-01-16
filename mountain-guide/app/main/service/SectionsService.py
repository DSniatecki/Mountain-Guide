from dao.SectionsDao import SectionsDao
from dao.RangesDao import RangesDao

from model.Destination import Destination
from model.Section import Section


class SectionsService:

    def __init__(self, sections_dao: SectionsDao, ranges_dao: RangesDao):
        self.sections_dao = sections_dao
        self.ranges_dao = ranges_dao

    def add_section(self):
        # TODO
        pass

    def find_zone_with_sections(self, zone_id: int):
        ranges = self.ranges_dao.find_all_ranges()
        for range in ranges:
            for zone in range.zones:
                if zone.id == zone_id:
                    return zone
