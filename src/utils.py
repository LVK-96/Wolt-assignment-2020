import json
from math import sqrt, cos, radians


def read_restaurants():
    '''Read restaurants from JSON file'''

    with open('../restaurants.json') as file:
        data = file.read()
        file.close()
        restaurants = json.loads(data)
        return restaurants['restaurants']


def validate_latitude(latitude):
    try:
        latitude = float(latitude)
        return latitude <= 90 and latitude >= -90
    except ValueError:
        return False


def validate_longitude(longitude):
    try:
        longitude = float(longitude)
        return longitude <= 180 and longitude >= -180
    except ValueError:
        return False


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


def euclidean_distance(user_location, restaurant_location):
    '''
    Calculate euclidean distance between two coordinates
    using the length of a degree of latitude and longitude.
    Naturally, this is isn't the most accurate method,
    but it is accurate enough when we are calculating distances
    of a few kilometers.

    Helpful links to understand how this works:
    https://jonisalonen.com/2014/computing-distance-between-coordinates-can-be-simple-and-fast/
    https://en.wikipedia.org/wiki/Meridian_arc
    https://en.wikipedia.org/wiki/Latitude#Length_of_a_degree_of_latitude
    '''
    # Circumference of a circle = 2 * pi * r, earth`s radius is ~6371km
    # -> (2 * pi * 6371) / 360 = ~111km
    length_of_a_degree = 111e3  # meters
    distance_lon = restaurant_location[0] - user_location[0]
    distance_lat = restaurant_location[1] - user_location[1]

    # Scale angle in longitutde with the cosine of latitude.
    # This way we account for the length of a degree of longitude
    # variaiting between ~111km at the equator and 0km at the poles.
    distance_lon_scaled = distance_lon * cos(radians(restaurant_location[1]))

    # Calculate euclidean distance in degrees and multiply by the length of
    # a degree to get the distance in meters
    return length_of_a_degree * sqrt(distance_lon_scaled * distance_lon_scaled
                                     + distance_lat * distance_lat)


def is_within_max_distance(user_location, restaurant):
    '''
    Check that user location is within 3km of restaurant
    '''
    max_distance = 3000  # meters
    restaurant_location = [float(location) for location
                           in restaurant['location']]
    distance = euclidean_distance(user_location, restaurant_location)
    return distance < max_distance


def filter_by_query_and_distance(query, location, restaurants):
    return [restaurant for restaurant in restaurants
            if match(query, restaurant)
            and is_within_max_distance(location, restaurant)]
