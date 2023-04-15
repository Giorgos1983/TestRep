from flask import Flask, jsonify, abort
import logging
import random
import time

app = Flask(__name__)

# The data to be returned for each endpoint and id
PEOPLE_DATA = {"name": "Luke Skywalker", "height": "172", "mass": "77", "hair_color": "blond", "skin_color": "fair", "eye_color": "blue", "birth_year": "19BBY", "gender": "male"}
PLANETS_DATA = {"name": "Tatooine", "rotation_period": "23", "orbital_period": "304", "diameter": "10465", "climate": "arid", "gravity": "1 standard", "terrain": "desert", "surface_water": "1", "population": "200000"}
STARSHIPS_DATA = {"name": "X-wing", "model": "T-65B X-wing", "manufacturer": "Incom Corporation", "cost_in_credits": "149999", "length": "12.5", "max_atmosphering_speed": "1050", "crew": "1", "passengers": "0", "cargo_capacity": "110", "consumables": "1 week", "hyperdrive_rating": "1.0", "MGLT": "100", "starship_class": "Starfighter"}

# Define the URL patterns for the three endpoints
ENDPOINT_URLS = {
    'people': 'api/people/{}/',
    'planets': 'api/planets/{}/',
    'starships': 'api/starships/{}/'
}

# Dictionary that maps each category to its corresponding data dictionary
DATA_DICTS = {
    'people': PEOPLE_DATA,
    'planets': PLANETS_DATA,
    'starships': STARSHIPS_DATA
}

logging.basicConfig(filename='server.log', level=logging.INFO)

@app.route('/<category>/<int:id>/', methods=['GET'])
def get_swapi_data(category, id):
    # Add a random small delay between 0.1 and 0.5 seconds
    time.sleep(random.uniform(0.1, 0.5))

    if id > 100:
        # error_message = {'error': f'{category} with ID {id} not found'}
        abort(404, description=f'{category} with ID {id} not found')
        logging.info(f'Request: /{category}/{id}/ - 404 Not Found')

    # Check if the category is recognized and return the corresponding data dictionary
    if category in DATA_DICTS:
        return jsonify(DATA_DICTS[category])

    # Return a 404 error if the category is not recognized
    error_message = {'error': f'Category {category} not found'}
    return jsonify(error_message), 404

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(port=8090, debug=True)
