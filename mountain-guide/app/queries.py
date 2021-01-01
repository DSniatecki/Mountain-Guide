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
