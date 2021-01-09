RECEIVE_ALL_RANGES = """
SELECT range.id            as range_id,
       range.name          as range_name,
       range.country       as range_country,
       zone.id             as zone_id,
       zone.name           as zone_name,
       destination.id      as destination_id,
       destination.name    as destination_id,
       destination.height  as destination_height,
       destination.is_open as destination_is_open
FROM ranges range
         JOIN zones zone on range.id = zone.range_id
         JOIN destinations destination on zone.id = destination.zone_id;
"""

RECEIVE_ALL_SECTIONS = """
SELECT * FROM sections;
"""

RECEIVE_ALL_PLANNED_TRIPS = """
SELECT  user.id             as user_id
        user.login          as user_login
        user.email          as user_email
        user.password       as user_password
        user.role           as user_role
        trip.id             as trip_id,
        trip.name           as trip_name,
        section.position    as section_position,
        section.section_id  as section_id
FROM Users user
        JOIN PlannedTrips trip ON user.id = trip.user_id
        JOIN PlannedSections section ON trip.id = section.planned_trip_id
"""
