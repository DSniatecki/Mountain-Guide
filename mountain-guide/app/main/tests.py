import unittest
from datetime import date

from model.Destination import Destination
from model.Range import Range
from model.Section import Section
from model.TripBuildingStage import TripBuildingStage
from model.TripSection import TripSection
from model.Zone import Zone
from service.DestinationsService import DestinationsService
from service.RangesService import RangesService
from service.TripsService import TripsService


class Mock:
    pass


class DestinationServiceTest(unittest.TestCase):

    def test_find_destination(self):
        expected_destination = Destination(id=1, name='super_destination', height=1232.32, isOpen=True)
        destination_dao = Mock()
        destination_dao.find_destination = lambda dest_id: expected_destination
        destination_service = DestinationsService(destination_dao)

        result = destination_service.find_destination(1)

        self.assertEqual(result, expected_destination)

    def test_update_destination(self):
        raw_destination_to_update = {'id': 1, 'name': 'super_destination', 'height': 1232.32, 'isOpen': 'true'}
        destination_dao = Mock()
        expected_destination = Destination(id=1, name='super_destination', height=1232.32, isOpen=True)
        destination_dao.find_destination = lambda dest_id: expected_destination
        destination_dao.update_destination = lambda dest_id, dest: None
        destination_service = DestinationsService(destination_dao)

        result = destination_service.update_destination(1, raw_destination_to_update)

        self.assertEqual(result, expected_destination)


class RangesServiceTest(unittest.TestCase):

    def test_find_all_ranges(self):
        expected_ranges = [
            Range(id=1, name='range1', country='country1', zones=[Zone(id=22, name='zone1')]),
            Range(id=2, name='range2', country='country2',
                  zones=[Zone(id=23, name='zone2.1'), Zone(id=23, name='zone2.2')])
        ]
        ranges_dao = Mock()
        ranges_dao.find_all_ranges = lambda: expected_ranges
        destination_service = RangesService(ranges_dao)

        result = destination_service.find_all_ranges()

        self.assertEqual(result, expected_ranges)


class TripsServiceTest(unittest.TestCase):

    def test_find_trip_sections(self):
        all_ranges = [
            Range(id=1, name='Tatry', country='Polska', zones=[
                Zone(id=1, name='Tatry Wysokie', sections=[
                    Section(
                        id=1, name='name6', gotPoints=4,
                        length=3400.24,
                        startDestination=Destination(id=1, name='name3', height=1400.24),
                        endDestination=Destination(id=2, name='name7', height=1122.87),
                        openingDate=date(2005, 1, 1)
                    ),
                    Section(
                        id=2,
                        name='name1', gotPoints=3, length=2522.24,
                        startDestination=Destination(id=3, name='name2', height=921.24),
                        endDestination=Destination(id=1, name='name3', height=1400.24),
                        openingDate=date(2010, 3, 1)
                    ),
                    Section(
                        id=3, name='name8', gotPoints=10, length=7677.24,
                        startDestination=Destination(id=3, name='name2', height=921.24),
                        endDestination=Destination(id=2, name='name7', height=1122.87),
                        openingDate=date(2006, 2, 1)
                    ),
                    Section(
                        id=4, name='name9', gotPoints=10, length=7677.24,
                        startDestination=Destination(id=2, name='name7', height=1122.87),
                        endDestination=Destination(id=3, name='name2', height=921.24),
                        openingDate=date(2006, 2, 1)
                    ),
                    Section(
                        id=5, name='name4', gotPoints=10, length=7677.24,
                        startDestination=Destination(id=1, name='name3', height=1400.24),
                        endDestination=Destination(id=7, name='name5',
                                                   height=1671.1),
                        openingDate=date(2003, 7, 1)
                    )
                ],
                     destinations=[
                         Destination(id=1, name='name3', height=1400.24),
                         Destination(id=3, name='name2', height=921.24),
                         Destination(id=7, name='name5', height=1671.1),
                         Destination(id=2, name='name7', height=1122.87)
                     ]
                     )])
        ]

        expected_trip_building_stage = TripBuildingStage(
            totalGotPoints=7,
            totalLengthKM=5.92,
            sections=[
                TripSection(id=2, name='name1', country='Polska', rangeName='Tatry', zoneName='Tatry Wysokie',
                            startDestination=Destination(id=3, name='name2', height=921.24),
                            endDestination=Destination(id=1, name='name3', height=1400.24), gotPoints=3,
                            length=2522.24),
                TripSection(id=1, name='name6', country='Polska', rangeName='Tatry', zoneName='Tatry Wysokie',
                            startDestination=Destination(id=1, name='name3', height=1400.24),
                            endDestination=Destination(id=2, name='name7', height=1122.87), gotPoints=4,
                            length=3400.24)
            ], possibleNextSections=[
                TripSection(id=4, name='name9', country='Polska', rangeName='Tatry', zoneName='Tatry Wysokie',
                            startDestination=Destination(id=2, name='name7', height=1122.87),
                            endDestination=Destination(id=3, name='name2', height=921.24), gotPoints=10,
                            length=7677.24)
            ]
        )

        ranges_dao = Mock()
        ranges_dao.find_all_ranges = lambda: all_ranges
        destination_service = TripsService(ranges_dao, None)

        result = destination_service.create_trip_building_stage([2, 1])

        self.assertEqual(expected_trip_building_stage, result)

    def test_find_trip_sections_simple(self):
        all_ranges = [
            Range(id=1, name='Tatry', country='Polska', zones=[
                Zone(id=1, name='Tatry Wysokie', sections=[
                    Section(
                        id=1, name='name6', gotPoints=4,
                        length=3400.24,
                        startDestination=Destination(id=1, name='name3', height=1400.24),
                        endDestination=Destination(id=2, name='name2', height=1122.87),
                        openingDate=date(2005, 1, 1)
                    ),
                    Section(
                        id=2,
                        name='name1', gotPoints=3, length=2522.24,
                        startDestination=Destination(id=2, name='name2', height=1122.87),
                        endDestination=Destination(id=1, name='name3', height=1400.24),
                        openingDate=date(2010, 3, 1)
                    ),
                ],
                     destinations=[
                         Destination(id=1, name='name3', height=1400.24),
                         Destination(id=2, name='name2', height=1122.87)
                     ]
                     )])
        ]

        expected_trip_building_stage = TripBuildingStage(
            totalGotPoints=7,
            totalLengthKM=5.92,
            sections=[
                TripSection(id=1, name='name6', country='Polska', rangeName='Tatry', zoneName='Tatry Wysokie',
                            startDestination=Destination(id=1, name='name3', height=1400.24),
                            endDestination=Destination(id=2, name='name2', height=1122.87), gotPoints=4,
                            length=3400.24),
                TripSection(id=2, name='name1', country='Polska', rangeName='Tatry', zoneName='Tatry Wysokie',
                            startDestination=Destination(id=2, name='name2', height=1122.87),
                            endDestination=Destination(id=1, name='name3', height=1400.24), gotPoints=3,
                            length=2522.24),

            ], possibleNextSections=[
                TripSection(id=1, name='name6', country='Polska', rangeName='Tatry', zoneName='Tatry Wysokie',
                            startDestination=Destination(id=1, name='name3', height=1400.24),
                            endDestination=Destination(id=2, name='name2', height=1122.87), gotPoints=4,
                            length=3400.24)
            ]
        )

        ranges_dao = Mock()
        ranges_dao.find_all_ranges = lambda: all_ranges
        destination_service = TripsService(ranges_dao, None)

        result = destination_service.create_trip_building_stage([1, 2])

        self.assertEqual(expected_trip_building_stage, result)

    def test_find_trip_sections_empty(self):
        all_ranges = []
        expected_trip_building_stage = TripBuildingStage(
            totalGotPoints=0,
            totalLengthKM=0,
            sections=[],
            possibleNextSections=[]
        )
        ranges_dao = Mock()
        ranges_dao.find_all_ranges = lambda: all_ranges
        destination_service = TripsService(ranges_dao, None)

        result = destination_service.create_trip_building_stage([])

        self.assertEqual(expected_trip_building_stage, result)


if __name__ == '__main__':
    unittest.main()
