from math import sqrt, cos, radians


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

    Based on the tests in test_euclidean_distance.py,
    done using locations in the Helsinki area
    the distances our algorithm produces are around 0.05% percent shorter
    than accurate distances calculated with geopy.
    '''
    # Circumference of a circle = 2 * pi * r, earth`s radius is ~6371km
    # -> (2 * pi * 6371) / 360 = ~111km
    length_of_a_degree = 111e3  # meters
    # locations in (lon, lat) tuple
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


def is_within_max_distance(user_location, restaurant, max_distance):
    # All distances in meters
    restaurant_location = tuple(float(location) for location
                                in restaurant['location'])
    # locations in (lon, lat) tuple
    distance = euclidean_distance(user_location, restaurant_location)
    return distance < max_distance
