## COMS W4111 Project 1.2

### Chia-Hao Hsu (ch3141), Hsiang-Ho Lin (hl2907)

####1. PostgreSQL database account number: hl2907

####2. Three Interesting SQL queries:
   We imported the real data from Yelp dataset into our database, which contains around 60000+ restaurant, review, and user data. 
   Also we modified some data specific for our project.
   
   The following are our interesting queries:
  
  - For each region with any restaurant reviews, find out the average review rating in the region. This helps us to find out which region has better restaurant.
   
   ```sql
  SELECT Zip_code, AVG(Rate)
  FROM (((Belong_to INNER JOIN Restaurant USING (Restaurant_id)) INNER JOIN Region Using (Region_id)) INNER JOIN Review USING (Restaurant_id))
  GROUP BY Zip_code;
  ```
  The following is the result:

              zip_code      |        avg         
      ----------------------+--------------------
       28202                | 3.3333333333333333
       61820                | 3.6000000000000000
       15106                | 3.4000000000000000
      (3 rows)

  - For each region with any restaurant reviews for both genders, find out the average male and female review rating in the region. This helps us to find out which region has better restaurant for different genders.
  
   ```sql
  SELECT *
  FROM 
      (SELECT Zip_code, AVG(Rate) AS male_rating
      FROM (((Belong_to INNER JOIN Restaurant USING (Restaurant_id)) INNER JOIN Region Using (Region_id)) INNER JOIN Review USING (Restaurant_id)) INNER JOIN (SELECT * FROM Person WHERE gender = 'male') AS tmp Using (Person_id)
      GROUP BY Zip_code) AS Male
      INNER JOIN
      (SELECT Zip_code, AVG(Rate) AS female_rating
      FROM (((Belong_to INNER JOIN Restaurant USING (Restaurant_id)) INNER JOIN Region Using (Region_id)) INNER JOIN Review USING (Restaurant_id)) INNER JOIN (SELECT * FROM Person WHERE gender = 'female') AS tmp Using (Person_id)
      GROUP BY Zip_code) AS Female 
      USING (Zip_code);
  ```
  The following is the result:


             zip_code       |    male_rating     |   female_rating    
      ----------------------+--------------------+--------------------
       28202                | 2.7500000000000000 | 3.8000000000000000
       61820                | 3.6000000000000000 | 3.6000000000000000
       15106                | 3.2500000000000000 | 3.5000000000000000
      (3 rows)

  - For each region with any restaurant reviews, find out the average review count of restaurants with 1 or more reviews. This helps us to find out which region has popular restaurant.

   ```sql
    SELECT Zip_code, AVG(review_num)
    FROM
        (SELECT Zip_code, Restaurant_id, COUNT(Restaurant_id) AS review_num
        FROM (((Belong_to INNER JOIN Restaurant USING (Restaurant_id)) INNER JOIN Region Using (Region_id)) INNER JOIN Review USING (Restaurant_id))
        GROUP BY Zip_code, Restaurant_id) As tmp
    GROUP BY Zip_code;
   ```
  The following is the result:

               zip_code       |        avg         
        ----------------------+--------------------
         28202                | 3.0000000000000000
         61820                | 3.3333333333333333
         15106                | 3.3333333333333333
        (3 rows)




