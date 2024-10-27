from flask import Flask, request, jsonify, render_template
import requests, json
app = Flask(__name__)
#Opening file with campus places and corresponding lat & long
with open ("campus_places.json") as f:
        campus_places = json.load(f)

API_KEY = 'AIzaSyCLCPDVcLovQkWDYM8BRNBV-VLA7vNwsxA'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/campus_places', methods = ['GET'])
def get_campus_places():
    return jsonify(campus_places)

@app.route('/directions', methods = ['GET'])
def get_directions():
    start_name = request.args.get('start')
    end_name = request.args.get('end')

    # # Testing
    # start_name = 'Go Beach'
    # end_name = 'V Cafe'

    start_location = None
    for place in campus_places:
        if place['name'] == start_name:
            start_location = place['location']
            break
    end_location = None
    for place in campus_places:
        if place['name'] == end_name:
            end_location = place['location']
            break

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_location['lat']},{start_location['long']}&destination={end_location['lat']},{end_location['long']}&mode=driving&key={API_KEY}"

    # Make a request to Google MAPS API
    try:
        goog_map_response = requests.get(url)
        goog_map_response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.HTTPError as err:
        return jsonify({'error': str(err)}), 500

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
