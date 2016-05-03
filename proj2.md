## COMS W4111 Project 2

### Chia-Hao Hsu (ch3141), Hsiang-Ho Lin (hl2907)

#### 1. PostgreSQL database account number: hl2907

#### 2. Explain carefully and thoroughly your rationale behind your modifications to the schema and how these modifications fit within your overall project 

- Composite types: For composite types we added an attribute of qualify_type type into the event table. This composite type consists of boolean values indicating on/off of the filter and the filter conditions. The purpose for qualify_type is for event administrators to limit the access of their events to only certain kind of people. For instance, a event administrator can set age filter on and set age to 18 so that only people who are no less than 18 years old are able to join the event. Moreover, a event administrator can also set the gender filter to limit access to male for female. This modification allows the administrator to set proper qualification of participants.

  ```sql
    CREATE TYPE qualify_type AS (
        is_age_on       BOOLEAN,
        is_gender_on    BOOLEAN,
        age_geq         INTEGER,
        gender          CHAR(10)
    ); 

    CREATE TABLE Event
    (
        Event_id SERIAL,
        Name CHAR(20) NOT NULL,
        Description text, 
        EDate DATE NOT NULL,
        ETime Time NOT NULL,
        PRIMARY KEY(Event_id),
    );

    ALTER TABLE Event ADD COLUMN qualify qualify_type DEFAULT (false, false, 0, 'male');
  ```

- Arrays: For the array type, we add "like_names" to the review table. This attribute stores the names of users who have liked a certain review. This encourages user interaction and helps us to know better about the user behavior. Users can look at the list of users who have liked a review to get a sense of a review's helpfulness.  We also want to know what kind of review the user will like most and what kind of review will not be attractive to user. Based on the analysis, we can provide better review comment guideline for user to make user write better review and attract more users for our application.

  ```sql
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

    ALTER TABLE Review ADD COLUMN Like_names text[];
  ```

- Documents: For the document type, we add description column for feature table. Since sometimes the simple feature cannot make user to understand the meaning of the feature. Therefore, we add some deatial description for feature to make user have more sense about the meaning of feature.

  ```sql
    CREATE TABLE Feature
    (
        Feature_id SERIAL,
        Name CHAR(20) NOT NULL,
        PRIMARY KEY(Feature_id)
    );

    ALTER TABLE Feature ADD COLUMN Description TEXT;
  ```

#### 3. Three Interesting SQL queries:
   We imported the real data from Yelp dataset into our database, which contains around 60000+ restaurant, review, and user data. 
   We modified three tables for fitting the requirement for project 2:

   The following are our interesting queries:
  
  - Review Table: Add Array type column "Like_names", which means the people's name who like this review
  
  The following query finds out the top 10 most liked reviews and print out the review id, restaurant id, person id, review comment, how much like number the review gets, and also the rate for the rate.
   
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

         review_id | restaurant_id | person_id |          comment          |              like_names              | like_cnt | rate
        -----------+---------------+-----------+---------------------------+--------------------------------------+----------+------
                88 |         13535 |      1756 | Not bad.                  | {Jenny,April,"Chris Hsu",Brian,Alex} | 5        |    5
                75 |         17087 |        56 | My life is complete       | {Jenny,April,Eason}                  | 3        |    4
                76 |           914 |       598 | 10/10 would come again    | {Jason,Russel,April}                 | 3        |    3
                77 |          5438 |       604 | Nice                      | {CK,Waston,Donald}                   | 3        |    3
                78 |         17790 |      1787 | Awesome                   | {Hillary,Trump,Maggie}               | 3        |    5
                79 |         18067 |      1273 | You'll miss this place    | {Clinton,Yoyo,Roger}                 | 3        |    1
                80 |          5085 |      1517 | GREAT                     | {Michael,Ryo,King}                   | 3        |    5
                81 |         14644 |        50 | Don't know what to say... | {N,Suman,Coco}                       | 3        |    4
                82 |          2941 |       882 | Pretty sweet              | {Jenni,Heather,Kathy}                | 3        |    2
                83 |           484 |      1989 | Loving it                 | {Anthony,C,Mary}                     | 3        |    5
        (10 rows)

  - Feature Table: Add description text attribute to better describe the feature
  
  As a customer, they might want to find some best restaurants, or some cheap restaurants based on the description we provided in the feature column. Therefore here it comes the query to find out five restaurants with their name, id and address which matches the "cheap or best restaurants" description.

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


  - Event Table: Add qualification composite type to filter out events for people who are not qualified 
   
  We allow the administrator to set proper qualification of participants. So when a user is searching for event that the user might be interested (neither joined nor managed), we have to filter out events that the user does not qualify. The following query finds the events which persion_id 2 qualifies but neither joined nor managed.

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
               16 | Xmas                
               17 | cool                
               31 | facebook employee ne
               32 | Google Foodie       
               18 | Chris's BDay Party  
               20 | Chill               
               21 | My BDay Party       
               23 | cool                
               27 | NYE                 
               29 | Facebook Employee   
               25 | English Meetup      
               26 | Metal lover         
               30 | NYE at NYC          
               14 | Pretty sweet
               15 | No more nightmare
               33 | My bday
        (27 rows)

