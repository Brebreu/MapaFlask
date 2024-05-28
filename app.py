from flask import Flask, render_template, jsonify, request
import folium
import pandas as pd
import geopandas as gpd

app = Flask(__name__)

# Carregar os dados do arquivo Excel
data = pd.read_excel('propriedades_com_degradacao.xlsx', engine='openpyxl')

@app.route('/')
def index():
    map_obj = folium.Map(location=[-19.7448, -47.9388], zoom_start=10)

    # Adicionar diferentes camadas de base
    folium.TileLayer('OpenStreetMap').add_to(map_obj)
    folium.TileLayer('CartoDB positron', attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(map_obj)
    folium.TileLayer('CartoDB dark_matter', attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(map_obj)
    folium.TileLayer('Esri WorldImagery', attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community').add_to(map_obj)

    # Criar grupos de camadas
    limites_group = folium.FeatureGroup(name='Limites APA')
    area_pasto_group = folium.FeatureGroup(name='Área de Pasto')
    car_group = folium.FeatureGroup(name='CAR')
    marcadores_group = folium.FeatureGroup(name='Centroides')  
    user_markers_group = folium.FeatureGroup(name='User Markers')

    # Adicionar marcadores para cada ponto
    for index, row in data.iterrows():
        lat = float(str(row['Centroide_Prop_y']).replace(',', '.'))
        lon = float(str(row['Centroide_Prop_x']).replace(',', '.'))
        popup_text = f"""
            CÓDIGO_IMOVEL: {row['CÓDIGO_IMOVEL']}<br>
            NUM_MODULO: {row['NUM_MODULO']}<br>
            SITUAÇÃO: {row['SITUAÇÃO']}<br>
            IMÓVEL: {row['IMÓVEL']}<br>
            CPF DO(S) PROPRIETÁRIO(S): {row['CPF DO(S) PROPRIETÁRIO(S)']}<br>
            PROPRIETÁRIO: {row['PROPRIETÁRIO']}<br>
            Área_propriedade (ha): {row['Área_propriedade (ha)']}<br>
            Área_degradada_APA (ha): {row['Área_degradada_APA (ha)']}<br>
            % Degradado: {row['% Degradado']}<br>
            Centroide_Prop_x: {row['Centroide_Prop_x']}<br>
            Centroide_Prop_y: {row['Centroide_Prop_y']}
        """
        folium.CircleMarker([lat, lon], radius=4, color='red', fill=True, fill_color='red', fill_opacity=0.6, popup=popup_text).add_to(marcadores_group)

    # Carregar os shapefiles e convertê-los para GeoJSON
    gdf_limite_apa = gpd.read_file('D:/Sipade/SipadeIC/MapaQGIS/LIMITE_APA/LIMITE_APA_R2.shp')
    if gdf_limite_apa.crs != "EPSG:4326":
        gdf_limite_apa = gdf_limite_apa.to_crs("EPSG:4326")
    gdf_limite_apa['geometry'] = gdf_limite_apa['geometry'].simplify(0.001)
    geojson_data = gdf_limite_apa.to_json()

    gdf_area_do_pasto = gpd.read_file('D:/Sipade/SipadeIC/MapaQGIS/propriedades/pasto/area_do_pasto.shp')
    if gdf_area_do_pasto.crs != "EPSG:4326":
        gdf_area_do_pasto = gdf_area_do_pasto.to_crs("EPSG:4326")
    geojson_data2 = gdf_area_do_pasto.to_json()

    gdf_skimmed_properties = gpd.read_file('D:/Sipade/SipadeIC/MapaQGIS/skimmed_properties/skimmed_properties.shp')
    if gdf_skimmed_properties.crs != "EPSG:4326":
        gdf_skimmed_properties = gdf_skimmed_properties.to_crs("EPSG:4326")
    geojson_data3 = gdf_skimmed_properties.to_json()

    # Adicionar camadas GeoJSON aos grupos de camadas
    folium.GeoJson(geojson_data, name='Limites APA').add_to(limites_group)
    folium.GeoJson(geojson_data2, name='Área de Pasto', style_function=lambda x: {'fillColor': 'green', 'color': 'green'}).add_to(area_pasto_group)
    folium.GeoJson(geojson_data3, name='CAR', style_function=lambda x: {'fillColor': 'gray', 'color': 'gray'}).add_to(car_group)

    # Adicionar grupos de camadas ao mapa
    limites_group.add_to(map_obj)
    area_pasto_group.add_to(map_obj)
    car_group.add_to(map_obj)
    marcadores_group.add_to(map_obj)
    user_markers_group.add_to(map_obj)

    # Adicionar controle de camadas
    folium.LayerControl().add_to(map_obj)

    return render_template('index.html', map_html=map_obj._repr_html_())

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
    lat = float(request.form['lat'])
    lon = float(request.form['lon'])
    return jsonify(status="success", lat=lat, lon=lon)

@app.route('/remove_markers', methods=['POST'])
def remove_markers():
    return jsonify(status="success")

if __name__ == '__main__':
    app.run(debug=True)
