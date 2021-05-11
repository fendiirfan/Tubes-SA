# Destinasi dimana? Jogja
# Berapa? 8

class tempat:
    #Suatu tempat terdiri dari id, nama, dan jarak destinasi dari tempat tersebut ke tempat lainnya
    def __init__(self, id: int, nama='null', jarak_destinasi=[]):
        self.id = id
        self.nama = nama
        self.jarak = jarak_destinasi
        
    def jarakMinimumSelainList(self, list_rute):
        # IS: list rute terdefinisi dari rute yang sudah dibuat
        # FS: mengembalikan index, dan nilai terkecil dari jarak selain index yang sudah di definisikan dari list_rute
        minimum = -1 #index
        # list rute = [0, 1, 2, 3]
        for i in range(len(self.jarak)):
            if self.jarak[i] != 0:
                if minimum == -1 and (i not in list_rute):
                    minimum = i
                if (self.jarak[i] <= self.jarak[minimum]) and (i not in list_rute):
                    minimum = i
        return [minimum, self.jarak[minimum]] #(index, jarak_aktual)
                    
    def printTempat(self):
        print( 'id: {}\nNama: {}\n    Jarak: {}'.format(self.id ,self.nama, self.jarak))

def greedy(list_destinasi) -> []:
    # IS: Terdefinisi list_destiniasi yang merupakan list dari tempat-tempat yang sudah didefinisikan
    # FS: Mengembalikan list yang berisi pola sirkuit terpendek untuk menuju suatu tempat2.
    rute_akhir = [3] # [1, 0, 2, 3, 4, 5]
    for i in range(len(list_destinasi)-1):
        if len(rute_akhir) == 1:
            next_destinasi_kanan = list_destinasi[rute_akhir[0]].jarakMinimumSelainList(rute_akhir)
            rute_akhir.append(next_destinasi_kanan[0])
        else:
            next_destinasi_kanan = list_destinasi[rute_akhir[len(rute_akhir)-1]].jarakMinimumSelainList(rute_akhir)
            next_destinasi_kiri = list_destinasi[rute_akhir[0]].jarakMinimumSelainList(rute_akhir)
            if next_destinasi_kanan[1] >= next_destinasi_kiri[1]:
                rute_akhir.insert(0,next_destinasi_kiri[0])
            else:
                rute_akhir.append(next_destinasi_kanan[0])   
    return rute_akhir
        
if __name__ == "__main__":
    # Test Case
    # 1 [0, 6, 7, 4, 2, 6]
    # 2 [6, 0, 8, 5, 6, 1]
    # 3 [7, 8, 0, 8, 6, 5]
    # 4 [4, 5, 8, 0, 3, 10]
    # 5 [2, 6, 6, 3, 0, 5]
    # 6 [6, 1, 5, 10, 5, 0]

    test_case = [ ['satu', [0, 6, 7, 4, 2, 6]], ['dua', [6, 0, 8, 5, 6, 1]], ['tiga', [7, 8, 0, 8, 6, 5]], 
                ['empat', [4, 5, 8, 0, 3, 10]], ['lima', [2, 6, 6, 3, 0, 5]], ['enam', [6, 1, 5, 10, 5, 0]]]
    
    list_destinasi_asli = []
    
    for i in range(6):
        destinasi_temp = tempat(i, test_case[i][0], test_case[i][1])
        list_destinasi_asli.append(destinasi_temp)
        
    for i in range(6):
        list_destinasi_asli[i].printTempat()
        
    list_pola_destinasi_greedy = greedy(list_destinasi_asli)
    print('=======================================')
    for i in range(len(list_pola_destinasi_greedy)):
        list_destinasi_asli[list_pola_destinasi_greedy[i]].printTempat()