import csv, json, random, re, time

def yelp_json_dict_transformer(json_file_path):
    with open(json_file_path) as json_file:
        data = json.loads(json_file.read())
    return data

def export_restaurant_csv(data_dicts):
    with open("csv/restaurant.csv", "wb+") as target_csv:
        dict_writer = csv.DictWriter(target_csv, fieldnames=['restaurant_id', 'name', 'address', 'url', 'longitude', 'latitude'])
        dict_writer.writeheader()
        for idx, data_dict in enumerate(data_dicts):
            try:
                dict_writer.writerow(                                                        \
                                        {                                                    \
                                                'restaurant_id' : idx + 1,   \
                                                'name' : data_dict['name'],                  \
                                                'address' : data_dict['full_address'].replace('\n', ' '),\
                                                'url' : '',         \
                                                'longitude' : float(data_dict['longitude']), \
                                                'latitude' : float(data_dict['latitude'])    \
                                        }                                                    \
                                    )
            except UnicodeEncodeError:
                print data_dict

def export_person_csv(data_dicts):
    with open("csv/person.csv", "wb+") as target_csv:
        dict_writer = csv.DictWriter(target_csv, fieldnames=['person_id', 'name', 'email', 'gender', 'age'])
        dict_writer.writeheader()
        for idx, data_dict in enumerate(data_dicts):
            if idx == 2000:
                return
            try:
                dict_writer.writerow(                                                        \
                                        {                                                    \
                                                'person_id' : idx + 1,            \
                                                'name' : data_dict['name'],                  \
                                                'email' : data_dict['name'][:2].lower() + "@columbia.edu",\
                                                'gender' : random.choice(['male', 'female']),         \
                                                'age' : random.randint(10, 50) \
                                        }                                                    \
                                    )
            except UnicodeEncodeError:
                print data_dict

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y', prop)

def export_review_sql():
    with open("sql/review.sql", "wb+") as review_sql:
        for _ in xrange(50000):
            person_id = str(random.choice(xrange(1, 2001)))
            restaurant_id = str(random.choice(xrange(0, 20324)))
            comment = "'Hmmmm'"
            date = "'" + randomDate("1/1/2015", "3/20/2016", random.random()) + "'"
            star = str(random.choice(xrange(1, 6)))

            review_str = ', '.join([restaurant_id, person_id, comment, date, star])
            review_sql_str = "INTO Review (Restaurant_id, Person_id, Comment, Date, Rate) VALUES (" + review_str + ");\n"

            review_sql.write(review_sql_str)

def export_restaurant_sql(data_dicts):
    with open("sql/restaurant.sql", "wb+") as restaurant_sql:
        restaurant_idx = 0
        for data_dict in data_dicts:
            if 'Restaurants' in data_dict['categories']:
                try:
                    restaurant_id = str(restaurant_idx)
                    name = data_dict['name'].replace("'", '')
                    if not(name[0] == '"' and name[-1] == '"'):
                        name = "'" + name + "'"
                    address = data_dict['full_address'].replace('\n', ' ').replace("'", '')
                    if not(address[0] == '"' and address[-1] == '"'):
                        address = "'" + address + "'"
                    url = "'yelp.com'"
                    location = 'point(' + str(float(data_dict['longitude'])) + ', ' + str(float(data_dict['latitude'])) + ')'
                    value_str = ", ".join([restaurant_id, name, address, url, location])
                    rest_sql_str = "INSERT INTO Restaurant (Restaurant_id, Name, Addr, Url, Location) VALUES (" + value_str + ");\n"
                    restaurant_idx += 1
                    restaurant_sql.write(rest_sql_str)
                except UnicodeEncodeError:
                    restaurant_idx -= 1
                    print data_dict

def export_region_sql(data_dicts):
    with open("sql/region.sql", "wb+") as region_sql:
        zipcode_regex = ", [A-Z]{2} ([0-9]{5})"
        region_dicts = {}
        for data_dict in data_dicts:
            try:
                match_obj = re.search(zipcode_regex, data_dict["full_address"].replace('\n', ' '))
                zip_code = match_obj.group(1)
                longitude, latitude = float(data_dict["longitude"]), float(data_dict["latitude"])
                if region_dicts.get(zip_code):
                    if latitude > region_dicts[zip_code]["north"]:
                        region_dicts[zip_code]["north"] = latitude
                    if latitude < region_dicts[zip_code]["south"]:
                        region_dicts[zip_code]["south"] = latitude
                    if longitude > region_dicts[zip_code]["east"]:
                        region_dicts[zip_code]["east"] = longitude
                    if longitude < region_dicts[zip_code]["west"]:
                        region_dicts[zip_code]["west"] = longitude
                else:
                    region_dicts[zip_code] = {}
                    region_dicts[zip_code]["north"] = latitude
                    region_dicts[zip_code]["south"] = latitude
                    region_dicts[zip_code]["west"] = longitude
                    region_dicts[zip_code]["east"] = longitude
            except AttributeError, UnicodeEncodeError:
                print data_dict
        idx = 0
        zipcode_dict = {}
        for zip_code, region_dict in region_dicts.items():
            region_id = str(idx)
            zipcode_dict[zip_code] = region_id
            NW_point = "point(" + str(region_dict["north"]) + ',' + str(region_dict["west"]) + ')'
            SE_point = "point(" + str(region_dict["south"]) + ',' + str(region_dict["east"]) + ')'
            region_val_str = ' ,'.join([region_id, zip_code, NW_point, SE_point])
            region_sql.write("INSERT INTO Region (Region_id, Zip_code, NW_point, SE_point) VALUES (" + region_val_str + ');\n')
            idx += 1

        restaurant_sql = open("sql/restaurant.sql", "r")
        belong_to_sql = open("sql/belong_to.sql", "wb+")

        for restaurant_line in restaurant_sql:
            match_id_obj = re.search("\) VALUES \((\d+),", restaurant_line)
            match_zipcode_obj = re.search(zipcode_regex, restaurant_line)
            if match_zipcode_obj and match_id_obj:
                restaurant_id, zip_code = match_id_obj.group(1), match_zipcode_obj.group(1)
                if zipcode_dict.get(zip_code):
                    region_id = zipcode_dict.get(zip_code)
                    belong_to_str = "INSERT INTO Belong_to (Restaurant_id, Region_id) VALUES (" + restaurant_id + ',' + region_id + ");\n"
                    belong_to_sql.write(belong_to_str)

        restaurant_sql.close()
        belong_to_sql.close()

if __name__ == "__main__":
    # export_restaurant_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))
    # export_person_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_user.json"))
    # export_restaurant_sql(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))
    # export_region_sql(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))
    export_review_sql()

