from flask import Flask, send_file, Response
import geopandas as gpd
import matplotlib.pyplot as plt
from flask_cors import CORS, cross_origin

from io import BytesIO 

# Load your GeoDataFrame or GeoJSON file
# Replace 'countries.geojson' with the path to your shapefile or GeoJSON file
world_data = gpd.read_file('countries.geojson')
app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/demo', methods=['GET'])
def selize_query(slug):
  name = request.args.get('name')
  age = request.args.get('age')
  #return f'Bonjour {name}, votre avez {age} ans, vous etes sur la page {slug}'
  return jsonify({slug: name, age: age})

@app.route('/shapes/<slug>')
@cross_origin(origin='*', supports_credentials=True)
def getShapes(slug):
  # Filter the GeoDataFrame based on the provided shape_id
  feature = world_data[world_data['ADMIN'] == slug]
  feature_json = feature.to_json()

  # Check if the requested feature_id exists
  if feature.empty:
      return jsonify({'error': 'Feature not found'}), 404

  res = Response(feature_json, status=201, mimetype='application/geo+json')

  # Convert the GeoDataFrame to GeoJSON format
  #return jsonify(shape_json)
  return res

@app.route('/<slug>') # Route
def getHome(slug): # Fonction a declancher une fois l'utilisateur visite /<pays>
  # Filter the GeoDataFrame to get the specific feature
  feature = world_data[world_data['ADMIN'] == slug]
  # Plot the feature
  feature.plot()

  # Save the plot to a BytesIO object
  img_stream = BytesIO()
  plt.savefig(img_stream, format="png")
  img_stream.seek(0)

  # Close the plot to free up resources
  plt.close()

  # Return the PNG image as a response
  return send_file(img_stream, mimetype='image/png') # Envoyer une reponse a l'utilisateur

'''
@app.route('/search')
def search_countries():
  query = request.args.get('q', '').lower()

  # Filter countries based on the search query
  matching_countries = gdf[gdf['ADMIN'].str.lower().str.contains(query)]

  # Optional: Convert to a standard CRS for compatibility
  matching_countries = matching_countries.to_crs(epsg='4326')  

  # Convert GeoDataFrame to a GeoJSON string
  geojson_str = matching_countries.to_json()

  return geojson_str
'''

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == "__main__":
  app.run(port=5000)
