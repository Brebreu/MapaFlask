from flask import Flask, jsonify, render_template, request, redirect, url_for
import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import Point
import json

app = Flask(__name__)

# Caminho para o arquivo Shapefile
SHP_FILEPATH = os.path.join('.', 'D:/Sipade/SipadeIC/AplicacaoBuscaDados/shp_merged/updated_shapefile.shp')
JSON_FILEPATH = os.path.join('.', 'propriedades_com_degradacao.json')

# Carregar os dados do arquivo JSON
with open(JSON_FILEPATH, 'r', encoding='utf-8') as f:
    data = json.load(f)["centroide_propriedade"]

def buscar_propriedades_imovel(point):
    """Busca as propriedades ['PROP_CPF'] e ['PROP'] do imóvel que contém o ponto especificado na geometria."""
    gdf = gpd.read_file(SHP_FILEPATH)
    # Filtra o GeoDataFrame para encontrar o imóvel que contém o ponto
    imovel = gdf[gdf.contains(point)]
    if not imovel.empty:
        return imovel.iloc[0]['PROP_CPF'], imovel.iloc[0]['PROP']
    return None, None  # Retorna None se não encontrado

@app.route('/', methods=['GET', 'POST'])
def index():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    return render_template('index.html', latitude=latitude, longitude=longitude, data=data)

@app.route('/limite_apa')
def limite_apa():
    gdf_limite_apa = gpd.read_file('D:/Sipade/SipadeIC/MapaQGIS/LIMITE_APA/LIMITE_APA_R2.shp')
    if gdf_limite_apa.crs != "EPSG:4326":
        gdf_limite_apa = gdf_limite_apa.to_crs("EPSG:4326")
    return jsonify(gdf_limite_apa.to_json())

@app.route('/area_do_pasto')
def area_do_pasto():
    gdf_area_do_pasto = gpd.read_file('D:/Sipade/SipadeIC/MapaQGIS/propriedades/pasto/area_do_pasto.shp')
    if gdf_area_do_pasto.crs != "EPSG:4326":
        gdf_area_do_pasto = gdf_area_do_pasto.to_crs("EPSG:4326")
    return jsonify(gdf_area_do_pasto.to_json())

@app.route('/skimmed_properties')
def skimmed_properties():
    gdf_skimmed_properties = gpd.read_file('D:/Sipade/SipadeIC/MapaQGIS/skimmed_properties/skimmed_properties.shp')
    if gdf_skimmed_properties.crs != "EPSG:4326":
        gdf_skimmed_properties = gdf_skimmed_properties.to_crs("EPSG:4326")
    return jsonify(gdf_skimmed_properties.to_json())

@app.route('/add_marker', methods=['POST'])
def add_marker():
    lat = request.form['lat']
    lon = request.form['lon']
    return redirect(url_for('index', latitude=lat, longitude=lon))

@app.route('/remove_markers', methods=['POST'])
def remove_markers():
    return jsonify(status="success")

@app.route('/buscar_proprietario', methods=['GET', 'POST'])
def buscar_proprietario():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    if latitude and longitude:
        point = Point(float(longitude), float(latitude))
        cpf, nome = buscar_propriedades_imovel(point)
        if cpf and nome:
            return render_template('result.html', cpf_prop=cpf, nome_prop=nome)
    return render_template('result.html', cpf_prop="Não encontrado", nome_prop="Não encontrado")

if __name__ == '__main__':
    app.run(debug=True)
