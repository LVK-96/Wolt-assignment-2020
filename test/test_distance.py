import unittest
import random
from unittest.mock import patch
from geopy.distance import geodesic
from app.utils import read_restaurants
from app.distance import euclidean_distance, is_within_max_distance


class EuclideanDistanceTestCase(unittest.TestCase):
    '''
    Spec the distance calculation to have a maxium acceptable error of 1%
    (30m on a distance of 3000m).

    The algorithm is validated against geopy's geodesic distance
    https://geopy.readthedocs.io/en/stable/#module-geopy.distance
    '''
    def setUp(self):
        self.user_location = (24.93147, 60.17045)
        self.error_threshold = 0.01

    def calculate_error(self, restaurant_location):
        # Our algortihm takes coords in (lon, lat) tuple
        result = euclidean_distance(
            self.user_location, restaurant_location
        )
        accurate_result = geodesic(
            # geopy uses the opposite coordinate order
            tuple(restaurant_location[::-1]), tuple(self.user_location[::-1])
        ).meters
        err = abs(result - accurate_result) / accurate_result
        return err

    def test_error_is_less_than_1percent_1000m_distance(self):
        restaurant_location = (24.94148075580597, 60.16990257838493)
        err = self.calculate_error(restaurant_location)
        self.assertLess(err, self.error_threshold)

    def test_error_is_less_than_1percent_3000m_distance(self):
        restaurant_location = (24.9031036, 60.1832326)
        err = self.calculate_error(restaurant_location)
        self.assertLess(err, self.error_threshold)

    def test_error_is_less_than_1percent_12000m_distance(self):
        restaurant_location = (24.8169519, 60.1871435)
        err = self.calculate_error(restaurant_location)
        self.assertLess(err, self.error_threshold)

    def test_error_is_less_than_1percent_30000m_distance(self):
        restaurant_location = (24.6606493, 60.2168285)
        err = self.calculate_error(restaurant_location)
        self.assertLess(err, self.error_threshold)

    def test_error_is_less_than_1percent_for_all_in_restaurantsjson(self):
        restaurants = read_restaurants()
        locations = [restaurant['location'] for restaurant in restaurants]
        longitudes = [float(location[0]) for location in locations]
        latitudes = [float(location[1]) for location in locations]
        lon_min = min(longitudes)
        lon_max = max(longitudes)
        lat_min = min(latitudes)
        lat_max = max(latitudes)
        for l in locations:
            # Choose random lon and lat from the range of the locations
            # in restaurants.json
            new_lon = random.uniform(lon_min, lon_max)
            new_lat = random.uniform(lat_min, lat_max)
            self.user_location = (new_lon, new_lat)
            err = self.calculate_error(tuple(float(location) for
                                             location in l))
            self.assertLess(err, self.error_threshold)


class IsWithinMaxDistanceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_location = (0, 0)
        self.restaurant = {'location': [90, 90]}

    @patch('app.distance.euclidean_distance', return_value=4000)
    def test_return_false_when_distance_is_over_max(self, distance_function):
        self.assertFalse(
            is_within_max_distance(self.user_location, self.restaurant, 3000)
        )

    @patch('app.distance.euclidean_distance', return_value=2000)
    def test_return_true_when_distance_is_under_max(self, distance_function):
        self.assertTrue(
            is_within_max_distance(self.user_location, self.restaurant, 3000)
        )

    @patch('app.distance.euclidean_distance', return_value=3000)
    def test_return_false_when_distances_are_equal(self, distance_function):
        self.assertFalse(
            is_within_max_distance(self.user_location, self.restaurant, 3000)
        )
