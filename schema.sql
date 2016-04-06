CREATE TABLE satellites
(
name text PRIMARY KEY,
lineone text,
linetwo text,
updateDTS text
);

CREATE TABLE locations
(
callsign text PRIMARY KEY,
lat REAL,
lon REAL,
elevation INT
);