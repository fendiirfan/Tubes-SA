# import library
import requests
import json
from colorama import Fore, Style

from dotenv import load_dotenv

import os
from os.path import join, dirname
from dotenv import load_dotenv
from os import system

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API")
getCoordinateLink = (
    "https://api.openrouteservice.org/geocode/search?api_key={}&text=".format(
        API_KEY))
getMatrixLink = "https://api.openrouteservice.org/v2/matrix/foot-hiking"


# =========================================== API ==============================================
def jprint(obj):
    # IS: Terdefinisi sebuah objek
    # FS: Mengoutputkan isi dari objek-objek tersebut dengan bentuk json
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def getCityNameCoordinate(city: str):
    # IS: Memasukkan nama kota
    # FS: Mengembalikan Nama Kota Secara Rinci dan Koordinat kota Tersebut menggunakan OpenRouteService API
    response = requests.get(getCoordinateLink + city)
    res_json = response.json()

    if len(res_json["features"]) == 0:
        return []

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
        "Accept":
        "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": API_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }

    response = requests.post(
        getMatrixLink,
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


def printAllInputedCities(list_city):
    # IS: Terdefinisi sebuah list yang berisi objek tempat
    # FS: Mengoutpukan data yang disimpan pada objek tempat
    for i in range(len(list_city)):
        print("")
        print("City Number {}".format(i + 1))
        print("===========================")
        print("Index: {}".format(i))
        print("Cities Name: {}".format(list_city[i][0]))
        print("Coordinate: {}".format(list_city[i][1]))
        if len(list_city[i]) == 3:
            print("Jarak ke destinasi lain berdasarkan index: {}".format(
                list_city[i][2]))


# =========================================== GREEDY ALGORITHM ==============================================
class tempat:
    # Objek "Tempat"
    # Objek ini memiliki properti id, nama kota, jarak dari kota tersebut ke kota lainnya dalam bentuk list yang ditentukan dengan index relatif ke variable city_list_for_greedy
    def __init__(self,
                 id: int,
                 nama="null",
                 koordinat_kota=[],
                 jarak_destinasi=[]):
        # Inisialisasi objek, dengan properti id, nama, list jarak dari kota yang terinisialisasi dengan kota-kota lainnya, dan koordinat
        self.id = id
        self.nama = nama
        self.jarak = jarak_destinasi
        self.koordinat = koordinat_kota

    def jarakMinimumSelainList(self, list_rute):
        # IS: list rute terdefinisi dari rute-rute yang sudah dibuat
        # FS: mengembalikan index suatu kota yang tidak terdefinisi pada list_rute dengan nilai jarak terkecil dari properti jarak yang dimiliki objek ini.

        minimum = -1
        for i in range(len(self.jarak)):
            if self.jarak[i] != 0:
                if minimum == -1 and (i not in list_rute):
                    minimum = i
                if (self.jarak[i] <=
                        self.jarak[minimum]) and (i not in list_rute):
                    minimum = i

        print("Jarak Minimum dari Kota {}".format(self.nama))
        print("[", end=" ")
        for i in range(len(self.jarak)):
            if i == minimum:
                print(Fore.GREEN, self.jarak[i], Fore.WHITE, end=" ")
            else:
                print(self.jarak[i], end=" ")
        print("]")
        return [minimum, self.jarak[minimum]]  # (index, jarak_aktual)

    def printTempat(self):
        print("id: {}\nNama: {}\n    Jarak: {}".format(self.id, self.nama,
                                                       self.jarak))


def greedy(list_destinasi):
    # IS: Terdefinisi list_destiniasi yang merupakan list dari tempat-tempat yang sudah didefinisikan
    # FS: Mengembalikan list yang berisi nomor index pola sirkuit terpendek untuk membuat sirkui tempat-tempat yang sudah terdefinisi.

    # list_destinasi merupakan list variabel yang berisi objek tempat
    # [objekTempat1, objekTempat2, objekTempat3]
    
    # rute_akhir merupakan list yang berisi pola hasil greedy, berisi dari nomor index kota relatif ke list list_destinasi
    # [0, 2 ,1] <- nomor index relatif kepada list_destinasi
    # artinya, kalau misalkan digambarkan nomor-nomor index tersebut digambarkan menjadi objek aslinya, sehingga
    # ["objekTempat1", "objekTempat3", "objekTempat2"]

    print("\n\n")
    print(Fore.RED, "GREEDY BY DISTANCE", Fore.WHITE)
    rute_akhir = [
        0
    ]  # diawali dengan kota index ke 0 relatif dari list_destinasi.

    for i in range(len(list_destinasi) - 1):  # perulangan akan dilakukan sebanyak jumlah kota yang terdefinisi - 1
        print(Fore.RED, "=======================", Fore.WHITE)
        print("ITERASI {}".format(i + 1))

        if len(rute_akhir) == 1:                                            # Ketika hanya 1 kota yang ada di rute_akhir
            next_destinasi_kanan = list_destinasi[rute_akhir[0]].jarakMinimumSelainList(rute_akhir)
            print("Terpilih {} dari {} dengan jarak {}".format(
                list_destinasi[next_destinasi_kanan[0]].nama,
                list_destinasi[rute_akhir[len(rute_akhir) - 1]].nama,
                next_destinasi_kanan[1],
            ))
            rute_akhir.append(next_destinasi_kanan[0])
        else:                                                               # Ketika sudah lebih dari 1 kota yang terdefinisi di rute_akhir
            idx_kota_node_kanan = rute_akhir[len(rute_akhir) - 1]
            idx_kota_node_kiri = rute_akhir[0]
            
            print("Node Kanan")
            next_destinasi_kanan = list_destinasi[idx_kota_node_kanan].jarakMinimumSelainList(rute_akhir)
            # next_destinasi_kanan akan mendapatkan index kota yang terpendek relatif dari kota yang berada pada list rute_akhir di paling akhir dan jarak dari kota tersebut ke kota selanjutnya
            print("Node Kiri")
            next_destinasi_kiri = list_destinasi[idx_kota_node_kiri].jarakMinimumSelainList(rute_akhir)
            # next_destinasi_kiri akan mendapatkan index kota yang terpendek relatif dari kota yang berada pada list rute_akhir di paling awal dan jarak dari kota tersebut ke kota selanjutnya
            
            # Pemilihan dari node kanan dan node kiri, mana yang memiliki jarak untuk destinasi selanjutnya yang paling kecil
            if next_destinasi_kanan[1] >= next_destinasi_kiri[1]:
                print("Terpilih {} dari {} dengan jarak {}".format(
                    list_destinasi[next_destinasi_kiri[0]].nama,
                    list_destinasi[rute_akhir[0]].nama,
                    next_destinasi_kiri[1],
                ))
                rute_akhir.insert(0, next_destinasi_kiri[0])
            else:
                print("Terpilih {} dari {} dengan jarak {}".format(
                    list_destinasi[next_destinasi_kanan[0]].nama,
                    list_destinasi[rute_akhir[len(rute_akhir) - 1]].nama,
                    next_destinasi_kanan[1],
                ))
                rute_akhir.append(next_destinasi_kanan[0])
                
    print(Fore.BLUE, "============== GREEDY FINISH ==============", Fore.WHITE)
    return rute_akhir


# =========================================== MAIN PROGRAM ==============================================

if __name__ == "__main__":
    # initialization
    city_list_for_greedy = []
    input_cities_state = True

    # ===================================== GETTING CITY AND DISTANCE MATRIX =================================
    # Input kota-kota yang diinginkan
    while input_cities_state:
        city_list = []

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
                    assert len(temp_city) != 0
                    print(temp_city)
                    city_list.append(temp_city)
                    print("===============")
                    input_counter += 1
                elif input_city == "del":
                    city_list.pop(len(city_list) - 1)
                    input_counter -= 1
                else:
                    bool_input_ulang = False
            except:
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
            printAllInputedCities(city_list)
        else:
            print("==================================================")
            print("Input Kota Tidak Valid, Coba untuk lebih spesifik")

    # ===================================== GREEDY ALGORITHM =================================
    system("cls" if os.name == "nt" else "clear")

    print("List Kota")
    for i in range(len(city_list)):
        destinasi_temp = tempat(i, city_list[i][0], city_list[i][1],
                                city_list[i][2])
        city_list_for_greedy.append(destinasi_temp)

    print("=======================================")
    for i in range(len(city_list)):
        city_list_for_greedy[i].printTempat()

    list_pola_destinasi_greedy = greedy(city_list_for_greedy)

    print("\n\n Pola Kota yang Didapatkan")
    print("=======================================")
    print("Rute by ID:", end=" ")
    for i in range(len(list_pola_destinasi_greedy)):
        if i != (len(list_pola_destinasi_greedy) - 1):
            print(list_pola_destinasi_greedy[i],end="-")
        else:
            print(str(list_pola_destinasi_greedy[i]) + "-" + str(list_pola_destinasi_greedy[0]))
    for i in range(len(list_pola_destinasi_greedy)):
        city_list_for_greedy[list_pola_destinasi_greedy[i]].printTempat()
        
    
