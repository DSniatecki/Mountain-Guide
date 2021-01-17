from dao.DestinationsDao import DestinationsDao
from dao.RangesDao import RangesDao
from dao.TripsDao import TripsDao
from dao.SectionsDao import SectionsDao
from service.DestinationsService import DestinationsService
from service.RangesService import RangesService
from service.TripsService import TripsService
from service.SectionsService import SectionsService


class ServicesFactory:

    def __init__(self, db_executor):
        self._db_executor = db_executor
        self._ranges_dao = None
        self._trips_dao = None
        self._destinations_dao = None
        self._sections_dao = None
        self._ranges_service = None
        self._trips_service = None
        self._destinations_service = None
        self._sections_service = None

    def create_ranges_service(self) -> RangesService:
        if self._ranges_service is None:
            self._ranges_service = RangesService(self._create_ranges_dao())
        return self._ranges_service

    def create_trips_service(self) -> TripsService:
        if self._trips_service is None:
            self._trips_service = TripsService(self._create_ranges_dao(), self._create_trips_dao())
        return self._trips_service

    def create_destinations_service(self) -> DestinationsService:
        if self._destinations_service is None:
            self._destinations_service = DestinationsService(self._create_destinations_dao())
        return self._destinations_service

    def create_sections_service(self) -> SectionsService:
        if self._sections_service is None:
            self._sections_service = SectionsService(self._create_sections_dao(), self._create_destinations_dao(),
                                                     self._create_ranges_dao())
        return self._sections_service

    def _create_ranges_dao(self) -> RangesDao:
        if self._ranges_dao is None:
            self._ranges_dao = RangesDao(self._db_executor)
        return self._ranges_dao

    def _create_trips_dao(self) -> TripsDao:
        if self._trips_dao is None:
            self._trips_dao = TripsDao(self._db_executor)
        return self._trips_dao

    def _create_destinations_dao(self) -> DestinationsDao:
        if self._destinations_dao is None:
            self._destinations_dao = DestinationsDao(self._db_executor)
        return self._destinations_dao

    def _create_sections_dao(self) -> SectionsDao:
        if self._sections_dao is None:
            self._sections_dao = SectionsDao(self._db_executor)
        return self._sections_dao
