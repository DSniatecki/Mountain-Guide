from .DbExecutor import DbExecutor
from model.Section import Section

INSERT_SECTION = "INSERT INTO Sections(name, length, got_points, zone_id, start_destination_id, end_destination_id," \
                 " is_open, opening_date, closure_date ) " \
                 "VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {})"


class SectionsDao:

    def __init__(self, db_executor: DbExecutor):
        self.db_executor = db_executor

    def add_section(self, sec: Section, zone_id: int) -> None:
        if sec.openingDate is None:
            opening_date = "null"
        else:
            opening_date = sec.closureDate.strftime("%Y-%m-%d")
        if sec.closureDate is None:
            closure_date = "null"
        else:
            closure_date = sec.closureDate.strftime("%Y-%m-%d")
        self.db_executor.execute_query(INSERT_SECTION.format(sec.name, sec.length, sec.gotPoints, zone_id,
                                                             sec.startDestination.id, sec.endDestination.id,
                                                             sec.isOpen, opening_date, closure_date))
