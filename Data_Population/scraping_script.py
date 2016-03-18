import csv, json, random, re

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
    with open("sql/feature.sql", "wb+") as feature_sql:
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
    zipcode_regex = ", [A-Z]{2} ([0-9]{5})"
    with open("sql/region.sql", "wb+") as target_sql:
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
        for zip_code, region_dict in region_dicts.items():
            region_id = str(idx)
            print idx, region_dict
            zip_code = zip_code
            NW_point = "point(" + str(region_dict["north"]) + ',' + str(region_dict["west"]) + ')'
            SE_point = "point(" + str(region_dict["south"]) + ',' + str(region_dict["east"]) + ')'
            region_val_str = ' ,'.join([region_id, zip_code, NW_point, SE_point])
            target_sql.write("INSERT INTO Region (Region_id, Zip_code, NW_point, SE_point) VALUES (" + region_val_str + ');\n')
            idx += 1


if __name__ == "__main__":
    # export_restaurant_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))
    # export_person_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_user.json"))
    export_restaurant_sql(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))
    # export_region_sql(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))

