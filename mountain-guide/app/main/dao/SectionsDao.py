from .DbExecutor import DbExecutor
from model.Section import Section

INSERT_SECTION = "INSERT INTO Sections(name, length, got_points, zone_id, start_destination_id, end_destination_id," \
                 " is_open, opening_date, closure_date ) " \
                 "VALUES ('{}', {}, {}, {}, {}, {}, {}, {}, {})"

GET_SECTION_DATA = "SELECT name, length, got_points, is_open FROM Sections s WHERE s.zone_id={}"


def _extract_sections_data(section_row):
    section_data = {'name': section_row[0], "length": section_row[1], "got_points": section_row[2],
                    "is_open": section_row[3]}
    return section_data


class SectionsDao:

    def __init__(self, db_executor: DbExecutor):
        self.db_executor = db_executor

    def add_section(self, sec: Section, zone_id: int) -> None:
        if sec.openingDate is None:
            openingDate = 'null'
        else:
            openingDate = '\'' + sec.openingDate.strftime('%Y-%m-%d') + '\''
        if sec.closureDate is None:
            closureDate = 'null'
        else:
            closureDate = '\'' + sec.openingDate.strftime('%Y-%m-%d') + '\''
        self.db_executor.execute_query(INSERT_SECTION.format(sec.name, sec.length, sec.gotPoints, zone_id,
                                                             sec.startDestination.id, sec.endDestination.id,
                                                             sec.isOpen, openingDate, closureDate))

    def get_sections_data_from_zone(self, zone_id: int):
        sections_data = self.db_executor.execute_read_query(GET_SECTION_DATA.format(zone_id))
        sections = []
        for sections_row in sections_data:
            sections.append(_extract_sections_data(sections_row))
        return sections
