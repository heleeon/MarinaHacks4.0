from flask import Flask, request, jsonify
import requests, json
app = Flask(__name__)
#Opening file with campus places and corresponding lat & long
with open ("campus_places.json") as f:
        campus_places = json.load(f)

API_KEY = 'AIzaSyCLCPDVcLovQkWDYM8BRNBV-VLA7vNwsxA'
@app.route('/campus_places', methods = ['GET'])
def get_campus_places():
    return jsonify(campus_places)

@app.route('/directions', methods = ['GET'])
def get_directions():
    origin = request.args.get('start')
    destination = request.args.get('end')

    # # TEST: Use the provided lat/lng directly
    # origin = "33.77720918736128,-118.11455548486778"
    # destination = "33.78047261891716,-118.11397538002423"
    # origin_lat, origin_long = origin.split(',')
    # destination_lat, destination_long = destination.split(',')
    # url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_lat},{origin_long}&destination={destination_lat},{destination_long}&key={API_KEY}"

    # Use Google Maps Directions API
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}"

    # Make a request to Google API
    try:
        goog_map_response = requests.get(url)
        # goog_map_response = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=params)
        goog_map_response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.HTTPError as err:
        return jsonify({'error': str(err)}), 500
    goog_map_response = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?destination={destination}&origin={origin}&mode=walking&key={API_KEY}')

    # Check if request went through
    if goog_map_response.status_code == 200:
        # If yes, save the data response to directions_data
        directions_data = goog_map_response.json()
        # return jsonify(directions_data)
    else:
        return jsonify({'error': 'Failed to retrieve directions'}), goog_map_response.status_code

    # If status is not found in directions_data
    if directions_data['status'] != 'OK':
        return jsonify({"error": "Unable to find directions"}),
    else:
        steps = directions_data['routes'][0]['legs'][0]['steps']
        directions = [step['html_instructions'] for step in steps]
        return jsonify(directions)

if __name__ == '__main__':
    app.run(debug=True)
