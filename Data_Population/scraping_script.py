import csv, json, random

def yelp_json_dict_transformer(json_file_path):
    with open(json_file_path) as json_file:
        data = json.loads(json_file.read())
    return data

def export_restaurant_csv(data_dicts):
    with open("csv/restaurant.csv", "wb+") as target_csv:
        dict_writer = csv.DictWriter(target_csv, fieldnames=['name', 'address', 'stars', 'longitude', 'latitude'])
        dict_writer.writeheader()
        for data_dict in data_dicts:
            try:
                dict_writer.writerow(                                                        \
                                        {                                                    \
                                                'name' : data_dict['name'],                  \
                                                'address' : data_dict['full_address'].replace('\n', ' '),\
                                                'stars' : float(data_dict['stars']),         \
                                                'longitude' : float(data_dict['longitude']), \
                                                'latitude' : float(data_dict['latitude'])    \
                                        }                                                    \
                                    )
            except UnicodeEncodeError:
                print data_dict

def export_person_csv(data_dicts):
    with open("csv/person.csv", "wb+") as target_csv:
        dict_writer = csv.DictWriter(target_csv, fieldnames=['name', 'email', 'gender', 'age'])
        dict_writer.writeheader()
        for data_dict in data_dicts:
            try:
                dict_writer.writerow(                                                        \
                                        {                                                    \
                                                'name' : data_dict['name'],                  \
                                                'email' : data_dict['name'].lower() + "@gmail.com",\
                                                'gender' : random.choice(['Male', 'Female', 'None']),         \
                                                'age' : random.randint(10, 50) \
                                        }                                                    \
                                    )
            except UnicodeEncodeError:
                print data_dict


if __name__ == "__main__":
    export_restaurant_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_business.json"))
    export_person_csv(yelp_json_dict_transformer("YelpDataset/yelp_academic_dataset_user.json"))
