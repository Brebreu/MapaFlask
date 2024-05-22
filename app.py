from flask import Flask, render_template
import folium
import pandas as pd
import geopandas as gpd

app = Flask(__name__)

# Carregar os dados do arquivo Excel
data = pd.read_excel('propriedades_com_degradacao.xlsx', engine='openpyxl')

@app.route('/')
def index():
    # Criar o mapa
    map_obj = folium.Map(location=[-19.7448,-47.9388], zoom_start=10)  # Inverti a ordem das coordenadas aqui

    # Criar grupos de camadas
    marcadores_group = folium.FeatureGroup(name='Centroides')
    limites_group = folium.FeatureGroup(name='Limites APA')
    area_pasto_group = folium.FeatureGroup(name='Área de Pasto')
    car_group = folium.FeatureGroup(name='CAR')

    # Adicionar marcadores para cada ponto
    for index, row in data.iterrows():
        lat_str = str(row['Centroide_Prop_y']).replace(',', '.')  # Converter a latitude para string e substituir a vírgula por ponto
        lon_str = str(row['Centroide_Prop_x']).replace(',', '.')  # Converter a longitude para string e substituir a vírgula por ponto
        lat = float(lat_str)
        lon = float(lon_str)
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
        #folium.Marker([lat, lon], popup=popup_text).add_to(map_obj)
        folium.CircleMarker([lat, lon], radius=4, color='red', fill=True, fill_color='red', fill_opacity=0.6, popup=popup_text).add_to(marcadores_group)

    # Carregar o shapefile e convertê-lo para GeoJSON
    gdf_limite_apa = gpd.read_file('D:/Sipade/SipadeIC/MapaQGIS/LIMITE_APA/LIMITE_APA_R2.shp')
    geojson_data = gdf_limite_apa.to_json()

    gdf_area_do_pasto = gpd.read_file('D:/Sipade/SipadeIC/MapaQGIS/propriedades/pasto/area_do_pasto.shp')
    geojson_data2 = gdf_area_do_pasto.to_json()

    gdf_skimmed_properties = gpd.read_file('D:/Sipade/SipadeIC/MapaQGIS/skimmed_properties/skimmed_properties.shp')
    geojson_data3 = gdf_skimmed_properties.to_json()

    # Adicionar camadas GeoJSON aos grupos de camadas
    folium.GeoJson(
        geojson_data,
        name='Limites Apa'
    ).add_to(limites_group)

    folium.GeoJson(
        geojson_data2,
        name='Área de Pasto',
        style_function=lambda x: {'fillColor': 'green', 'color': 'green'}  # Alterar cor para verde
    ).add_to(area_pasto_group)

    folium.GeoJson(
        geojson_data3,
        name='CAR',
        style_function=lambda x: {'fillColor': 'gray', 'color': 'gray'} 
    ).add_to(car_group)

    # Adicionar grupos de camadas ao mapa
    marcadores_group.add_to(map_obj)
    limites_group.add_to(map_obj)
    area_pasto_group.add_to(map_obj)
    car_group.add_to(map_obj)

    # Adicionar controle de camadas
    folium.LayerControl().add_to(map_obj)

    return map_obj._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
