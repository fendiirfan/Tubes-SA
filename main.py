# import library
import requests
import json

from dotenv import load_dotenv

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API")
getCoordinateLink = (
    "https://api.openrouteservice.org/geocode/search?api_key={}&text=".format(API_KEY)
)
getMatrixLink = ""


# =========================================== API THINGY ==============================================
# printing on json format
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def getCityNameCoordinate(city: str):
    # IS: Memasukkan nama kota
    # FS: Mengembalikan Nama Kota Secara Rinci dan Koordinat kota Tersebut menggunakan OpenRouteService API
    response = requests.get(getCoordinateLink + city)
    res_json = response.json()
    city_name = "{}, {}, {}".format(
        res_json["features"][0]["properties"]["name"],
        res_json["features"][0]["properties"]["region"],
        res_json["features"][0]["properties"]["country"],
    )
    coordinate = res_json["features"][0]["geometry"]["coordinates"]
    return [city_name, coordinate]


def getMatrixDistance(cities_coordinate_array):
    # IS: Memasukkan array dari semua kota yang terdaftar
    # FS: Mengembalikan matrix Jarak Antar Kota menggunakan OpenRouteService API

    print(cities_coordinate_array)
    body = {
        "locations": cities_coordinate_array,
        "metrics": ["distance"],
        "resolve_locations": "true",
        "units": "km",
    }

    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": API_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }

    response = requests.post(
        "https://api.openrouteservice.org/v2/matrix/foot-walking",
        json=body,
        headers=headers,
    )

    res_json = response.json()

    matrix = res_json["distances"]

    # Checking if API ERROR
    for i in range(1, len(matrix[0])):
        if matrix[0][i] == 0:
            return []

    return res_json["distances"]


def printAllInpuutedCities(list_city):
    for i in range(len(list_city)):
        print("")
        print("City Number {}".format(i + 1))
        print("===========================")
        print("Index: {}".format(i))
        print("Cities Name: {}".format(list_city[i][0]))
        print("Coordinate: {}".format(list_city[i][1]))
        if len(list_city[i]) == 3:
            print(
                "Jarak ke destinasi lain berdasarkan index: {}".format(list_city[i][2])
            )


# =========================================== GREEDY ALGORITHM ==============================================
class tempat:
    # Suatu tempat terdiri dari id, nama, dan jarak destinasi dari tempat tersebut ke tempat lainnya
    def __init__(self, id: int, nama="null", koordinat_kota=[], jarak_destinasi=[]):
        self.id = id
        self.nama = nama
        self.jarak = jarak_destinasi
        self.koordinat = koordinat_kota

    def jarakMinimumSelainList(self, list_rute):
        # IS: list rute terdefinisi dari rute yang sudah dibuat
        # FS: mengembalikan index, dan nilai terkecil dari jarak selain index yang sudah di definisikan dari list_rute
        minimum = -1  # index
        # list rute = [0, 1, 2, 3]
        for i in range(len(self.jarak)):
            if self.jarak[i] != 0:
                if minimum == -1 and (i not in list_rute):
                    minimum = i
                if (self.jarak[i] <= self.jarak[minimum]) and (i not in list_rute):
                    minimum = i
        return [minimum, self.jarak[minimum]]  # (index, jarak_aktual)

    def printTempat(self):
        print("id: {}\nNama: {}\n    Jarak: {}".format(self.id, self.nama, self.jarak))


def greedy(list_destinasi):
    # IS: Terdefinisi list_destiniasi yang merupakan list dari tempat-tempat yang sudah didefinisikan
    # FS: Mengembalikan list yang berisi pola sirkuit terpendek untuk menuju suatu tempat2.
    rute_akhir = [0]  # [1, 0, 2, 3, 4, 5]
    for i in range(len(list_destinasi) - 1):
        if len(rute_akhir) == 1:
            next_destinasi_kanan = list_destinasi[rute_akhir[0]].jarakMinimumSelainList(
                rute_akhir
            )
            rute_akhir.append(next_destinasi_kanan[0])
        else:
            next_destinasi_kanan = list_destinasi[
                rute_akhir[len(rute_akhir) - 1]
            ].jarakMinimumSelainList(rute_akhir)
            next_destinasi_kiri = list_destinasi[rute_akhir[0]].jarakMinimumSelainList(
                rute_akhir
            )
            if next_destinasi_kanan[1] >= next_destinasi_kiri[1]:
                rute_akhir.insert(0, next_destinasi_kiri[0])
            else:
                rute_akhir.append(next_destinasi_kanan[0])
    return rute_akhir


# =========================================== MAIN PROGRAM ==============================================

if __name__ == "__main__":
    # initialization
    city_list = []
    city_list_for_greedy = []
    input_cities_state = True

    # ===================================== GETTING CITY AND DISTANCE MATRIX =================================
    # Input kota-kota yang diinginkan
    while input_cities_state:
        print("Inputting Cities")
        bool_input_ulang = True
        input_counter = 0
        while bool_input_ulang:
            input_city = input(
                "The City Name (input -1 if done, if you want to delete last city you inputted type 'del'): "
            ).format(input_counter)
            try:
                if input_city != "-1" and input_city != "del":
                    temp_city = getCityNameCoordinate(input_city)
                    print(temp_city)
                    city_list.append(temp_city)
                    print("===============")
                    input_counter += 1
                elif input_city == "del":
                    city_list.pop(len(city_list) - 1)
                else:
                    bool_input_ulang = False
            except (RuntimeError, TypeError, NameError):
                print("Error when getting city")

        # Ambil matrix jarak dari Koordinat-Koordinat Kota yang sudah diinputkan
        ## Memasukkan semua koordinat untuk API
        list_koordinat = []
        for i in range(len(city_list)):
            list_koordinat.append(city_list[i][1])
        try:
            matrix_jarak = getMatrixDistance(list_koordinat)
        except (RuntimeError, TypeError, NameError):
            print("Error when getting a Distance Matrix")
        ## Memasukkan matrix ke dalam city list
        if len(matrix_jarak) != 0:
            input_cities_state = False
            for i in range(len(city_list)):
                city_list[i].append(matrix_jarak[i])
            printAllInpuutedCities(city_list)
        else:
            print("==================================================")
            print("Input Kota Tidak Valid, Coba untuk lebih spesifik")

    # ===================================== GREEDY ALGORITHM =================================

    for i in range(len(city_list)):
        destinasi_temp = tempat(i, city_list[i][0], city_list[i][1], city_list[i][2])
        city_list_for_greedy.append(destinasi_temp)

    print("=======================================")
    for i in range(len(city_list)):
        city_list_for_greedy[i].printTempat()

    list_pola_destinasi_greedy = greedy(city_list_for_greedy)
    print("=======================================")
    for i in range(len(list_pola_destinasi_greedy)):
        city_list_for_greedy[list_pola_destinasi_greedy[i]].printTempat()
