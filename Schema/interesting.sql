/* For each region with any restaurant reviews, find out the average rating of restaurants with 1 or more reviews*/
SELECT Zip_code, AVG(Rate)
FROM (((Belong_to INNER JOIN Restaurant USING (Restaurant_id)) INNER JOIN Region Using (Region_id)) INNER JOIN Review USING (Restaurant_id))
GROUP BY Zip_code;

/* For each region with any restaurant reviews, find out the average male and female rating of restaurants with 1 or more reviews*/
SELECT Zip_code, AVG(male_rate), AVG(female_rate)
FROM 
    SELECT Zip_code, Rate AS male_rate FROM ((((Belong_to INNER JOIN Restaurant USING (Restaurant_id)) INNER JOIN Region Using (Region_id)) INNER JOIN Review USING (Restaurant_id)) INNER JOIN (SELECT * FROM Person WHERE gender = 'male') AS tmp Using (Person_id))
    UNION
    SELECT Zip_code, Rate AS female_rate FROM ((((Belong_to INNER JOIN Restaurant USING (Restaurant_id)) INNER JOIN Region Using (Region_id)) INNER JOIN Review USING (Restaurant_id)) INNER JOIN (SELECT * FROM Person WHERE gender = 'female') AS tmp Using (Person_id)) 
GROUP BY Zip_code;

/* For each region with any restaurant reviews, find out the average review count of restaurants with 1 or more reviews*/
SELECT Zip_code, AVG(review_num)
FROM
    (SELECT Zip_code, Restaurant_id, COUNT(Restaurant_id) AS review_num
    FROM (((Belong_to INNER JOIN Restaurant USING (Restaurant_id)) INNER JOIN Region Using (Region_id)) INNER JOIN Review USING (Restaurant_id))
    GROUP BY Zip_code, Restaurant_id) As tmp
GROUP BY Zip_code;
