from app.app import app
import unittest


class TestAPI(unittest.TestCase):
    def check_restaurant_has_all_fields(self, restaurant):
        keys = ['city', 'currency', 'delivery_price', 'description', 'image',
                'location', 'name', 'online', 'tags', 'blurhash']
        for k in keys:
            if k not in restaurant:
                return False
        return True

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_not_found(self):
        response = self.client.get('/will_not_be_found')
        self.assertEqual(response.status_code, 404)

    def test_missing_q(self):
        response = self.client.get(
            '/restaurants/search?q=&lat=60.17045&lon=24.93147'
        )
        body = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['error'], 'Missing query parameter q')

    def test_invalid_lat(self):
        response = self.client.get(
            '/restaurants/search?q=sushi&lat=100&lon=24.93147'
        )
        body = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            body['error'],
            'Query parameter lat should be a float in the range -90-90'
        )

    def test_invalid_lon(self):
        response = self.client.get(
            '/restaurants/search?q=sushi&lat=60.17045&lon=200'
        )
        body = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            body['error'],
            'Query parameter lon should be a float in the range -180-180'
        )

    def test_valid_query_no_restaurants_in_range(self):
        response = self.client.get(
            '/restaurants/search?q=sushi&lat=30.12343&lon=10.93147'
        )
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body), 0)

    def test_valid_query_no_matching_restaurants(self):
        response = self.client.get(
            '/restaurants/search?q=eivarmastimatchaa&lat=60.17045&lon=24.93147'
        )
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body), 0)

    def test_valid_quefy_that_has_a_mathcing_restaurant(self):
        response = self.client.get(
            '/restaurants/search?q=momotoko&lat=60.17045&lon=24.93147'
        )
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body), 1)
        self.assertTrue(self.check_restaurant_has_all_fields(body[0]))
        self.assertTrue(body[0]['name'] == 'Momotoko Citycenter')

    def test_valid_query_that_has_mathcing_restaurants(self):
        response = self.client.get(
            '/restaurants/search?q=sushi&lat=60.17045&lon=24.93147'
        )
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body), 9)
        for r in body:
            self.assertTrue(self.check_restaurant_has_all_fields(r))
