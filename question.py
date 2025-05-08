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