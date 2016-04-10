CREATE TABLE satellites
(
name text PRIMARY KEY,
lineone text,
linetwo text,
timezone text,
satellites text,
updateDTS text
);

CREATE TABLE locations
(
callsign text PRIMARY KEY,
lat REAL,
lon REAL,
elevation INT,
timezone text
);


CREATE TABLE timeslots
(
callsign text,
weekdays text,
start_time text,
duration INT,
FOREIGN KEY(callsign) REFERENCES locations(callsign)
);