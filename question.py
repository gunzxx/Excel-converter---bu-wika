Saya ingin menggabungkan data berikut:
oldData = [
    ['row1', '', 0, 1, 0, 0],
    ['', 'data1', 0, 1, 0, 0],
    ['row2', '', 1, 0, '7', 9],
    ['', 'data1', 0, 0, '2', 0],
    ['', 'data2', 1, 0, '5', 9],
    ['row3', '', 0, 0, 4, '(7)'],
    ['', 'data1', 0, 0, 0, '(3)'],
    ['', 'data2', 0, 0, 4, '4'],
    ['row5', '', 12, 0, 0, 0],
    ['', 'data2', 12, 0, 0, 0],
]
data3 = [
    ['row2', '', 2, 0, '4', 5],
    ['row4', '', 0, 0, 3, 0],
    ['row3', '', 1, 0, 0, 0],
]

menjadi:
newData = [
    ['row1', '', 0, 1, 0, 0],
    ['', 'data1', 0, 1, 0, 0],
    ['row2', '', 3, 0, '11', 14],
    ['', 'data1', 0, 0, '2', 0],
    ['', 'data2', 1, 0, '5', 9],
    ['', 'data3', 2, 0, '4', 5],
    ['row3', '', 1, 0, 4, '(7)'],
    ['', 'data1', 0, 0, 0, '(3)'],
    ['', 'data2', 0, 0, 4, '4'],
    ['', 'data3', 1, 0, 0, 0],
    ['row4', '', 0, 0, 3, 0],
    ['', 'data3', 0, 0, 3, 0],
    ['row5', '', 12, 0, 0, 0],
    ['', 'data2', 12, 0, 0, 0],
]
bagaimana caranya?


Saya ingin mengolah data berikut:
oldData = [
    ['row1', '', 0, 1, 0, 0],
    ['row1', '', 0, 2, 0, 1],
    ['row2', '', 0, 0, '3', 0],
    ['row2', '', 1, 0, '7', 9],
    ['row3', '', 0, 0, 4, '(7)'],
    ['row3', '', 1, 0, 0, 0],
]
menjadi:
newData = [
    ['row1', '', 0, 2, 0, 1],
    ['row2', '', 1, 0, '10', 9],
    ['row3', '', 1, 0, 4, '(7)'],
]
bagaimana caranya?



saya memiliki data table
datakolom1 | 600,000 | 2
datakolom2 | 3,100,000 | 17
datakolom2 | 100,000 | 2
datakolom3 | 300,000 | 615
datakolom3 | 200,000 | 1
diubah menjadi seperti berikut:
[600,000, 2, 3,100,000, 19, 500,
000, 616]
bagaimana caranya?



Saya memiliki list of string timestamp, saya ingin mengubah list tersebut menjadi list of list yang berisi timestamp dan timestamp yang telah di format, contoh:
[
    ["1746672544.7356393", "06-06-2025 01-01-01"],
]


Saya memiliki list:
data = [
    ['row1', '', 0, 1, 0, 0, 1],
    ['', 'data1', 0, 1, 0, 0, 1],
    ['row2', '', 3, 0, '11', 14, 28],
    ['', 'data1', 0, 0, '2', 0, 2],
    ['', 'data2', 1, 0, '5', 9, 15],
    ['', 'data3', 2, 0, '4', 5, 11],
    ['row3', '', 1, 0, 4, '(7)', 12],
    ['', 'data1', 0, 0, 0, '(3)', 3],
    ['', 'data2', 0, 0, 4, '4', 8],
    ['', 'data3', 1, 0, 0, 0, 1],
    ['row4', '', 0, 0, 3, 0, 3],
    ['', 'data3', 0, 0, 3, 0, 3],
    ['row5', '', 12, 0, 0, 0, 12],
    ['', 'data2', 12, 0, 0, 0, 12],
]


Saya memiliki list:
data = [
    ['row1', '', 0, 1, 0, 0, 1],
    ['row2', '', 3, 0, '11', 14, 28],
    ['row3', '', 1, 0, 4, '(7)', 12],
    ['row4', '', 0, 0, -3, 0, -3],
    ['row5', '', -12, 0, 0, 0, -12],
]
Saya ingin menjumlahkan data di list tersebut dari kolom ke 3 sampai 1 kolom sebelum kolom terakhir menjadi data seperti berikut:

output = [
    ['bertambah', '', 4, 1, 15, 21, ''],
    ['bertambah', '', -12, 0, -3, 0, ''],
]

bagaimana caranya?




data = [
[
"Penghentiaan Aset Dari Penggunaan (401)",
459,
"-2.864.563.586"
],
[
"Pencatatan Barang Yang Mau Dihapuskan (911)",
138,
"-186.959.176"
],
[
"Internal Transfer Keluar (921)",
503,
"-6.027.542.213"
]
]

bagaimana cara memberikan index dan menambahkan total data tersebut manjadi:
[
[
1,
"Penghentiaan Aset Dari Penggunaan (401)",
459,
"-2.864.563.586"
],
[
2,
"Pencatatan Barang Yang Mau Dihapuskan (911)",
138,
"-186.959.176"
],
[
3,
"Internal Transfer Keluar (921)",
503,
"-6.027.542.213"
],
[
'',
"Jumlah",
110,
"-15.106.607.188",
],
],




bagaimana cara mengubah:
data = [ 
    [4, 1,, 1],
    [12, -1, 1],
    [10, 0, 1],
    [0, 0, 1],
]
menjadi
output = [
    [4, 1],
    [10, 0],
]

dengan syarat:
- jika ada bilangan negatif, maka row di hapus
- jika semua nilai 0, maka row dihapus






Saya ingin menggabungkan data berikut:
oldData = [
    ['row1', '', 0, 1, 0, 0],
    ['', 'data1', 0, 1, 0, 0],
    ['row2', '', 1, 0, 7, 9],
    ['', 'data1', 0, 0, 2, 0],
    ['', 'data2', 1, 0, 5, 9],
    ['row3', '', 3, 0, 4, 7],
    ['', 'data1', 0, 0, 0, 3],
    ['', 'data2', 3, 0, 4, 4],
    ['row5', '', 12, 0, 0, 0],
    ['', 'data2', 12, 0, 0, 0],
]
data2 = [
    ['row2', '', 2, 0, 4, 5],
    ['row4', '', 0, 0, 3, 0],
    ['row3', '', -1, 0, 0, 0],
]

menjadi:

newData = [
    ['row1', '', 0, 1, 0, 0],
    ['', 'data1', 0, 1, 0, 0],
    ['row2', '', 3, 0, 11, 14],
    ['', 'data1', 0, 0, 2, 0],
    ['', 'data2', 3, 0, 9, 14],
    ['row3', '', 2, 0, 4, 7],
    ['', 'data1', 0, 0, 0, 3],
    ['', 'data2', 2, 0, 4, 4],
    ['row4', '', 0, 0, 3, 0],
    ['', 'data2', 0, 0, 3, 0],
    ['row5', '', 12, 0, 0, 0],
    ['', 'data2', 12, 0, 0, 0],
]

dengan syarat:
- jika terdapat jenis data yang sama dan di row yang sama, , seperti "data2" di row2, maka akan ditambahkan, jika tidak maka akan buat di baris baru
- jika ada postif ditambah negatif, akan dihitung seperti biasa
bagaimana caranya?