# Wolt backend assignment 2020

Built with:

* [Python 3.8](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Pipenv](https://github.com/pypa/pipenv)
* [geopy.geodesic](https://geopy.readthedocs.io/en/stable/#geopy.distance.geodesic) (Only for validating the accuracy of a simpler distance calculation algorithm)
* [coverage](https://coverage.readthedocs.io/en/coverage-5.0.3/)
* [Docker](https://docs.docker.com/)

## Dev environment setup

Install:

* [Docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/)

Start the api

```bash
docker-compose up # api accessible at localhost:5000
```

Open `localhost:5000/restaurants/search?q=sushi&lat=60.17045&lon=24.93147` with
your browser. It should return 9 restaurants as JSON.

## Running tests

```bash
docker-compose run backend sh -c "coverage run -m unittest discover && coverage report -m"
```
