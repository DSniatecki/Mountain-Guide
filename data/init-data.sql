CREATE TABLE Ranges
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(80) NOT NULL UNIQUE,
    country VARCHAR(80) NOT NULL
);

CREATE TABLE Zones
(
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(80) NOT NULL,
    range_id INT         NOT NULL,
    CONSTRAINT FK_ZoneRange FOREIGN KEY (range_id) REFERENCES Ranges (id)
);


CREATE TABLE Destinations
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(80) NOT NULL,
    zone_id int         NOT NULL,
    height  float,
    is_open boolean     NOT NULL,
    CONSTRAINT FK_DestinationZone FOREIGN KEY (zone_id) REFERENCES Zones (id)
);

CREATE TABLE Sections
(
    id                   SERIAL PRIMARY KEY,
    name                 VARCHAR(80) NOT NULL,
    length               float       NOT NULL,
    got_points           int         NOT NULL,
    zone_id              int         NOT NULL,
    start_destination_id int         NOT NULL,
    end_destination_id   int         NOT NULL,
    is_open              boolean     NOT NULL,
    opening_date         date,
    closure_date         date,
    CONSTRAINT FK_StartZone FOREIGN KEY (zone_id) REFERENCES Zones (id),
    CONSTRAINT FK_SectionStartDestination FOREIGN KEY (start_destination_id) REFERENCES Destinations (id),
    CONSTRAINT FK_SectionEndDestination FOREIGN KEY (end_destination_id) REFERENCES Destinations (id)

);


INSERT INTO Ranges(NAME, COUNTRY)
VALUES ('Tatry', 'Polska'),
       ('Sudety', 'Polska');

INSERT INTO Zones(name, range_id)
VALUES ('Tatry Wysokie', 1),
       ('Tatry Nizinne', 1),
       ('Tatry Niskie', 1),
       ('Sudety wysokie', 2),
       ('Sudety niskie', 2);

INSERT INTO Destinations(name, zone_id, height, is_open)
VALUES ('Schronisko przy Morskim Oku', 1, 1400.24, true),
       ('Schronisko pod Labedziem', 1, 1122.87, true),
       ('Parking przy łące', 1, 921.24, true),
       ('Parking przy Grajdolku', 3, 810.54, true),
       ('Parking pod wodospadem', 2, 995.80, false),
       ('Stare schronisko', 4, 995.80, true);


INSERT INTO Sections(name, length, got_points, zone_id, start_destination_id, end_destination_id, is_open, opening_date)
VALUES ('Z Morskiego Oku dla schroniska pod Labedziem.', 3400.24, 3, 1, 1, 2, true, '2005-01-01'),
       ('Ze schroniska pod Labedziem na parking przy lace', 6300.24, 8, 1, 2, 3, true, '2008-01-01'),
       ('Z parkingu przy łące na Morskie oko.', 2522.24, 2, 1, 3, 1, true, '2010-03-01'),
       ('Z parkingu przy łące na Schronisko pod labedziem.', 7677.24, 9, 1, 3, 2, true, '2006-02-01');