from flask import Flask, request, jsonify, g
from utils import (
    read_restaurants, filter_by_query_and_distance, validate_latitude,
    validate_longitude
)


app = Flask(__name__)
@app.before_first_request
def load_restaurants():
    '''
    Store restaurants in global variable
    so we don't need to do unnecessary disk I/O
    '''
    g.restaurants = read_restaurants()


@app.errorhandler(400)
def bad_request(error_message):
    return jsonify({'error': error_message}), 400


@app.route('/restaurants/search')
def restaurants():
    query = request.args.get('q')
    if (not query):
        return bad_request('Missing query parameter q')

    latitude = request.args.get('lat')
    if (not latitude):
        return bad_request('Missing query parameter lat')

    if (not validate_latitude(latitude)):
        return bad_request(
            'Query parameter lat should be a float in the range -180-180'
        )

    longitude = request.args.get('lon')
    if (not longitude):
        return bad_request('Missing query parameter lon')

    if (not validate_longitude(longitude)):
        return bad_request(
            'Query parameter lon should be a float in the range 0-90'
        )

    location = [float(longitude), float(latitude)]
    filtered_restaurants = filter_by_query_and_distance(query, location,
                                                        g.restaurants)
    return jsonify(filtered_restaurants)
