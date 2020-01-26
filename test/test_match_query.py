import unittest
from app.match_query import match_query
from .mocks import mock_restaurants


class MatchQueryTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_restaurants = mock_restaurants

    def test_äijä_should_match_second_restaurant(self):
        self.assertTrue(match_query('äijä', self.mock_restaurants[1]))

    def test_äijä_should_not_match_first_and_third_restaurant(self):
        self.assertFalse(match_query('äijä', self.mock_restaurants[0]))
        self.assertFalse(match_query('äijä', self.mock_restaurants[2]))

    def test_burger_should_not_match_any_restaurant(self):
        for r in self.mock_restaurants:
            self.assertFalse(match_query('burger', r))

    def test_o_should_match_every_restaurant(self):
        for r in self.mock_restaurants:
            self.assertTrue(match_query('o', r))

    def test_makaroo_should_match_third_restaurant(self):
        self.assertTrue(
            match_query('makaroo', self.mock_restaurants[2])
        )

    def test_makaroonia_should_not_match_any_restaurant(self):
        for r in self.mock_restaurants:
            self.assertFalse(match_query('makaroonia', r))

    def test_motoko_should_match_first_restaurant(self):
        self.assertTrue(match_query('motoko', self.mock_restaurants[0]))

    def test_oujee_should_match_third_restaurant(self):
        self.assertTrue(
            match_query('oujee', self.mock_restaurants[2])
        )
