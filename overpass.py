# -*- coding: latin-1 -*-
import requests
import json
import numpy as np

def readingFromGeojson():

    vnome = []
    with open('allHighways.geojson') as f:
        data = json.load(f)

    for feature in data['features']:
        try:
            nome = feature['properties']['name']
            coordinates = feature['geometry']['coordinates']
            if nome not in vnome:
                vnome.append(nome)
                for feature1 in data['features']:
                    try:
                        nome1 =  feature1['properties']['name']
                        coordinates1 = feature1['geometry']['coordinates']
                        if nome == nome1:
                            for i in range(len(coordinates1)):
                                if coordinates1[i] not in coordinates:
                                    coordinates.append(coordinates1[i])

                    except:
                        pass
                with open("Ruas&Coordenadas.txt","a") as writter:
                    writter.write("%s\n" % nome)
                    #print("%s" % nome)
                    for i in range(len(coordinates)):
                        try:
                            #print("%.6lf , %.6lf" % (coordinates[i][0], coordinates[i][1]))
                            writter.write("%.6lf , %.6lf\n" % (coordinates[i][0], coordinates[i][1]))
                        except:
                            #print("%.6lf , %.6lf" % (coordinates[i], coordinates[i+1]))
                            writter.write("%.6lf , %.6lf\n" % (coordinates[i], coordinates[i+1]))
                            i = i+1

        except:
            pass
            
def queryWebSite():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area["ISO3166-1"="DE"][admin_level=2];
    (node["amenity"="biergarten"](area);
     way["amenity"="biergarten"](area);
     rel["amenity"="biergarten"](area);
    );
    out center;
    """
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    data = response.json()

    for feature in data['features']:
        try:
            print(feature['properties']['name'])
            print(feature['geometry']['coordinates'])
            print("\n")
        except:
            pass

def main():
    readingFromGeojson()
    #queryWebSite()
main()
