from flask import Flask, send_file, Response
import geopandas as gpd
import matplotlib.pyplot as plt

from io import BytesIO 

world_data = gpd.read_file('countries.geojson')
app = Flask(__name__)

@app.route('/shapes/<slug>')
def getShapes(slug):
  feature = world_data[world_data['ADMIN'] == slug]
  feature_json = feature.to_json()

  res = Response(feature_json, mimetype='application/json')

  return res

@app.route('/<slug>') # Route
def getHome(slug): # Fonction a declancher une fois l'utilisateur visite /<pays>
  feature = world_data[world_data['ADMIN'] == slug]
  feature.plot()
  img_stream = BytesIO()
  plt.savefig(img_stream, format="png")
  img_stream.seek(0)
  plt.close()
  
  return send_file(img_stream, mimetype='image/png') # Envoyer une reponse a l'utilisateur

if __name__ == "__main__":
  app.run(port=5000)
