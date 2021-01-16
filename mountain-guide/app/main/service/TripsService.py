from typing import List, Iterable
from dao.RangesDao import RangesDao
from dao.TripsDao import TripsDao
from model.Destination import Destination
from model.Range import Range
from model.Section import Section
from model.Zone import Zone
from model.PlannedTrip import PlannedTrip
from model.TripSection import TripSection
from model.TripBuildingStage import TripBuildingStage


def create_trip_section(range: Range, section: Section, zone: Zone) -> TripSection:
    return TripSection(
        id=section.id,
        name=section.name,
        country=range.country,
        rangeName=range.name,
        zoneName=zone.name,
        startDestination=section.startDestination,
        endDestination=section.endDestination,
        gotPoints=section.gotPoints,
        length=section.length,
        isOpen=section.isOpen
    )


class TripsService:

    def __init__(self, ranges_dao: RangesDao, trips_dao: TripsDao):
        self.ranges_dao = ranges_dao
        self.trips_dao = trips_dao

    def create_new_planned_trip(self, trip_name: str, trip_section_ids: List[int]) -> None:
        self.trips_dao.create_new_planned_trip(trip_name, trip_section_ids)

    def create_trip_building_stage(self, section_ids: Iterable[int]) -> TripBuildingStage:
        sections, possible_next_sections = self._find_trip_sections(section_ids)
        total_trip_length_KM = 0.0
        total_trip_got_points = 0
        for current_Trip_section in sections:
            total_trip_length_KM += (current_Trip_section.length / 1000.0)
            total_trip_got_points += current_Trip_section.gotPoints
        total_trip_length_KM = round(total_trip_length_KM, 2)
        return TripBuildingStage(totalGotPoints=total_trip_got_points, totalLengthKM=total_trip_length_KM,
                                 sections=sections, possibleNextSections=possible_next_sections)

    def _find_trip_sections(self, section_ids: Iterable[int]) -> (List[TripSection], List[TripSection]):
        all_ranges = self.ranges_dao.find_all_ranges()
        possible_next_trip_sections = []
        trip_sections = {}
        for range in all_ranges:
            for zone in range.zones:
                for section in zone.sections:
                    if section.id in section_ids:
                        trip_sections[section.id] = create_trip_section(range, section, zone)
        all_trips_sections = []
        for section_id in section_ids:
            all_trips_sections.append(trip_sections[section_id])

        if len(all_trips_sections) > 0:
            last_trip_section = all_trips_sections[-1]
            final_destination = last_trip_section.endDestination
            for range in all_ranges:
                for zone in range.zones:
                    for section in zone.sections:
                        if section.startDestination.id == final_destination.id:
                            trip_section = create_trip_section(range, section, zone)
                            possible_next_trip_sections.append(trip_section)
        return all_trips_sections, possible_next_trip_sections

    def find_all_trips(self) -> List[PlannedTrip]:
        trip_sections = self.trips_dao.find_all_planned_trips()
        section_map = self.ranges_dao.make_sections_map()
        trips = []
        for trip, planned_sections in trip_sections.items():
            planned_sections.sort(key=lambda x: x[0])
            for planned_section in planned_sections:
                trip.sections.append(section_map[planned_section[1]])
            trips.append(trip)
        return trips

    def get_all_trips_data(self, trips) -> {PlannedTrip: (Destination, Destination, int, float)}:
        data = {}
        for trip in trips:
            data[trip] = self._get_trip_data(trip)
        return data

    def _get_trip_data(self, plannedtrip) -> (Destination, Destination, int, float):
        length = 0
        gotpoints = 0
        for section in plannedtrip.sections:
            length += section.length
            gotpoints += section.gotPoints
        return plannedtrip.sections[0].startDestination.name, plannedtrip.sections[
            -1].endDestination.name, gotpoints, length

    def find_matching_trips(self, search_pattern) -> List[PlannedTrip]:
        trips = self.find_all_trips()
        if len(search_pattern) == 0:
            return trips
        matching_trips = []
        for trip in trips:
            if trip.name.lower().find(search_pattern.lower()) != -1:
                matching_trips.append(trip)
        return matching_trips
