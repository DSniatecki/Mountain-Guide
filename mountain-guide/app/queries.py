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

RECEIVE_DESTINATION_BY_ID = "SELECT * FROM destinations WHERE id = {};"

UPDATE_DESTINATION_BY_ID = """
UPDATE destinations
SET name = '{}',
    height = {},
    is_open = {}
WHERE id = {};
"""

RECEIVE_ALL_USERS = """
SELECT  myuser.id             as user_id,
        myuser.login          as user_login,
        myuser.email          as user_email,
        myuser.password       as user_password,
        myuser.role           as user_role,
        trip.id             as trip_id,
        trip.name           as trip_name,
        section.position    as section_position,
        section.section_id  as section_id
FROM users myuser
        JOIN plannedtrips trip ON myuser.id = trip.user_id
        JOIN plannedsections section ON trip.id = section.planned_trip_id;
"""
