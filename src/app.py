from flask import Flask, request, jsonify
from utils import read_restaurants, filter_by_query, filter_by_distance


app = Flask(__name__)
restaurants = []


@app.before_first_request
def load_restaurants():
    '''
    Store restaurants in global variable
    so we don't need to do unnecessary disk I/O
    '''

    global restaurants
    restaurants = read_restaurants()


@app.route('/restaurants/search')
def restaurants():
    global restaurants
    query = request.args.get('q')
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    location = [float(longitude), float(latitude)]
    filtered_restaurants = filter_by_query(restaurants, query)
    filtered_restaurants = filter_by_distance(restaurants, location)
    return jsonify(filtered_restaurants)
