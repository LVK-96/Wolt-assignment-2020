import json
from .match_query import match_query
from .distance import is_within_max_distance


def read_restaurants():
    with open('./static/restaurants.json') as file:
        data = file.read()
        file.close()
        restaurants = json.loads(data)
        return restaurants['restaurants']


def validate_latitude(latitude):
    try:
        latitude = float(latitude)
        return abs(latitude) <= 90
    except ValueError:
        return False


def validate_longitude(longitude):
    try:
        longitude = float(longitude)
        return abs(longitude) <= 180
    except ValueError:
        return False


def filter_by_query_and_distance(query, location, restaurants):
    return [restaurant for restaurant in restaurants
            if match_query(query, restaurant)
            # Restaurant should also be within 3000 meters
            and is_within_max_distance(location, restaurant, 3000)]
