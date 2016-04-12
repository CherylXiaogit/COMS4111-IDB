DROP TABLE Person CASCADE;
DROP TABLE Event CASCADE;
DROP TABLE Restaurant CASCADE;
DROP TABLE Feature CASCADE;
DROP TABLE Review CASCADE;
DROP TABLE Region CASCADE;
DROP TABLE PJoinE CASCADE;
DROP TABLE Own CASCADE;
DROP TABLE Write CASCADE;
DROP TABLE Get CASCADE;
DROP TABLE Belong_to CASCADE;
DROP TABLE Recommend CASCADE;
DROP TABLE Special_for CASCADE;

CREATE TABLE Person 
(
    Person_id SERIAL,
    Name CHAR(20) NOT NULL,
    Email CHAR(20) NOT NULL,
    Gender CHAR(10),
    Age INTEGER,
    PRIMARY KEY(Person_id),
    CONSTRAINT valid_age CHECK (Age > 0 AND Age < 100),
    CONSTRAINT valid_gender CHECK (Gender = 'male' OR Gender = 'female')
);

ALTER TABLE Person ADD COLUMN Zip_code CHAR(20) NOT NULL DEFAULT '15205'

/* Good */
/*
INSERT INTO Person (Name, Email, Gender, Age) VALUES ('Sean Malto', 'sm@columbia.edu', 'male', 24);
INSERT INTO Person (Name, Email, Gender, Age) VALUES ('Chaz Ortiz', 'co@columbia.edu', 'male', 22);
INSERT INTO Person (Name, Email, Gender, Age) VALUES ('Daisy Zhang', 'dz@columbia.edu', 'female', 23);
*/

/* Bad */
/*
INSERT INTO Person (Name, Email, Gender, Age) VALUES ('Daisy Zhang', 'dz@columbia.edu', 'female', -1);
INSERT INTO Person (Name, Email, Gender, Age) VALUES ('Daisy Zhang', 'dz@columbia.edu', 'female', 223);
INSERT INTO Person (Name, Email, Gender, Age) VALUES ('Daisy Zhang', 'dz@columbia.edu', 'abc', 22);
*/

CREATE TABLE Event 
(
    Event_id SERIAL,
    Name CHAR(20) NOT NULL,
    Description text,
    EDate DATE NOT NULL,
    ETime Time NOT NULL,
    PRIMARY KEY(Event_id)
);

/*
INSERT INTO Event (Name, Description, EDate, ETime) VALUES ('Farewell for John', 'John is sooooo cool, everyone loves John. Wish you all the best back to Taiwan', '3/5/2016', '17:00');
*/

CREATE TABLE Restaurant 
(
    Restaurant_id bigint, /* The id according to the data source */
    Name text NOT NULL,
    Addr text NOT NULL,
    Url CHAR(20),
    Location POINT NOT NULL,
    PRIMARY KEY(Restaurant_id)
);

/*
INSERT INTO Restaurant (Restaurant_id, Name, Addr) VALUES (1213123, 'Jin Ramen', '555 W 125 St');
*/

CREATE TABLE Feature
(
    Feature_id SERIAL,
    Name CHAR(20) NOT NULL,
    PRIMARY KEY(Feature_id)
);

/*
INSERT INTO Feature (Name) VALUES ('cheap');
INSERT INTO Feature (Name) VALUES ('wine');
*/

CREATE TABLE Review
(
    Review_id SERIAL,
    Restaurant_id bigint NOT NULL,
    Person_id INTEGER NOT NULL,
    Comment TEXT NOT NULL,
    Date DATE,
    Rate INTEGER NOT NULL,
    PRIMARY KEY (Review_id),
    UNIQUE (Person_id, Restaurant_id),
    FOREIGN KEY (Person_id) REFERENCES Person ON DELETE CASCADE,
    FOREIGN KEY (Restaurant_id) REFERENCES Restaurant ON DELETE CASCADE,
    CONSTRAINT valid_rate CHECK (Rate > 0 AND Rate < 6)
);

/*
INSERT INTO Review (Restaurant_id, Person_id, Comment, Date, Rate) VALUES (1213123, 1, 'vely gooda', '3/11/2016', 5);
*/

CREATE TABLE Region
(
    Region_id INTEGER,
    Zip_code CHAR(20) NOT NULL,
    NW_point POINT NOT NULL,
    SE_point POINT NOT NULL,
    UNIQUE (Zip_code),
    PRIMARY KEY(Region_id)
);

/*
INSERT INTO Region (Region_id, Zip_code, NW_point, SE_point) VALUES (1, 10027, point(40.817419,73.973054), point(40.802380,73.943056));
*/

CREATE TABLE PJoinE
(
    Join_id SERIAL,
    Event_id INTEGER NOT NULL,
    Person_id INTEGER NOT NULL,
    UNIQUE (Person_id, Event_id),
    PRIMARY KEY(Join_id),
    FOREIGN KEY (Person_id) REFERENCES Person,
    FOREIGN KEY (Event_id) REFERENCES Event
);

/*
INSERT INTO PJoinE (Event_id, Person_id) VALUES (1, 1);
INSERT INTO PJoinE (Event_id, Person_id) VALUES (1, 2);
INSERT INTO PJoinE (Event_id, Person_id) VALUES (1, 3);
*/

CREATE TABLE Own
(
    Own_id SERIAL,
    Event_id INTEGER NOT NULL,
    Person_id INTEGER NOT NULL,
    UNIQUE (Person_id, Event_id),
    PRIMARY KEY(Own_id),
    FOREIGN KEY (Person_id) REFERENCES Person,
    FOREIGN KEY (Event_id) REFERENCES Event
);

/*
INSERT INTO Own (Event_id, Person_id) VALUES (1, 1);
*/

/* Redundant? */
CREATE TABLE Write
(
    Write_id SERIAL,
    Person_id INTEGER NOT NULL,
    Review_id INTEGER NOT NULL,
    PRIMARY KEY(Person_id, Review_id),
    FOREIGN KEY (Person_id) REFERENCES Person ON DELETE CASCADE,
    FOREIGN KEY (Review_id) REFERENCES Review ON DELETE CASCADE
);

/* Redundant? */
CREATE TABLE Get
(
    Get_id SERIAL,
    Review_id INTEGER NOT NULL,
    Restaurant_id INTEGER NOT NULL,
    PRIMARY KEY(Restaurant_id, Review_id),
    FOREIGN KEY (Review_id) REFERENCES Review ON DELETE CASCADE,
    FOREIGN KEY (Restaurant_id) REFERENCES Restaurant ON DELETE CASCADE
);

CREATE TABLE Belong_to
(
    Belong_to_id SERIAL,
    Restaurant_id INTEGER NOT NULL,
    Region_id INTEGER NOT NULL,
    PRIMARY KEY(Restaurant_id),
    FOREIGN KEY (Restaurant_id) REFERENCES Restaurant ON DELETE CASCADE,
    FOREIGN KEY (Region_id) REFERENCES Region ON DELETE CASCADE
);

/*
INSERT INTO Belong_to (Restaurant_id, Region_id) VALUES (1213123, 1);
*/

/* Commercial Purpose */
CREATE TABLE Recommend
(
    Recommend_id SERIAL,
    Feature_id INTEGER NOT NULL,
    Restaurant_id INTEGER NOT NULL,
    PRIMARY KEY(Recommend_id),
    FOREIGN KEY (Restaurant_id) REFERENCES Restaurant ON DELETE CASCADE,
    FOREIGN KEY (Feature_id) REFERENCES Feature ON DELETE CASCADE
);

/* General Purpose */
CREATE TABLE Special_for
(
    Special_id SERIAL,
    Feature_id INTEGER NOT NULL,
    Restaurant_id INTEGER NOT NULL,
    PRIMARY KEY(Special_id),
    FOREIGN KEY (Restaurant_id) REFERENCES Restaurant ON DELETE CASCADE,
    FOREIGN KEY (Feature_id) REFERENCES Feature ON DELETE CASCADE
);

