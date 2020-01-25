import unittest
from unittest.mock import patch
from app.utils import (
    validate_latitude, validate_longitude, filter_by_query_and_distance
)
from .mocks import mock_restaurants


class TestValidateLatitudeTestCase(unittest.TestCase):
    def test_invalid_latitude_minus_100(self):
        self.assertFalse(validate_latitude(-100))

    def test_invalid_latitude_100(self):
        self.assertFalse(validate_latitude(100))

    def test_valid_latitude_minus_60(self):
        self.assertTrue(validate_latitude(-60))

    def test_valid_latitude_60(self):
        self.assertTrue(validate_latitude(60))

    def test_valid_latitude_edge_case_minus_90(self):
        self.assertTrue(validate_latitude(-90))

    def test_valid_latitude_edge_case_90(self):
        self.assertTrue(validate_latitude(90))


class TestValidateLongitudeTestCase(unittest.TestCase):
    def test_invalid_longitude_minus_200(self):
        self.assertFalse(validate_longitude(-200))

    def test_invalid_longitude_200(self):
        self.assertFalse(validate_longitude(200))

    def test_valid_longitude_minus_120(self):
        self.assertTrue(validate_longitude(-120))

    def test_valid_longitude_120(self):
        self.assertTrue(validate_longitude(120))

    def test_valid_longitude_edge_case_minus_180(self):
        self.assertTrue(validate_longitude(-180))

    def test_valid_longitude_edge_case_180(self):
        self.assertTrue(validate_longitude(180))


class TestFilterByQueryAndDistance(unittest.TestCase):
    def setUp(self):
        self.mock_restaurants = mock_restaurants

    @patch('app.utils.is_within_max_distance', return_value=True)
    @patch('app.utils.match_query', return_value=True)
    def test_matches_query_and_is_within_max_distance(
        self, query_funciton, distance_function
    ):
        result = filter_by_query_and_distance(
            'test', (0, 0), self.mock_restaurants
        )
        self.assertEqual(self.mock_restaurants, result)

    @patch('app.utils.is_within_max_distance', return_value=False)
    @patch('app.utils.match_query', return_value=True)
    def test_match_query_and_is_not_within_max_distance(
        self, query_funciton, distance_function
    ):
        result = filter_by_query_and_distance(
            'test', (0, 0), self.mock_restaurants
        )
        self.assertNotEqual(self.mock_restaurants, result)

    @patch('app.utils.is_within_max_distance', return_value=True)
    @patch('app.utils.match_query', return_value=False)
    def test_doesnt_match_query_and_is_within_max_distance(
        self, query_funciton, distance_function
    ):
        result = filter_by_query_and_distance(
            'test', (0, 0), self.mock_restaurants
        )
        self.assertNotEqual(self.mock_restaurants, result)

    @patch('app.utils.is_within_max_distance', return_value=False)
    @patch('app.utils.match_query', return_value=False)
    def test_doesnt_match_query_and_is_not_within_max_distance(
        self, query_funciton, distance_function
    ):
        result = filter_by_query_and_distance(
            'test', (0, 0), self.mock_restaurants
        )
        self.assertNotEqual(self.mock_restaurants, result)
