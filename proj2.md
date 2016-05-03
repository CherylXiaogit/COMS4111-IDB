## COMS W4111 Project 2

### Chia-Hao Hsu (ch3141), Hsiang-Ho Lin (hl2907)

#### 1. PostgreSQL database account number: hl2907

#### 2. Explain carefully and thoroughly your rationale behind your modifications to the schema and how these modifications fit within your overall project 
- Composite types:
- Arrays: For the array type, we add "like_names" to the review table since we want to know better about the user behavior. We want to know what kind of review the user will like most and what kind of review will not be attractive to user. Based on the analysis, we can provide better review comment guideline for user to make user write better review and attract more users for our application.
- Documents: For the document type, we add description column for feature table. Since sometimes the simple feature cannot make user to understand the meaning of the feature. Therefore, we add some deatial description for feature to make user have more sense about the meaning of feature.


#### 3. Three Interesting SQL queries:
   We imported the real data from Yelp dataset into our database, which contains around 60000+ restaurant, review, and user data. 
   We modified three tables for fitting the requirement for project 2:

   1. Feature: Add description text attribute to better describe the feature
   2. Review: Add Array type column "Like_names", which means the people's name who like this review
   3. Event: Add qualification composite type to filter out events for people who are not qualified 

   The following are our interesting queries:
  
  - Find out which review is liked by top 10 biggest number of people and print out the review id, restaurant id, person id, review comment, how much like number the review gets, and also the rate for the rate.
   
  ```sql
  select Review_id, Restaurant_id, Person_id, comment, Like_names, top_liked_review.like_cnt, Rate
  from review, 
  (select review_stats.Review_id as top_review_id, review_stats.like_cnt
  from (select Review_id,  substring(array_dims(Like_names) from 4 for 1) as like_cnt from review) review_stats
  group by review_stats.Review_id, review_stats.like_cnt
  order by review_stats.like_cnt
  desc
  limit 10) top_liked_review
  where Review_id = top_liked_review.top_review_id
  ;  
  ```
  
  The following is the result:

         review_id | restaurant_id | person_id | comment |              like_names              | like_cnt | rate
        -----------+---------------+-----------+---------+--------------------------------------+----------+------
                88 |         13535 |      1756 | Hmmmm   | {Jenny,April,"Chris Hsu",Brian,Alex} | 5        |    5
                75 |         17087 |        56 | Hmmmm   | {Jenny,April,Eason}                  | 3        |    4
                76 |           914 |       598 | Hmmmm   | {Jason,Russel,April}                 | 3        |    3
                77 |          5438 |       604 | Hmmmm   | {CK,Waston,Donald}                   | 3        |    3
                78 |         17790 |      1787 | Hmmmm   | {Hillary,Trump,Maggie}               | 3        |    5
                79 |         18067 |      1273 | Hmmmm   | {Clinton,Yoyo,Roger}                 | 3        |    1
                80 |          5085 |      1517 | Hmmmm   | {Michael,Ryo,King}                   | 3        |    5
                81 |         14644 |        50 | Hmmmm   | {N,Suman,Coco}                       | 3        |    4
                82 |          2941 |       882 | Hmmmm   | {Jenni,Heather,Kathy}                | 3        |    2
                83 |           484 |      1989 | Hmmmm   | {Anthony,C,Mary}                     | 3        |    5
        (10 rows)

  - As a customer, they might want to find some best restaurants, or some cheap restaurants based on the description we provided in the feature column. Therefore here it comes the query to find out five restaurants with their name, id and address which matches the "cheap or best restaurants" description.

  ```sql
    select Restaurant.restaurant_id, Restaurant.name, Restaurant.addr
    from Restaurant, Special_for, 
    (SELECT Feature_id as f_id, ts_rank(to_tsvector(Description), query) AS rank
    FROM Feature, to_tsquery('best & restaurant | cheap') query
    ORDER BY rank 
    DESC
    LIMIT 5) best_or_cheap_restaurant
    where Restaurant.Restaurant_id = Special_for.Restaurant_id and Special_for.Feature_id = best_or_cheap_restaurant.f_id
    limit 5
    ;
  ```


  The following is the result:

           restaurant_id |           name           |                       addr
          ---------------+--------------------------+--------------------------------------------------
                   19849 | Jersey Mikes Subs        | 1743 E Camelback Suite A-02 Phoenix, AZ 85016
                   15121 | Genghis Grill            | 4722 E Cactus Rd Phoenix, AZ 85032
                    5300 | Pittsburgh Steak Company | 1924 E Carson St South Side Pittsburgh, PA 15203
                   14559 | Taco Bell                | 199 North Pecos Henderson, NV 89014
                    3956 | Pacifics Cafe            | 7272 E Indian School Rd Scottsdale, AZ 85251
          (5 rows)



   - 
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




