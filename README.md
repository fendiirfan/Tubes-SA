# Tubes-SA

Kaenova Mahendra Auditama<sup>1</sup><br>
Fendi Irfan Amorokhman<sup>2</sup><br>
Rachdian Habi Yahya<sup>3</sup><br>
Ananda Affan Fattahila <sup>4</sup><br>
<sup>1</sup><a href="kaenova@student.telkomuniversity.ac.id">kaenova@student.telkomuniversity.ac.id</a><br>
<sup>2</sup><a href="fendiirfan@student.telkomuniversity.ac.id">fendiirfan@student.telkomuniversity.ac.id</a><br>
<sup>3</sup><a href="rhabiy@student.telkomuniversity.ac.id">rhabiy@student.telkomuniversity.ac.id</a><br>
<sup>4</sup><a href="affanfattahila@student.telkomuniversity.ac.id">affanfattahila@student.telkomuniversity.ac.id</a><br>
Informatics Engineering, Telkom University, Indonesia<br>
2021

Penggunaan Algoritma Greedy dalam Perencanaan Rute Perjalanan Sederhana dengan Beberapa Destinasi dengan Menggunakan Open Service Route API.

## Penggunaan

Untuk menjalankan program, pastikan anda sudah mempunyai API Key dari Oepn Service Route:  
[https://openrouteservice.org/]()

Program ini membutuhkan beberapa dependencies dengan itu jalankan script ini terlebih dahulu:

```sh
python -m pip install -r requirements.txt
```

Lalu buka file `.env_example` dan isi `API` dengan API Key yang sudah anda punya. Setelah itu ganti nama file `.env_example` menjadi `.env`

Anda sudah siap untuk menjalankan program kami degnan menggunakan:

```
python main.py
```

## Test Case (No API, No Library)

Untuk menjalankan test case, dapat dilakukan dengan command

```
python main_greedy.py
```
