import csv, json, random

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

def export_restaurant_sql(data_dicts):
    with open("sql/restaurant.sql", "wb+") as target_sql:
        for idx, data_dict in enumerate(data_dicts):
            try:
                restaurant_id = str(idx + 1)
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
                target_sql.write(rest_sql_str)
            except UnicodeEncodeError:
                print data_dict

def csv_sql_formatter(csv_path, formatter):
    row_idx = 0
    with open(csv_path, "r") as read_csv:
        with open("sql/restaurant.sql", "wb+") as rest_sql:
            for row in read_csv:
                if row_idx == 0:
                    row_idx += 1
                else:
                    rest_sql.write(formatter(row))

def restaurant_sql_formatter(csv_data_row):
    restaurant_id, name, address, url, longitude, latitude = csv_data_row.split(',')
    if not(name[0] == '"' and name[-1] == '"'):
        name = '"' + name + '"'
    if not(address[0] == '"' and address[-1] == '"'):
        address = '"' + address + '"'
    url = "'yelp.com'"
    location = "point(" + longitude + "," + latitude + ")"
    value_str = ", ".join(restaurant_id, name, address, url, location)
    rest_sql_str = "INSERT INTO Restaurant (Restaurant_id, Name, Addr, Location) VALUES (" + value_str + ");"
    return rest_sql_str

# INSERT INTO Region (Region_id, Zip_code, NW_point, SE_point) VALUES (1, 10027, point(40.817419,73.973054), point(40.802380,73.943056));
# INSERT INTO Restaurant (Restaurant_id, Name, Addr) VALUES (1213123, 'Jin Ramen', '555 W 125 St');

if __name__ == "__main__":

    # export_restaurant_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))
    export_person_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_user.json"))
    # csv_sql_formatter('csv/restaurant.csv', restaurant_sql_formatter)
    # export_restaurant_sql(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))
