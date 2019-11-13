# -*- coding: latin-1 -*-
import requests
import json
import numpy as np
import csv


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
                            writter.write("%f %f" % (coordinates[i][0], coordinates[i][1]))
                            writter.write("\n")
                        except:
                            #print("%.6lf , %.6lf" % (coordinates[i], coordinates[i+1]))
                            writter.write("%lf %lf" % (coordinates[i], coordinates[i+1]))
                            writter.write("\n")
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

def readingCSV(rua):

    highwayCoords = []
    with open('tabela.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        #pegar as coordenadas da rua e colocar em uma lista
        with open("Ruas&Coordenadas.txt") as txt_reader:
            line = txt_reader.readline()
            n = rua + "\n"
            while line:
                #print(n)
                if line == n:
                    line = txt_reader.readline()
                    while line.startswith("-"):
                        highwayCoords.append(line.split())
                        line = txt_reader.readline()
                    break
                line = txt_reader.readline()
        #terminei de pegar as coordenadas da rua

        #verificar se a rua esta dentro de cada celula geografica
        line_count = 0
        celulas = []
        for row in csv_reader:
            if line_count == 1:
                for hc in highwayCoords:
                    #passando os valores para float
                    lonHighway = float(hc[0]) # longitude da rua
                    latHighway = float(hc[1]) # latitude da rua
                    lonRowS = float(row[0][:10]) # longitude superior da celula geografica
                    lonRowI = float(row[2][:10]) # longitude inferior da celula geografica
                    latRowS = float(row[1][:10]) # latitude superior da celula geografica
                    latRowI = float(row[3][:10]) # latitude inferior da celula geografica
                    if lonHighway >= lonRowS and lonHighway <= lonRowI and latHighway <= latRowS and latHighway >= latRowI:
                        if row[4] not in celulas:
                            celulas.append(row[4])
            line_count = 1
        #print(celulas)
        return celulas

def bitMap():

    #colocando as ruas em uma lista
    vRuas = []
    localizacao = []
    cg = []
    with open("Ruas&Coordenadas.txt") as txt_reader:
        line = txt_reader.readline()
        while line:
            if not line.startswith("-"):
                vRuas.append(line.rstrip('\n'))
            line = txt_reader.readline()

    #pegando a quantidade de celulas geografica
    quantCelulas = -1 #pq tem a linha com os nomes dos campos
    with open('tabela.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            quantCelulas += 1

    #lembrar que as celulas geograficas comecam no 1
    for r in vRuas:
        localizacao = readingCSV(r)
        iLoc = [] #lista de celulas geograficas com valores inteiros
        for i in range(len(localizacao)):
            iLoc.append(int(localizacao[i]))
        l1 = []
        for i in range(quantCelulas):
            if i+1 not in iLoc:
                l1.append(0)
            else:
                l1.append(1)
        cg.append(l1)
        #print(r)
        #print(l1)
        #print("\n")
        with open("Ruas&CelulasGeo.txt","a") as writter:
            writter.write("%s\n" % r)
            for i in l1:
                writter.write("%d " % i)
            writter.write("\n\n")
    #print(cg)

def main():
    #readingFromGeojson()
    #queryWebSite()
    #readingCSV()
    bitMap()
    
main()
