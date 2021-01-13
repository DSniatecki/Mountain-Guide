from .DbExecutor import DbExecutor
from model.Destination import Destination

RECEIVE_DESTINATION_BY_ID = "SELECT * FROM destinations WHERE id = {};"


def create_destination_from_row(dest_tup) -> Destination:
    return Destination(id=dest_tup[0], name=dest_tup[1], height=dest_tup[3], isOpen=dest_tup[4])


UPDATE_DESTINATION_BY_ID = "UPDATE destinations SET name = '{}', height = {}, is_open = {} WHERE id = {};"


class DestinationsDao:

    def __init__(self, db_executor: DbExecutor):
        self.db_executor = db_executor

    def find_destination(self, destination_id: int) -> Destination:
        row = self.db_executor.execute_read_query(RECEIVE_DESTINATION_BY_ID.format(destination_id))
        return create_destination_from_row(row[0])

    def update_destination(self, dest_id: int, dest: Destination) -> None:
        self.db_executor.execute_query(UPDATE_DESTINATION_BY_ID.format(dest.name, dest.height, dest.isOpen, dest_id))
