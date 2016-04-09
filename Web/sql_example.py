
if __name__ == "__main__":

    data = (1699)
    cmd_find_rest_by_restid = "SELECT * FROM Restaurant WHERE Restaurant_id = %d"
    # cursor = g.conn.execute(cmd_find_rest_by_restid % data)

    data = (8)
    cmd_find_rest_by_regionid = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            SELECT *
            FROM Belong_to
            WHERE Region_id = %d
        ) AS R INNER JOIN Restaurant USING (Restaurant_id)
    ) INNTER JOIN Review USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC
"""
    # cursor = g.conn.execute(cmd_find_rest_by_regionid % data)

    data = (8)
    cmd_find_rest_by_regionid_sp = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            (
                SELECT *
                FROM Belong_to
                WHERE Region_id = %d
            ) AS R INNER JOIN Restaurant USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id)
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC"""
    #cursor = g.conn.execute(cmd_find_rest_by_regionid_sp % data)

    data = ("15106")
    cmd_find_rest_by_zip = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            (
                SELECT *
                FROM Region
                WHERE Zip_code = '%s'
            ) AS R INNER JOIN Belong_to USING (Region_id)
        ) INNER JOIN Restaurant USING (Restaurant_id)
    ) INNTER JOIN Review USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC"""
    #cursor = g.conn.execute(cmd_find_rest_by_zip % data)

    data = ("15106")
    cmd_find_rest_by_zip_sp = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            (
                (
                    SELECT *
                    FROM Region
                    WHERE Zip_code = '%s'
                ) AS R INNER JOIN Belong_to USING (Region_id)
            ) INNER JOIN Restaurant USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id)
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC"""

    data = (3)
    cmd_find_rest_by_feature = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
        (
            (
                SELECT *
                FROM Special_for
                WHERE Feature_id = %d
            ) AS R INNER JOIN Restaurant USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC;"""

    data = (3)
    cmd_find_rest_by_feature_sp = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            (
                SELECT *
                FROM Special_for
                WHERE Feature_id = %d
            ) AS R INNER JOIN Restaurant USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id)
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC"""

    data = (3, "61820")
    cmd_find_rest_by_feature_zip = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            SELECT *
            FROM Special_for
            WHERE Feature_id = %d
        ) AS F
        INNER JOIN
        (
            (
                (
                    SELECT *
                    FROM Region
                    WHERE Zip_code = '%s'
                ) AS R INNER JOIN Belong_to USING (Region_id)
            ) INNER JOIN Restaurant USING (Restaurant_id)
        ) USING (Restaurant_id)
    ) INNTER JOIN Review USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC"""

    data = (3, "61820")
    cmd_find_rest_by_feature_zip_sp = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            (
                SELECT *
                FROM Special_for
                WHERE Feature_id = %d
            ) AS F
            INNER JOIN
            (
                (
                    (
                        SELECT *
                        FROM Region
                        WHERE Zip_code = '%s'
                    ) AS R INNER JOIN Belong_to USING (Region_id)
                ) INNER JOIN Restaurant USING (Restaurant_id)
            ) USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id)
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC"""

    data = (3, 8)
    cmd_find_rest_by_feature_regionid = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            SELECT *
            FROM Special_for
            WHERE Feature_id = %d
        ) AS F
        INNER JOIN
        (
            (
                (
                    SELECT *
                    FROM Region
                    WHERE region_id = %d
                ) AS R INNER JOIN Belong_to USING (Region_id)
            ) INNER JOIN Restaurant USING (Restaurant_id)
        ) USING (Restaurant_id)
    ) INNTER JOIN Review USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC"""

    data = (3, 8)
    cmd_find_rest_by_feature_regionid_sp = """
SELECT Restaurant_id, Name, Addr, Url, Location, AVG(rate)
FROM
    (
        (
            (
                SELECT *
                FROM Special_for
                WHERE Feature_id = %d
            ) AS F
            INNER JOIN
            (
                (
                    (
                        SELECT *
                        FROM Region
                        WHERE region_id = %d
                    ) AS R INNER JOIN Belong_to USING (Region_id)
                ) INNER JOIN Restaurant USING (Restaurant_id)
            ) USING (Restaurant_id)
        ) INNTER JOIN Review USING (Restaurant_id)
    ) INNER JOIN Recommend USING (Restaurant_id)
GROUP BY Restaurant_id
ORDER BY AVG(rate) DESC"""

    data = (6239, 1999, "Hmmmmmm", "07/02/2015", 2)
    cmd_add_review = """INSERT INTO Review (Restaurant_id, Person_id, Comment, Date, Rate) VALUES (%d, %d, '%s', '%s', %d) RETURNING Review_id """

    data = (1)
    cmd_find_review_by_personid = """SELECT * from review where Person_id = %d order by date DESC"""

    data = (10)
    cmd_find_review_by_restid = """SELECT * from review where Restaurant_id = %d order by date DESC"""

    data = ("2016 CU Grad Fair!", "blablabla whatever", "3/8/2016","11:00")
    cmd_add_event = """INSERT INTO Event (Name, Description, EDate, ETime) VALUES ('%s','%s','%s','%s') RETURNING Event_id"""

    data = (1,1)
    cmd_add_admin_to_event = """INSERT INTO Own (Event_id, Person_id) VALUES (%d, %d)"""

    data = (1,1)
    cmd_add_member_to_event = """INSERT INTO PJoinE (Event_id, Person_id) VALUES (%d, %d)"""

    data = (99)
    cmd_find_events_i_manage = """
SELECT Event_id, Name, Description, EDate, ETime, COUNT(PJoinE.Person_id)
FROM
    (
        (SELECT Event_id FROM Own WHERE Person_id = %d) AS O
        INNER JOIN Event USING(Event_id)
    ) LEFT OUTER JOIN PJoinE USING (Event_id)
GROUP BY Event_id, Name, Description, EDate, ETime
ORDER BY EDate DESC"""


    data = (3)
    cmd_find_events_i_join = """
SELECT Event_id, Name, Description, EDate, ETime, COUNT(PJoinE.Person_id)
FROM
    (
        (SELECT Event_id FROM PJoinE WHERE Person_id = %d) AS O
        INNER JOIN Event USING(Event_id)
    ) LEFT OUTER JOIN PJoinE USING (Event_id)
GROUP BY Event_id, Name, Description, EDate, ETime
ORDER BY EDate DESC"""

    data = (1)
    cmd_find_admins_of_event = """
SELECT *
FROM
    (
        (SELECT Person_id FROM Own WHERE Event_id = %d) AS O
        INNER JOIN Person USING(Person_id)
    )"""

    data = (1)
    cmd_find_member_of_event = """
SELECT *
FROM
    (
        (SELECT Person_id FROM PJoinE WHERE Event_id = %d) AS O
        INNER JOIN Person USING(Person_id)
    )"""

