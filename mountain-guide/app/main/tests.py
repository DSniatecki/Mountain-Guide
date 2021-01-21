import unittest
from datetime import date

from model.Destination import Destination
from model.PlannedTrip import PlannedTrip
from model.Range import Range
from model.Section import Section
from model.TripBuildingStage import TripBuildingStage
from model.TripSection import TripSection
from model.Zone import Zone
from service.DestinationsService import DestinationsService
from service.RangesService import RangesService
from service.TripsService import TripsService
from service.SectionsService import SectionsService


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
        trip_service = TripsService(ranges_dao, None)

        result = trip_service.create_trip_building_stage([2, 1])

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
        trip_service = TripsService(ranges_dao, None)

        result = trip_service.create_trip_building_stage([1, 2])

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
        trip_service = TripsService(ranges_dao, None)

        result = trip_service.create_trip_building_stage([])

        self.assertEqual(expected_trip_building_stage, result)

    def test_find_trips(self):
        expected_trips = [PlannedTrip(id=1, name='super wycieczka', sections=
        [Section(id=22, name='pierwszy odcinek', gotPoints=3, length=12.3,
                 startDestination=Destination(id=1, name='miejsce 1', height=123.4),
                 endDestination=Destination(id=2, name='miejsce 2', height=321.7)),
         Section(id=23, name='drugi odcinek', gotPoints=5, length=10.9,
                 startDestination=Destination(id=2, name='miejsce 2', height=321.7),
                 endDestination=Destination(id=3, name='miejsce 3', height=500.5))
         ])]

        trips_dao = Mock()
        trips_dao.find_all_planned_trips = lambda: {PlannedTrip(id=1, name='super wycieczka'): [(1, 22), (2, 23)]}
        ranges_dao = Mock()
        ranges_dao.make_sections_map = lambda: {22: Section(id=22, name='pierwszy odcinek', gotPoints=3, length=12.3,
                                                            startDestination=Destination(id=1, name='miejsce 1',
                                                                                         height=123.4),
                                                            endDestination=Destination(id=2, name='miejsce 2',
                                                                                       height=321.7)),
                                                23: Section(id=23, name='drugi odcinek', gotPoints=5, length=10.9,
                                                            startDestination=Destination(id=2, name='miejsce 2',
                                                                                         height=321.7),
                                                            endDestination=Destination(id=3, name='miejsce 3',
                                                                                       height=500.5))}
        trip_service = TripsService(ranges_dao, trips_dao)

        result = trip_service.find_all_trips()

        self.assertEqual(result, expected_trips)

    def test_find_matching_trips(self):
        all_trips = [PlannedTrip(id=1, name='super wycieczka', sections=
        [Section(id=22, name='odcinek22', gotPoints=3, length=12.3,
                 startDestination=Destination(id=1, name='miejsce 1', height=123.4),
                 endDestination=Destination(id=2, name='miejsce 2', height=321.7)),
         Section(id=23, name='odcinek23', gotPoints=5, length=10.9,
                 startDestination=Destination(id=2, name='miejsce 2', height=321.7),
                 endDestination=Destination(id=3, name='miejsce 3', height=500.5))]),
                     PlannedTrip(id=1, name='trasa w miejsce', sections=
                     [Section(id=31, name='odcinek31', gotPoints=3, length=17.3,
                              startDestination=Destination(id=21, name='miejsce 21', height=123.4),
                              endDestination=Destination(id=22, name='miejsce 21', height=321.7)),
                      Section(id=32, name='odcinek32', gotPoints=2, length=8.2,
                              startDestination=Destination(id=23, name='miejsce 23', height=321.7),
                              endDestination=Destination(id=24, name='miejsce 24', height=500.5)),
                      Section(id=33, name='odcinek33', gotPoints=1, length=9.9,
                              startDestination=Destination(id=25, name='miejsce 25', height=321.7),
                              endDestination=Destination(id=26, name='miejsce 26', height=500.5))])]
        expected_result = [PlannedTrip(id=1, name='trasa w miejsce', sections=
        [Section(id=31, name='odcinek31', gotPoints=3, length=17.3,
                 startDestination=Destination(id=21, name='miejsce 21', height=123.4),
                 endDestination=Destination(id=22, name='miejsce 21', height=321.7)),
         Section(id=32, name='odcinek32', gotPoints=2, length=8.2,
                 startDestination=Destination(id=23, name='miejsce 23', height=321.7),
                 endDestination=Destination(id=24, name='miejsce 24', height=500.5)),
         Section(id=33, name='odcinek33', gotPoints=1, length=9.9,
                 startDestination=Destination(id=25, name='miejsce 25', height=321.7),
                 endDestination=Destination(id=26, name='miejsce 26', height=500.5))])]
        trip_service = TripsService(None, None)
        trip_service.find_all_trips = lambda: all_trips

        result = trip_service.find_matching_trips('Miej')

        self.assertEqual(result, expected_result)

    def test_find_matching_trips_no_match(self):
        all_trips = [PlannedTrip(id=1, name='super wycieczka', sections=
        [Section(id=22, name='odcinek22', gotPoints=3, length=12.3,
                 startDestination=Destination(id=1, name='miejsce 1', height=123.4),
                 endDestination=Destination(id=2, name='miejsce 2', height=321.7)),
         Section(id=23, name='odcinek23', gotPoints=5, length=10.9,
                 startDestination=Destination(id=2, name='miejsce 2', height=321.7),
                 endDestination=Destination(id=3, name='miejsce 3', height=500.5))]),
                     PlannedTrip(id=1, name='trasa w miejsce', sections=
                     [Section(id=31, name='odcinek31', gotPoints=3, length=17.3,
                              startDestination=Destination(id=21, name='miejsce 21', height=123.4),
                              endDestination=Destination(id=22, name='miejsce 21', height=321.7)),
                      Section(id=32, name='odcinek32', gotPoints=2, length=8.2,
                              startDestination=Destination(id=23, name='miejsce 23', height=321.7),
                              endDestination=Destination(id=24, name='miejsce 24', height=500.5)),
                      Section(id=33, name='odcinek33', gotPoints=1, length=9.9,
                              startDestination=Destination(id=25, name='miejsce 25', height=321.7),
                              endDestination=Destination(id=26, name='miejsce 26', height=500.5))])]
        expected_result = []
        trip_service = TripsService(None, None)
        trip_service.find_all_trips = lambda: all_trips

        result = trip_service.find_matching_trips('Góry')

        self.assertEqual(result, expected_result)


class SectionsServiceTest(unittest.TestCase):

    def test_add_section_valid(self):
        raw_section_to_add = {'name': 'nowy odcinek', 'got_points': 3, 'length': 12.3,
                              'start_destination': 1, 'end_destination': 2,
                              'is_open': True, 'opening_date': None, 'closing_date': None}
        destinations = [Destination(id=1, name='miejsce 1', height=123.4),
                        Destination(id=2, name='miejsce 2', height=321.7)]
        expected_zone = Zone(id=1, name='zone1', destinations=[Destination(id=1, name='miejsce 1', height=123.4),
                                                               Destination(id=2, name='miejsce 2', height=321.7)],
                             sections=[Section(id=1, name='nowy odcinek', gotPoints=3, length=12.3,
                                               startDestination=Destination(id=1, name='miejsce 1', height=123.4),
                                               endDestination=Destination(id=2, name='miejsce 2', height=321.7))])
        expected_result = (expected_zone, True)
        sections_dao = Mock()
        sections_dao.add_section = lambda section_to_add, zone_id: None
        destination_dao = Mock()
        destination_dao.find_destination = lambda dest_id: destinations[dest_id - 1]
        section_service = SectionsService(sections_dao, destination_dao, None)
        section_service._check_section_is_valid = lambda sec, zone_id: True
        section_service.find_zone_with_sections = lambda zone_id: expected_zone

        result = section_service.add_section(raw_section_to_add, 1)

        self.assertEqual(result, expected_result)

    def test_add_section_invalid_name(self):
        raw_section_to_add = {'name': 'nowy odcinek', 'got_points': 3, 'length': 12.3,
                              'start_destination': 1, 'end_destination': 2,
                              'is_open': True, 'opening_date': None, 'closing_date': None}
        expected_zone = Zone(id=1, name='zone1', destinations=[Destination(id=1, name='miejsce 1', height=123.4),
                                                               Destination(id=2, name='miejsce 2', height=321.7)],
                             sections=[Section(id=1, name='nowy odcinek', gotPoints=5, length=32.1,
                                               startDestination=Destination(id=1, name='miejsce 1', height=123.4),
                                               endDestination=Destination(id=1, name='miejsce 1', height=123.4))])
        expected_result = (expected_zone, False)
        sections_dao = Mock()
        sections_dao.add_section = lambda section_to_add, zone_id: None
        section_service = SectionsService(sections_dao, None, None)
        section_service._check_section_is_valid = lambda sec, zone_id: False
        section_service.find_zone_with_sections = lambda zone_id: expected_zone

        result = section_service.add_section(raw_section_to_add, 1)

        self.assertEqual(result, expected_result)

    def test_add_section_invalid_destination(self):
        raw_section_to_add = {'name': 'nowy odcinek', 'got_points': 3, 'length': 12.3,
                              'start_destination': -1, 'end_destination': -1,
                              'is_open': True, 'opening_date': None, 'closing_date': None}
        expected_zone = Zone(id=1, name='zone1', destinations=[Destination(id=1, name='miejsce 1', height=123.4),
                                                               Destination(id=2, name='miejsce 2', height=321.7)])
        expected_result = (expected_zone, False)
        sections_dao = Mock()
        sections_dao.add_section = lambda section_to_add, zone_id: None
        section_service = SectionsService(sections_dao, None, None)
        section_service._check_section_is_valid = lambda sec, zone_id: False
        section_service.find_zone_with_sections = lambda zone_id: expected_zone

        result = section_service.add_section(raw_section_to_add, 1)

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
