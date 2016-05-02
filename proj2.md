## COMS W4111 Project 2

### Chia-Hao Hsu (ch3141), Hsiang-Ho Lin (hl2907)

#### 1. PostgreSQL database account number: hl2907

#### 2. Three Interesting SQL queries:

   We imported the real data from Yelp dataset into our database, which contains around 60000+ restaurant, review, and user data. 
   We modified three tables for fitting the requirement for project 2:

   1. Feature
   2. Review: Add Array type column "Like_names", which means the people's name who like this review
   3. Event: 

   The following are our interesting queries:
  
  - Find out which review is liked by biggest number of people and print out the review id, restaurant id, person id, review comment, how much like number the review gets, and also the rate for the rate.
   
  ```sql
  select Review_id, Restaurant_id, Person_id, comment, Like_names, top_liked_review.like_cnt, Rate
  from review, 
  (select review_stats.Review_id as top_review_id, review_stats.like_cnt
  from (select Review_id,  substring(array_dims(Like_names) from 4 for 1) as like_cnt from review) review_stats
  group by review_stats.Review_id, review_stats.like_cnt
  order by review_stats.like_cnt
  desc
  limit 1) top_liked_review
  where Review_id = top_liked_review.top_review_id
  ;  
  ```
  
  The following is the result:

         review_id | restaurant_id | person_id | comment |              like_names              | like_cnt | rate
        -----------+---------------+-----------+---------+--------------------------------------+----------+------
                88 |         13535 |      1756 | Hmmmm   | {Jenny,April,"Chris Hsu",Brian,Alex} | 5        |    5

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




