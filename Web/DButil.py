def get_first_result(cursor):
	data = None
	for result in cursor:
		data = result
		break
	return data
