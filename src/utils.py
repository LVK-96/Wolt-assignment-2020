import json
from math import sqrt, tan, radians


def read_restaurants():
    '''Read restaurants from JSON file'''

    with open('../restaurants.json') as file:
        data = file.read()
        file.close()
        restaurants = json.loads(data)
        return restaurants['restaurants']


def match_name(query, name):
    return query in name.lower()


def match_description(query, description):
    return query in description.lower()


def match_tags(query, tags):
    tags_lower = [tag.lower() for tag in tags]
    return query in tags_lower


def match(query, restaurant):
    query = query.lower()
    return(match_name(query, restaurant['name'])
           or match_description(query, restaurant['description'])
           or match_tags(query, restaurant['tags']))


def filter_by_query(restaurants, query):
    filtered = [restaurant for restaurant in restaurants
                if match(query, restaurant)]
    return filtered


def euclidean_distance(restaurant_location, user_location):
    '''
    Calculate euclidean distance between two coordinates.
    Actually the earth is not flat, but this is accurate enough
    when we are calculating distances of a few kilometers.
    '''

    earths_ray = 6370000  # meters
    # Python trig functions use radians
    angle_between_lon = radians(abs(restaurant_location[0] - user_location[0]))
    distance_lon = earths_ray * tan(angle_between_lon)
    angle_between_lat = radians(abs(restaurant_location[1] - user_location[1]))
    distance_lat = earths_ray * tan(angle_between_lat)
    return (sqrt(pow(distance_lat, 2) + pow(distance_lon, 2)))


def is_within_max_distance(restaurant, user_location):
    max_distance = 3000  # 3000 meters
    restaurant_location = [float(location) for location
                           in restaurant['location']]
    distance = euclidean_distance(restaurant_location, user_location)
    return distance < max_distance


def filter_by_distance(restaurants, user_location):
    filtered = [restaurant for restaurant in restaurants
                if is_within_max_distance(restaurant, user_location)]
    return filtered
