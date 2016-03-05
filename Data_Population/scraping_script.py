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
            try:
                dict_writer.writerow(                                                        \
                                        {                                                    \
                                                'person_id' : idx + 1,            \
                                                'name' : data_dict['name'],                  \
                                                'email' : data_dict['name'].lower() + "@gmail.com",\
                                                'gender' : random.choice(['male', 'female']),         \
                                                'age' : random.randint(10, 50) \
                                        }                                                    \
                                    )
            except UnicodeEncodeError:
                print data_dict


if __name__ == "__main__":
    export_restaurant_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))
    export_person_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_user.json"))
