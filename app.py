from flask import Flask, request
import geopandas as gpd

app = Flask(__name__)

countries = gpd.read_file('countries.geojson')

@app.route('/countries')
def get_coutries():

  country_name = request.args.get('country_name')
  feature = countries[countries['ADMIN'] == country_name]

  feature_json = feature.to_json()

  return feature_json








if __name__ == "__main__":
  app.run()
