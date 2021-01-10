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
    length               float,
    got_points           float       NOT NULL,
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

CREATE TABLE Users
(
    id          SERIAL PRIMARY KEY,
    login       VARCHAR(80) NOT NULL UNIQUE,
    email       VARCHAR(80) NOT NULL UNIQUE,
    password    VARCHAR(80) NOT NULL,
    role        VARCHAR(30) NOT NULL
);

CREATE TABLE PlannedTrips
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(80) NOT NULL,
    user_id     INT         NOT NULL,
    CONSTRAINT FK_PlannedTripUser FOREIGN KEY (user_id) REFERENCES Users (id)
);

CREATE TABLE PlannedSections
(
    planned_trip_id INT NOT NULL,
    position        INT NOT NULL,
    section_id      INT NOT NULL,
    CONSTRAINT FK_PlannedSectionTrip FOREIGN KEY (planned_trip_id) REFERENCES PlannedTrips (id),
    CONSTRAINT FK_PlannedSectionSection FOREIGN KEY (section_id) REFERENCES Sections (id),
    PRIMARY KEY (planned_trip_id, position)
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
       ('Stare schronisko', 4, 995.80, true),
       ('Schronisko w Dolinie Pięciu Stawów Polskich', 1, 1671.10, true);

INSERT INTO Sections(name, length, got_points, zone_id, start_destination_id, end_destination_id, is_open, opening_date)
VALUES ('Z Morskiego Oka do schroniska pod Labedziem.', 3400.24, 3.5, 1, 1, 2, true, '2005-01-01'),
       ('Z parkingu przy łące na Morskie oko.', 2522.24, 2.5, 1, 3, 1, true, '2010-03-01'),
       ('Z parkingu przy łące na Schronisko pod labedziem.', 7677.24, 9.5, 1, 3, 2, true, '2006-02-01'),
       ('Ze Schroniska pod labedziem do parkingu przy łące.', 7677.24, 9.5, 1, 2, 3, true, '2006-02-01'),
       ('Z Morskiego Oka do Doliny Pięciu Stawów Polskich.', 7677.24, 9.5, 1, 1, 7, true, '2003-07-01');

INSERT INTO Users(login, email, password, role)
VALUES ('adam123', 'great_email@gmail.com', '21b72c0b7adc5c7b4a50ffcb90d92dd6', 'użytkownik'),
       ('magda_789', 'madzia89@gmail.com', '5b9a8069d33fe9812dc8310ebff0a315', 'użytkownik');

INSERT INTO PlannedTrips(name, user_id)
VALUES ('Super wycieczka', 1),
       ('Bardzo krótka wycieczka', 1),
       ('Wycieczka na Morskie Oko', 2);

INSERT INTO PlannedSections(planned_trip_id, position, section_id)
VALUES (1, 1, 2),
       (1, 2, 5),
       (2, 1, 3),
       (3, 1, 2),
       (3, 2, 1),
       (3, 3, 4);

