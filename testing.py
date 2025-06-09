# def parseNumber(val) ->int:
#     try:
#         return int(str(val).replace('(', '').replace(')', '').replace(',',''))
#     except:
#         return 0

# datas = [
#     ['row1', '', 0, 1, 0, 0, 1],
#     ['row2', '', 3, 0, '11', 14, 28],
#     ['row3', '', 1, 0, 4, '(7)', 12],
#     ['row4', '', 0, 0, -3, 0, -3],
#     ['row5', '', -12, 0, 0, 0, -12],
# ]


# result = [
#     ['bertambah', '', 0,0,0,0,0],
#     ['berkurang', '', 0,0,0,0,0],
# ]

# for data in datas:
#     if all(parseNumber(x) >= 0 for x in data):
#         result[0][2] += parseNumber(data[2])
#         result[0][3] += parseNumber(data[3])
#         result[0][4] += parseNumber(data[4])
#         result[0][5] += parseNumber(data[5])
#         result[0][6] += parseNumber(data[6])
#     else:
#         result[1][2] += parseNumber(data[2])
#         result[1][3] += parseNumber(data[3])
#         result[1][4] += parseNumber(data[4])
#         result[1][5] += parseNumber(data[5])
#         result[1][6] += parseNumber(data[6])

# # print(result)




# datas2 = [
#     ['row1', '', 0, 1, 0, 0, 1],
#     ['', 'data1', 0, 1, 0, 0, 1],
#     ['row2', '', 3, 0, '11', 14, 28],
#     ['', 'data1', 0, 0, '2', 0, 2],
#     ['', 'data2', 1, 0, '5', 9, 15],
#     ['', 'data3', 2, 0, '4', 5, 11],
#     ['row3', '', 1, 0, 4, '(7)', 12],
#     ['', 'data1', 0, 0, 0, '(3)', 3],
#     ['', 'data2', 0, 0, 4, '4', 8],
#     ['', 'data3', 1, 0, 0, 0, 1],
#     ['row4', '', 0, 0, 3, 0, 3],
#     ['', 'data3', 0, 0, 3, 0, 3],
#     ['row5', '', 12, 0, 0, 0, 12],
#     ['', 'data2', 12, 0, 0, 0, 12],
# ]

# datas2filter = [x for x in datas2 if x[0] != '']
# print(datas2filter)





from collections import OrderedDict
# import copy

# Data awal
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
outputData = []

# Fungsi untuk buat struktur default manual
# def default_row():
#     return {'': [0] * 18}  # key '' sudah ada dengan nilai default

# Buat dict utama, default dict dengan fungsi default_row
structured = OrderedDict()

# Helper untuk tambah data
def add_row_data(jenis, bulan, data):
    if jenis not in structured:
        structured[jenis] = {}
        # structured[jenis][''] = data
    if bulan not in structured[jenis]:
        structured[jenis][bulan] = [0] * 4
    for i in range(4):
        structured[jenis][bulan][i] += data[i]

# add_row_data('row1', '', [0,1]*9)
i = 0
while i < len(oldData):
    jenis = oldData[i][0]
    i += 1
    while i < len(oldData) and oldData[i][0] == '':
        bulan = oldData[i][1]
        data = oldData[i][2:]
        add_row_data(jenis, bulan, data)
        i += 1

for data in data2:
    jenis = data[0]
    base = data[2:]
    add_row_data(jenis,'data2', base)

# print(structured)

# proses dictionary
for jenisTransaksi in structured:
    headerTransaksi = [jenisTransaksi, ''] + [0] * 4
    prices = headerTransaksi[2:]
    for bulan in [data for data in structured[jenisTransaksi]]:
        for i in range(len(structured[jenisTransaksi][bulan])):
            headerTransaksi[i+2] += structured[jenisTransaksi][bulan][i]
    outputData.append(headerTransaksi)

    for bulan in [data for data in structured[jenisTransaksi]]:
        outputData.append(['',bulan] + structured[jenisTransaksi][bulan])
        
        # combined = [a+b for a,b in zip(headerTransaksi[2:], structured[jenisTransaksi][bulan])]

print(outputData)