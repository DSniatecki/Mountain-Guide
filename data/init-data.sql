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

CREATE TABLE Users
(
    id       SERIAL PRIMARY KEY,
    login    VARCHAR(80) NOT NULL UNIQUE,
    email    VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(80) NOT NULL,
    role     VARCHAR(30) NOT NULL
);

CREATE TABLE PlannedTrips
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(80) NOT NULL,
    user_id INT         NOT NULL,
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
       ('Tatry Słowackie', 'Słowacja'),
       ('Beskidy Zachodnie', 'Polska'),
       ('Beskidy Wschodnie', 'Polska'),
       ('Góry Świętokrzyskie', 'Polska'),
       ('Sudety', 'Polska');


INSERT INTO Zones(name, range_id)
VALUES ('Tatry Wysokie', 1),
       ('Tatry Zachodnie', 1),
       ('Podtatrze', 1),
       ('Zapadne Tatry', 2),
       ('Vysoke Tatry', 2),
       ('Beskid Śląski', 3),
       ('Beskid Żywiecki', 3),
       ('Beskid Mały', 3),
       ('Beskid Średni', 3),
       ('Podgórze Ciężkowickie', 4),
       ('Bieszczady', 4),
       ('Góry Świętokrzyskie', 5),
       ('Góry Izerskie', 6),
       ('Karkonosze', 6),
       ('Góry Kamienne', 6),
       ('Góry Złote', 6),
       ('Góry Opawskie', 6);

INSERT INTO Destinations(name, zone_id, height, is_open)
VALUES ('Rusinowa polana', 1, 1170, true),
        ('Dolina Filipka', 1, 513, true),
        ('Wierch Porońca', 1, 1036, true),
        ('Palenica Białczańska', 1, 611, true),
        ('Polana pod Wołoszynem', 1, 1320, true),
        ('Łysa Polana', 1, 613, true),
        ('Gęsia Szyja', 1, 1489, true),
        ('Równień Waksmundzka', 1, 533, true),
        ('Czerwony Staw w Dolinie Pańszczyzny', 1, 691, true),
        ('Schronisko PTTK na Hali Gąsienicowej', 1, 1201, true),
        ('Psia Trawka', 1, 610, true),
        ('Brzeziny', 3, 1209, true),
        ('Wodogrzmoty Mickiewicza', 1, 1300, true),
        ('Schronisko PTTK w Roztoce', 1, 721.8, true),
        ('Schronisko PTTK nad Morskim Okiem', 1, 1410, true),
        ('Czarny Staw nad Morskim Okiem', 1, 1583, true),
        ('Rysy', 1, 2499, true),
        ('Polana Biały Potok', 2, 981.5, true),
        ('Trzydniowiański Wierch', 2, 1758, true),
        ('Kasprowy Wierch', 2, 1987, true),
        ('Przełęcz Liliowe', 2, 1952, true),
        ('Palenica Kościeliska', 3, 1183.3, true);

INSERT INTO Sections(name, length, got_points, zone_id, start_destination_id, end_destination_id, is_open, opening_date, closure_date)
VALUES ('Z Dolin Filipka na Rusinową Polanę', 64.24, 6, 1, 2, 1, true, '2005-01-01', null),
       ('Z Rusinowej Polany do Dolin Filipka', 22.24, 3, 1, 1, 2, true, '2010-03-01', null),
       ('Z Wierchu Porońca na Rusinową Polanę', 72.09, 6, 1, 1, 3, true, '2010-03-01', null),
       ('Z Rusinowej Polany na Wierch Porońca', 22.24, 4, 1, 3, 1, true, '1990-06-21', null),
       ('Z Palenicy Białczańskiej na Rusinową Polanę', 252.4, 4, 1, 4, 1, true, '2010-03-01', null),
       ('Z Rusinowej Polany do Palenicy Białczańskiej', 252.4, 2, 1, 1, 4, true, '2010-03-01', null),
       ('Z Polany pod Wołoszynem na Rusinową Polanę', 522.2, 3, 1, 5, 1, true, '2010-03-01', null),
       ('Z Rusinowej Polany na Polanę pod Wołoszynem', 522.2, 3, 1, 1, 5, true, '2010-03-01', null),
       ('Z Wierchu Porońca na Łysą Polanę', 22.94, 3, 1, 3, 6, true, '2010-03-01', null),
       ('Z Łysej Polany na Wierch Porońca', 22.94, 4, 1, 6, 3, true, '2010-03-01', null),
       ('Z Palenicy Białczańskiej na Łysą Polanę', 8.4, 1, 1, 4, 6, true, '2010-03-01', null),
       ('Z Łysej Polany do Palenicy Białczańskiej', 8.4, 1, 1, 6, 4, true, '2010-03-01', null),
       ('Z Rusinowej Polany na Gęsią Szyję', 67.2, 4, 1, 1, 7, true, '2010-03-01', null),
       ('Z Gęsiej Szyi na Rusinową Polanę', 67.9, 1, 1, 7, 1, true, '2010-03-01', null),
       ('Z Równi Waksmundzkiej na Gęsią Szyję', 2.24, 2, 1, 8, 7, true, '2010-03-01', null),
       ('Z Gęsiej Szyi na Równień Waksmundzką', 2.14, 1, 1, 7, 8, true, '2010-03-01', null),
       ('Z Psiej Trawki na Równień Waksmundzką', 23.2, 5, 1, 11, 8, true, '2010-03-01', null),
       ('Z Równi Waksmundzkiej na Psią Trawkę', 28.8, 3, 1, 8, 11, true, '2010-03-01', null),
       ('Z Polany pod Wołoszynem na Równień Waksmundzką', 25.4, 4, 1, 5, 8, true, '2010-03-01', null),
       ('Z Równi Waksmundzkiej na Polanę pod Wołoszynem', 22.3, 2, 1, 8, 5, true, '2010-03-01', null),
       ('Z Czerwonego Stawu w Dolinie Pańszczyzny na Równień Waksmundzką', 9.2, 4, 1, 9, 8, true, '2010-03-01', null),
       ('Z Równi Waksmundzkiej do Czerwonego Stawu w Dolinie Pańszczyzny', 12.24, 6, 1, 8, 9, true, '2010-03-01', null),
       ('Ze Schroniska PTTK na Hali Gąsienicowej na Równień Waksmundzką', 40.9, 7, 1, 10, 8, true, '2010-03-01', null),
       ('Z Równi Waksmundzkiej do Schroniska PTTK na Hali Gąsienicowej', 51.24, 8, 1, 8, 10, true, '2010-03-01', null),
       ('Ze Schroniska PTTK na Hali Gąsienicowej na Psią Trawkę', 54.7, 4, 1, 10, 11, true, '2010-03-01', null),
       ('Z Psiej Trawki do Schroniska PTTK na Hali Gąsienicowej', 65.22, 7, 1, 11, 10, true, '2010-03-01', null),
       ('Z Brzezin na Psią Trawkę', 63.26, 5, 1, 12, 11, true, '2010-03-01', null),
       ('Z Psiej Trawki do Brzezin', 43.64, 3, 1, 11, 12, true, '2010-03-01', null),
       ('Z Kasprowego Wierchu na Przełęcz Liliowe', 39.2, 2, 2, 20, 21, true, '2010-03-01', null),
       ('Z Przełęczy Liliowe na Kasprowy Wierch', 29.24, 2, 2, 21, 20, true, '2010-03-01', null)
       ;

INSERT INTO Users(login, email, password, role)
VALUES ('user1', 'great_email@gmail.com', '21b72c0b7adc5c7b4a50ffcb90d92dd6', 'administrator'),
       ('magda_789', 'madzia89@gmail.com', '5b9a8069d33fe9812dc8310ebff0a315', 'użytkownik');

INSERT INTO PlannedTrips(name, user_id)
VALUES ('Super wycieczka', 1),
       ('Bardzo krótka wycieczka', 1);

INSERT INTO PlannedSections(planned_trip_id, position, section_id)
VALUES (1, 1, 1),
       (1, 2, 6),
       (1, 3, 11),
       (1, 4, 10),
       (2, 1, 3);


