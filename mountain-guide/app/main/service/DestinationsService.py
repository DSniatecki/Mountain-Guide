from dao.DestinationsDao import DestinationsDao

from model.Destination import Destination


class DestinationsService:

    def __init__(self, destinations_dao: DestinationsDao):
        self.destinations_dao = destinations_dao

    def update_destination(self, dest_id: int, dest: {}) -> Destination:
        is_dest_open = (dest['isOpen'] == 'true')
        dest_to_update = Destination(id=dest_id, name=dest['name'], height=dest['height'], isOpen=is_dest_open)
        self.destinations_dao.update_destination(dest_id, dest_to_update)
        return self.find_destination(dest_id)

    def find_destination(self, dest_id: int) -> Destination:
        return self.destinations_dao.find_destination(dest_id)
