

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

def get_first_result(cursor):
	data = None
	for result in cursor:
		data = result
		break
	return data

def get_results(cursor):
	return [result for result in cursor]
