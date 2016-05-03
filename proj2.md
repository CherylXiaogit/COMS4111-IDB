## COMS W4111 Project 2

### Chia-Hao Hsu (ch3141), Hsiang-Ho Lin (hl2907)

#### 1. PostgreSQL database account number: hl2907

#### 2. Explain carefully and thoroughly your rationale behind your modifications to the schema and how these modifications fit within your overall project 

- Composite types: For composite types we added an attribute of qualify_type type into the event table. This composite type consists of boolean values indicating on/off of the filter and the filter conditions. The purpose for qualify_type is for event administrators to limit the access of their events to only certain kind of people. For instance, a event administrator can set age filter on and set age to 18 so that only people who are no less than 18 years old are able to join the event. Moreover a event administrator can also set the gender filter to limit access to male for female. This modification allows the administrator to set proper qualification of participants.

- Arrays: For the array type, we add "like_names" to the review table since we want to know better about the user behavior. We want to know what kind of review the user will like most and what kind of review will not be attractive to user. Based on the analysis, we can provide better review comment guideline for user to make user write better review and attract more users for our application.

- Documents: For the document type, we add description column for feature table. Since sometimes the simple feature cannot make user to understand the meaning of the feature. Therefore, we add some deatial description for feature to make user have more sense about the meaning of feature.


#### 3. Three Interesting SQL queries:
   We imported the real data from Yelp dataset into our database, which contains around 60000+ restaurant, review, and user data. 
   We modified three tables for fitting the requirement for project 2:

   The following are our interesting queries:
  
  1. Review Table: Add Array type column "Like_names", which means the people's name who like this review
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

  2. Feature Table: Add description text attribute to better describe the feature
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


   3. Event Table: Add qualification composite type to filter out events for people who are not qualified 
   - We allow the administrator to set proper qualification of participants. So when a user is searching for event that the user might be interested (neither joined nor managed), we have to filter out events that the user does not qualify. The following query finds the events which person with persion_id 2 qualifies but neither joined nor managed.

   - 
   ```sql
    SELECT Event_id, name
    FROM Event AS e
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
    )
    AND (
            (e.qualify).is_age_on = FALSE OR
        (
            (e.qualify).is_age_on = TRUE AND
            (e.qualify).age_geq <= (SELECT age from person where person_id = 2)
        )
    )
    AND (
            (e.qualify).is_gender_on = FALSE OR
        (
            (e.qualify).is_gender_on = TRUE AND
            (e.qualify).gender = (SELECT gender from person where person_id = 2)
        )
    );
   ```
  The following is the result:


         event_id |         name         
        ----------+----------------------
                2 | CUTSA Movie Event!  
                3 | Health Hackathon    
                4 | BATMAN V SUPERMAN   
                5 | Pillow Fight NYC    
                6 | Startup Career Fair 
                7 | TechCrunch Disrupt  
                8 | NYC Comic Con 2016  
                9 | FB site visit       
                10 | Hot Dog Throwdown   
                11 | 2016 CU Grad Fair!  
                13 | 2016 CU Grad Fair!  
                14 | test                
                15 | test                
                16 | Xmas                
                17 | cool                
                31 | facebook employee ne
                32 | Google Foodie       
                33 | test                
                18 | Chris's BDay Party  
                20 | Chill               
                21 | My BDay Party       
                23 | cool                
                25 | dsfasf              
                26 | sadasd              
                27 | NYE                 
                29 | Facebook Employee   
                30 | NYE at NYC          
        (27 rows)

