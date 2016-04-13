DATABASEURI = 																   \
"postgresql://hl2907:481516losT_@w4111vm.eastus.cloudapp.azure.com/w4111"

SIGNUP_USER_SQL = 															   \
"INSERT INTO Person (Name, Email, Age, Gender, Zip_Code) VALUES (%s, %s, %s, %s, %s);"

GET_LAST_USER_ID_SQL = "SELECT MAX(Person_id) FROM Person;"

LOGIN_USER_SQL = 															   \
'''
SELECT Person_id, Name, Email
FROM Person WHERE
Name = %s and Email = %s
'''

FIND_USER_OWN_EVENTS_SQL =                                                     \
'''
SELECT Event_id, Name, Description, EDate, ETime, COUNT(PJoinE.Person_id)
FROM
(
    (SELECT Event_id FROM Own WHERE Person_id = %s) AS O
    INNER JOIN Event USING(Event_id)
) LEFT OUTER JOIN PJoinE USING (Event_id)
GROUP BY Event_id, Name, Description, EDate, ETime
ORDER BY EDate DESC;
'''

FIND_USER_JOIN_EVENTS_SQL =                                                    \
'''
SELECT Event_id, Name, Description, EDate, ETime, COUNT(PJoinE.Person_id)
FROM
(
    (SELECT Event_id FROM PJoinE WHERE Person_id = %s) AS O
    INNER JOIN Event USING(Event_id)
) LEFT OUTER JOIN PJoinE USING (Event_id)
GROUP BY Event_id, Name, Description, EDate, ETime
ORDER BY EDate DESC;
'''

FIND_EVENTS_USER_NOT_IN_SQL = 												   \
'''
SELECT *
FROM Event
WHERE Event_id NOT IN (
    (
	    SELECT Event_id
	    FROM Own
	    WHERE Person_id = %s
    ) UNION (
	    SELECT Event_id
	    FROM PJoinE
	    WHERE Person_id = %s
    )
);

'''

CREATE_EVENT_SQL = 															   \
'''
INSERT INTO Event (Name, Description, EDate, ETime) VALUES (%s, %s, %s, %s);
'''

CREATE_OWN_SQL = 															   \
'''
INSERT INTO Own (Event_id, Person_id) VALUES
((SELECT MAX(event_id) from Event), %s);
'''

FIND_EVENT_WITH_ID_SQL = 													   \
'''
SELECT * FROM Event WHERE Event_id = %s
'''

JOIN_EVENT_SQL =															   \
'''
INSERT INTO PJoinE (Event_id, Person_id) VALUES (%s, %s);
'''

FIND_ALL_FEATURES_SQL = 													   \
'''
SELECT * FROM feature;
'''

FIND_ALL_REGION_ID_ZIPCODE_SQL = 											   \
'''
SELECT region_id, zip_code FROM region;
'''

FIND_ALL_REGION_ID_ZIPCODE_SORTED_SQL = 								        \
'''
SELECT region_id, zip_code FROM region order by zip_code;
'''

FIND_RESTAURANT_BY_RESTAURANT_ID =                                          \
'''
SELECT Restaurant_id, Name, Addr, Url, Location, count(*) as dum1, count(*) as dum2
FROM Restaurant
WHERE Restaurant_id = %s
GROUP BY Restaurant_id
'''

FIND_RESTAURANT_BY_REGION_ID = 											   \
'''
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            SELECT *
            FROM Belong_to
            WHERE Region_id = %s
        ) AS R INNER JOIN Restaurant USING (Restaurant_id)
    ) INNTER JOIN Review USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;
'''

FIND_REVIEWS_BY_RESTAURANT_ID = 											   \
'''
SELECT * from review where Restaurant_id = %s order by date DESC;

'''

FIND_RESTAURANT_BY_ZIPCODE = 												   \
'''
SELECT Restaurant_id, Name, Addr, Url, Location, coalesce(AVG(rate), 0), count(Review_id)
FROM
    (
        (
            (
                SELECT *
                FROM Region
                WHERE Zip_code = %s
            ) AS R INNER JOIN Belong_to USING (Region_id)
        ) INNER JOIN Restaurant USING (Restaurant_id)
    ) LEFT OUTER JOIN Review USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC NULLS LAST;
'''

FIND_RESTAURANT_BY_FEATURE = 												   \
'''
SELECT Restaurant_id, Name, Addr, Url, Location, coalesce(AVG(rate), 0), count(Review_id)
FROM
        (
            (
                SELECT *
                FROM Special_for
                WHERE Feature_id = %s
            ) AS R INNER JOIN Restaurant USING (Restaurant_id)
        ) LEFT OUTER JOIN Review USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC NULLS LAST;
'''

FIND_RESTAURANT_BY_ZIPCODE_AND_FEATURE = 									   \
'''
SELECT Restaurant_id, Name, Addr, Url, Location, coalesce(AVG(rate), 0), count(Review_id)
FROM
    (
        (
            SELECT *
            FROM Special_for
            WHERE Feature_id = %s
        ) AS F
        INNER JOIN
        (
            (
                (
                    SELECT *
                    FROM Region
                    WHERE Zip_code = %s
                ) AS R INNER JOIN Belong_to USING (Region_id)
            ) INNER JOIN Restaurant USING (Restaurant_id)
        ) USING (Restaurant_id)
    ) LEFT OUTER JOIN Review USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC NULLS LAST;
'''

FIND_RESTAURANT_WITH_REVIEW_BY_ID = 									   	   \
'''
SELECT restaurant_id, restaurant_name, addr, person_name, rate, comment, date
FROM
(Review INNER JOIN (SELECT Person_id, Name as Person_name FROM Person)
AS P1 USING(Person_id) ) AS T1
INNER JOIN
(SELECT Restaurant_id, Name as Restaurant_name, Addr as addr FROM Restaurant)
AS R1 USING(Restaurant_id)
WHERE Restaurant_id = %s
ORDER BY date DESC;
'''

ADD_REVIEW_SQL = 															   \
'''
INSERT INTO Review (Restaurant_id, Person_id, Comment, Date, Rate)
VALUES (%s, %s, %s, %s, %s);
'''

def get_first_result(cursor):
	data = None
	for result in cursor:
		data = result
		break
	return data

def get_results(cursor):
	return [result for result in cursor]
