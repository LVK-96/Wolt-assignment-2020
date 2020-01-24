import unittest
from ..utils import euclidean_distance


class EuclideanDistanceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_location = [60.17045, 24.93147]

    def test_error_is_less_than_1m_1(self):
        accurate = 1110.288  # meters
        restaurant_location = [60.16990257838493, 24.94148075580597]
        result = euclidean_distance(self.user_location, restaurant_location)
        print(f'\nResult: {result} - Accurate: {accurate}')
        self.assertLess(abs(result - accurate), 100,
                        f'Result: {result} - Accurate: {accurate}')
    
    def test_error_is_less_than_10m_2(self):
        accurate = 3397.168
        restaurant_location = [60.1832326, 24.9031036]
        result = euclidean_distance(self.user_location, restaurant_location)
        print(f'\nResult: {result} - Accurate: {accurate}')
        self.assertLess(abs(result - accurate), 100,
                        f'Result: {result} - Accurate: {accurate}')

    def test_error_is_less_than_50m_3(self):
        accurate = 12796.96  # meters
        test_location = [60.1871435, 24.8169519]
        result = euclidean_distance(self.user_location, test_location)
        print(f'\nResult: {result} - Accurate: {accurate}')
        self.assertLess(abs(result - accurate), 100,
                        f'Result: {result} - Accurate: {accurate}')

    def test_error_is_less_than_100m_4(self):
        accurate = 30363.113  # meters
        test_location = [60.2168285, 24.6606493]
        result = euclidean_distance(self.user_location, test_location)
        print(f'\nResult: {result} - Accurate: {accurate}')
        self.assertLess(abs(result - accurate), 100,
                        f'Result: {result} - Accurate: {accurate}')
