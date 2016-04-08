/* Find Resturant by Region Id, rank by avg rating*/
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

/* Find Resturant by Region Id, show only sponsored, rank by avg rating*/
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

/* Find Resturant by Zipcode, rank by avg rating */
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

/* Find Resturant by Zipcode, show only sponsored, rank by avg rating*/
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

/* Find Resturant by Feature Id, rank by avg rating*/
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

/* Find Resturant by Feature Id, show only sponsored, rank by avg rating*/
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

/* Find Resturant by Feature Id and Zipcode, rank by avg rating */
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

/* Find Resturant by Feature Id and Zipcode, only show sponsored, rank by avg rating */
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


