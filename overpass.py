# -*- coding: latin-1 -*-
import requests
import json
import geojson
import numpy as np
import csv

#nao estou utilizando, mas pode ser util no futuro
def readingFromGeojson():
    vnome = []
    #data = json.load(open(C:\Users\Lucas\PycharmProjects\gerador\venv\Lib, encoding='utf-8'))
    with open('allHighways.geojson', encoding="utf8") as f:
        data = geojson.load(f)

    #nomesPossiveis = ["Rua", "Avenida"]
    for feature in data['features']:
        try:
            nome = feature['properties']['name']
            coordinates = feature['geometry']['coordinates']
            if nome.startswith("Rua") or nome.startswith("Avenida"):
                if nome not in vnome:
                    vnome.append(nome)
                    for feature1 in data['features']:
                        try:
                            nome1 = feature1['properties']['name']
                            coordinates1 = feature1['geometry']['coordinates']
                            if nome == nome1:
                                for i in range(len(coordinates1)):
                                    if coordinates1[i] not in coordinates:
                                        coordinates.append(coordinates1[i])

                        except:
                            pass
                    with open("Ruas&Coordenadas.txt", "a") as writter:
                        writter.write("%s\n" % nome)
                        # print("%s" % nome)
                        for i in range(len(coordinates)):
                            try:
                                # print("%.6lf , %.6lf" % (coordinates[i][0], coordinates[i][1]))
                                writter.write("%f %f" % (coordinates[i][0], coordinates[i][1]))
                                writter.write("\n")
                            except:
                                # print("%.6lf , %.6lf" % (coordinates[i], coordinates[i+1]))
                                writter.write("%lf %lf" % (coordinates[i], coordinates[i + 1]))
                                writter.write("\n")
                                i = i + 1

        except:
            pass
#nao estou utilizando, mas pode ser util no futuro
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
#nao estou utilizando, mas pode ser util no futuro
def readingCSV(readingCsvParameters):

    highwayCoords = []
    with open(readingCsvParameters[0]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # pegar as coordenadas da rua e colocar em uma lista
        with open("Ruas&Coordenadas.txt") as txt_reader:
            line = txt_reader.readline()
            n = readingCsvParameters[1] + "\n"
            while line:
                # print(n)
                if line == n:
                    line = txt_reader.readline()
                    while line.startswith("-"):
                        highwayCoords.append(line.split())
                        line = txt_reader.readline()
                    break
                line = txt_reader.readline()
        # terminei de pegar as coordenadas da rua

        # verificar se a rua esta dentro de cada celula geografica
        line_count = 0
        celulas = []
        for row in csv_reader:
            if line_count == 1:
                for hc in highwayCoords:
                    # passando os valores para float
                    lonHighway = float(hc[0])  # longitude da rua
                    latHighway = float(hc[1])  # latitude da rua
                    lonRowS = float(row[0][:10])  # longitude superior da celula geografica
                    lonRowI = float(row[2][:10])  # longitude inferior da celula geografica
                    latRowS = float(row[1][:10])  # latitude superior da celula geografica
                    latRowI = float(row[3][:10])  # latitude inferior da celula geografica
                    if lonHighway >= lonRowS and lonHighway <= lonRowI and latHighway <= latRowS and latHighway >= latRowI:
                        if row[4] not in celulas:
                            celulas.append(row[4])
            line_count = 1
        # print(celulas)
        return celulas


def getLatLongMaxMin():

    latMaior = -50.0
    lonMaior = -50.0
    latMenor = 1.0
    lonMenor = 1.0

    nLatMaior = "a"
    nLonMaior = "a"
    nLatMenor = "a"
    nLonMenor = "a"

    with open("Ruas&Coordenadas.txt") as txt_reader:
        line = txt_reader.readline() # lendo cada linha do txt, procurando a Latitude e Longitude maior e menor
        while line:
            if not line.startswith("-"):
                nome = line
            if line.startswith("-"):
                aux = line.split()
                lat = float(aux[1])
                lon = float(aux[0])
                if lon <= lonMenor:
                    lonMenor = lon
                    nLonMenor = nome
                if lat >= latMaior:
                    latMaior = lat
                    nLatMaior = nome
                if lon >= lonMaior:
                    lonMaior = lon
                    nLonMaior = nome
                if lat <= latMenor:
                    latMenor = lat
                    nLatMenor = nome
            line = txt_reader.readline()
        print("TOP LON = %.6f %s" % (lonMenor, nLonMenor))
        print("TOP LAT = %.6f %s" % (latMaior, nLatMaior))
        print("BOTTOM LON = %.6f %s" % (lonMaior, nLonMaior))
        print("BOTTOM LAT = %.6f %s" % (latMenor, nLatMenor))

def geograficCell():

    print("Iniciando funcao : geograficCell")
    lonTopLeft = -48.933195
    latTopLeft = -26.139358

    lonBottomRight = -48.727638
    latBottomRight = -26.433591

    quantLon = input("Digite a quantidade LINHAS : ")
    quantLat = input("Digite a quantidade COLUNAS : ")
    quantLatStr = quantLat
    quantLonStr = quantLon
    quantLat = int(quantLat)
    quantLon = int(quantLon)
    quantCelulas = quantLat * quantLon
    print("Quantidade TOTAL de CELULAS GEOGRAFICAS = %d" % quantCelulas)

    tamLon = -1*((lonTopLeft - lonBottomRight)/quantLon) #definindo o tamanho total da longitude no mapa
    tamLat = -1*((latTopLeft - latBottomRight)/quantLat) #definindo o tamanho total da latitude no mapa

    cont = 1
    tabela = "Tabela-" + quantLonStr + "x" + quantLatStr
    tabelaCSV = tabela + ".csv"
    with open(tabelaCSV, 'w', newline='\n', encoding='utf-8') as csvFile: #escrevendo na tabela
        writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvData = ['left', 'top', "right", "bottom", "id"]
        # Serão necessários 2 conjuntos de coordenadas. (left, top) e (right, bottom), alem do id.
        #(left, top) são as coordenadas superiores da esquerda de um retangulo.
        # (right, bottom) são as coordenadas inferiores da direita de um retangulo
        writer.writerow(csvData)
        for i in range(quantLon):
            for j in range(quantLat):
                left = lonTopLeft + (i*tamLon)
                top = latTopLeft + (j*tamLat)
                right = left + tamLon
                bottom = top + tamLat
                id = cont
                cont += 1
                writer.writerow(["%.6f" % left , "%.6f" % top , "%.6f" % right, "%.6f" % bottom , "%d" % id])
    print("Terminando funcao : geograficCell")
    bitMap(tabela)

def bitMap(tabela):

    print("Iniciando a funcao : bitMap")
    # colocando as ruas em uma lista
    vRuas = []
    localizacao = []
    cg = []
    with open("Ruas&Coordenadas.txt") as txt_reader:
        line = txt_reader.readline()
        while line:
            if not line.startswith("-"):
                vRuas.append(line.rstrip('\n'))
            line = txt_reader.readline()

    # pegando a quantidade de celulas geografica
    quantCelulas = -1  # pq tem a linha com os nomes dos campos
    tabelaCSV = tabela + ".csv"
    with open(tabelaCSV) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            quantCelulas += 1

    # lembrar que as celulas geograficas comecam no 1
    readingCsvParameters = []
    readingCsvParameters.append(tabelaCSV)
    readingCsvParameters.append(" ")
    for r in vRuas:
        readingCsvParameters[1] = r
        localizacao = readingCSV(readingCsvParameters)
        iLoc = []  # lista de celulas geograficas com valores inteiros
        for i in range(len(localizacao)):
            iLoc.append(int(localizacao[i]))
        l1 = []
        for i in range(quantCelulas):
            if i + 1 not in iLoc:
                l1.append(0)
            else:
                l1.append(1)
        cg.append(l1)

        nameFile = "Ruas&BitMap-" + tabela + ".txt"
        with open(nameFile, "a") as writter:
            writter.write("%s\n" % r)
            for i in l1:
                writter.write("%d " % i)
            writter.write("\n\n")
    print("Terminando a funcao : bitMap")

def main():
    geograficCell()
    #getLatLongMaxMin()
    # readingFromGeojson()
    # queryWebSite()
    # readingCSV()
main()



