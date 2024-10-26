from flask import Flask, request, jsonify
import requests, json
app = Flask(__name__)
#Opening file with campus places and corresponding lat & long
with open ("campus_places.json") as f:
        campus_places = json.load(f)

API_KEY = 'AIzaSyAH_H3VJ-DDJPk_i_8LIojnfhfNtaY8DB4'
@app.route('/campus_places', methods = ['GET'])
def get_campus_places():
    return jsonify(campus_places)

@app.route('/directions', methods = ['GET'])
def get_directions():
    # start = request.args.get('start')
    # end = request.args.get('end')
    start = "library"
    end = "usu"

    params = {
        "origin":start,
        "destination":end,
        "key": API_KEY
    }


    #Make a request to Google API
    try:
        goog_map_response = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=params)
        goog_map_response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.HTTPError as err:
        return jsonify({'error': str(err)}), 500
    goog_map_response = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?destination={end}&origin={start}&key={API_KEY}')

    # # Check if request was successful
    # if goog_map_response.status_code != 200:
    #     return f'Error: Your request was unsuccessful.'
    # else:
    #     directions_data = goog_map_response.json() #dictionary
    #     steps = directions_data['routes'][0]['legs'][0]['steps']
    #     directions = [step['html_directions'] for step in steps]
    #     return jsonify(directions)





if __name__ == '__main__':
    app.run(debug=True)
