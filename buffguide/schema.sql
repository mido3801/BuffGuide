DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Classes;
DROP TABLE IF Exists Locations;
DROP TABLE IF Exists UserClass;
DROP TABLE IF Exists ClassLocation;
DROP TABLE IF EXISTS locationAbbrev;

CREATE TABLE Users(
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    userName TEXT UNIQUE,
    userPass TEXT UNIQUE
);

CREATE TABLE Classes(
    classID INTEGER PRIMARY KEY,
    classDept TEXT NOT NULL,
    classCourseNum TEXT NOT NULL,
    classSectionNum TEXT NOT NULL,
    classSessionNum TEXT NOT NULL,
    classClassNum INTEGER NOT NULL,
    classTitle TEXT NOT NULL,
    classComponent TEXT NOT NULL,
    classBuilding TEXT,
    classRoom TEXT
);

CREATE TABLE Locations(
    locationID INTEGER PRIMARY KEY AUTOINCREMENT,
    locationName TEXT UNIQUE NOT NULL,
    locationLatitude TEXT NOT NULL,
    locationLongitude TEXT NOT NULL
);

CREATE TABLE UserClass(
    userID INTEGER NOT NULL,
    classID INTEGER NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (classID) REFERENCES Classes(classID)
);

CREATE TABLE ClassLocation(
    classID INTEGER NOT NULL,
    locationID INTEGER NOT NULL,
    FOREIGN KEY (classID) REFERENCES Classes(classID),
    FOREIGN KEY (locationID) REFERENCES Locations(locationID)
);

CREATE TABLE locationAbbrev(
    abbrev TEXT UNIQUE NOT NULL,
    locationName TEXT NOT NULL
);