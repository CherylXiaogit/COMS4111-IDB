/* Find Restaurant by Restaurant id */
SELECT * FROM Restaurant WHERE Restaurant_id = 1699;

/* Find Restaurant by Region Id, rank by avg rating*/
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM 
    (
        (
            SELECT * 
            FROM Belong_to
            WHERE Region_id = 8
        ) AS R INNER JOIN Restaurant USING (Restaurant_id)
    ) INNTER JOIN Review USING (Restaurant_id) 
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC
;

/* Find Restaurant by Region Id, show only sponsored, rank by avg rating*/
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM 
    (
        (
            (
                SELECT * 
                FROM Belong_to
                WHERE Region_id = 8
            ) AS R INNER JOIN Restaurant USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id) 
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC
;

/* Find Restaurant by Zipcode, rank by avg rating */
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM 
    (
        (
            (
                SELECT * 
                FROM Region
                WHERE Zip_code = '15106'
            ) AS R INNER JOIN Belong_to USING (Region_id)
        ) INNER JOIN Restaurant USING (Restaurant_id)
    ) INNTER JOIN Review USING (Restaurant_id) 
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;

/* Find Restaurant by Zipcode, show only sponsored, rank by avg rating*/
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM 
    (
        (
            (
                (
                    SELECT * 
                    FROM Region
                    WHERE Zip_code = '15106'
                ) AS R INNER JOIN Belong_to USING (Region_id)
            ) INNER JOIN Restaurant USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id) 
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;

/* Find Restaurant by Feature Id, rank by avg rating*/
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM 
        (
            (
                SELECT * 
                FROM Special_for
                WHERE Feature_id = 3
            ) AS R INNER JOIN Restaurant USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id) 
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;

/* Find Restaurant by Feature Id, show only sponsored, rank by avg rating*/
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM 
    (
        (
            (
                SELECT * 
                FROM Special_for
                WHERE Feature_id = 3
            ) AS R INNER JOIN Restaurant USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id) 
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;

/* Find Restaurant by Feature Id and Zipcode, rank by avg rating */
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    ( 
        (
            SELECT *
            FROM Special_for
            WHERE Feature_id = 3
        ) AS F
        INNER JOIN
        (
            (
                (
                    SELECT * 
                    FROM Region
                    WHERE Zip_code = '61820'
                ) AS R INNER JOIN Belong_to USING (Region_id)
            ) INNER JOIN Restaurant USING (Restaurant_id)
        ) USING (Restaurant_id)
    ) INNTER JOIN Review USING (Restaurant_id) 
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;

/* Find Restaurant by Feature Id and Zipcode, only show sponsored, rank by avg rating */
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        ( 
            (
                SELECT *
                FROM Special_for
                WHERE Feature_id = 3
            ) AS F
            INNER JOIN
            (
                (
                    (
                        SELECT * 
                        FROM Region
                        WHERE Zip_code = '61820'
                    ) AS R INNER JOIN Belong_to USING (Region_id)
                ) INNER JOIN Restaurant USING (Restaurant_id)
            ) USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id) 
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;


/* Find Restaurant by Feature Id and Region Id, rank by avg rating */
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    ( 
        (
            SELECT *
            FROM Special_for
            WHERE Feature_id = 3
        ) AS F
        INNER JOIN
        (
            (
                (
                    SELECT * 
                    FROM Region
                    WHERE region_id = 8
                ) AS R INNER JOIN Belong_to USING (Region_id)
            ) INNER JOIN Restaurant USING (Restaurant_id)
        ) USING (Restaurant_id)
    ) INNTER JOIN Review USING (Restaurant_id) 
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;

/* Find Restaurant by Feature Id and Region Id, only show sponsored, rank by avg rating */
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        ( 
            (
                SELECT *
                FROM Special_for
                WHERE Feature_id = 3
            ) AS F
            INNER JOIN
            (
                (
                    (
                        SELECT * 
                        FROM Region
                        WHERE region_id = 8
                    ) AS R INNER JOIN Belong_to USING (Region_id)
                ) INNER JOIN Restaurant USING (Restaurant_id)
            ) USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id) 
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;

/* Add Review */
INSERT INTO Review (Restaurant_id, Person_id, Comment, Date, Rate) VALUES (6239, 1147, 'Hmmmm', '07/02/2015', 2);

/* Find Review by Person Id, order by date */
SELECT * from review where Person_id = 1 order by date DESC;

/* Find Review by Restaurant_id, order by date */
SELECT * from review where Restaurant_id = 10 order by date DESC;

/* Add Event */
INSERT INTO Event (Name, Description, EDate, ETime) VALUES ('2016 CU Grad Fair!', 'As graduation approacahes, you will want to make sure you have all everything you need for the big day(s)!Order your cap and gown, graduation announcements, class ring, and more at the Grad Fair in the Columbia University Bookstore, March 8-10, 11:00 a.m.-7:00 p.m.Vendors will be offering discounts, and students who attend get $15 off a diploma frame and 25% off all clearance and Class of 2016 merchandise.', '3/8/2016', '11:00');

/* Add Person to admin event */
INSERT INTO Own (Event_id, Person_id) VALUES (1, 1);

/* Add Person to join event */
INSERT INTO PJoinE (Event_id, Person_id) VALUES (1, 1);

/* Find Event by admin's Person_id, show the events admined by the user */
SELECT Event_id, Name, Description, EDate, ETime, COUNT(PJoinE.Person_id)
FROM 
    (
        (SELECT Event_id FROM Own WHERE Person_id = 99) AS O
        INNER JOIN Event USING(Event_id)
    ) LEFT OUTER JOIN PJoinE USING (Event_id)
GROUP BY Event_id, Name, Description, EDate, ETime
ORDER BY EDate DESC;

/* Find Event by Person_id, show the events the person joins */
SELECT Event_id, Name, Description, EDate, ETime, COUNT(PJoinE.Person_id)
FROM 
    (
        (SELECT Event_id FROM PJoinE WHERE Person_id = 3) AS O
        INNER JOIN Event USING(Event_id)
    ) LEFT OUTER JOIN PJoinE USING (Event_id)
GROUP BY Event_id, Name, Description, EDate, ETime
ORDER BY EDate DESC;

/* Find Person by Event_id, show the person who admin the event */
SELECT *
FROM 
    (
        (SELECT Person_id FROM Own WHERE Event_id = 1) AS O
        INNER JOIN Person USING(Person_id)
    )
;

/* Find Person by Event_id, show the people who join the event */
SELECT *
FROM 
    (
        (SELECT Person_id FROM PJoinE WHERE Event_id = 1) AS O
        INNER JOIN Person USING(Person_id)
    )
;

/* Find Events that a person does not manage nor join */
SELECT *
FROM Event 
WHERE Event_id NOT IN (
    (
    SELECT Event_id
    FROM Own
    WHERE Person_id = 2
    ) UNION (
    SELECT Event_id
    FROM PJoinE
    WHERE Person_id = 2
    ) 
);
