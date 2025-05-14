def parseNumber(val) ->int:
    try:
        return int(str(val).replace('(', '').replace(')', '').replace(',',''))
    except:
        return 0

datas = [
    ['row1', '', 0, 1, 0, 0, 1],
    ['row2', '', 3, 0, '11', 14, 28],
    ['row3', '', 1, 0, 4, '(7)', 12],
    ['row4', '', 0, 0, -3, 0, -3],
    ['row5', '', -12, 0, 0, 0, -12],
]


result = [
    ['bertambah', '', 0,0,0,0,0],
    ['berkurang', '', 0,0,0,0,0],
]

for data in datas:
    if all(parseNumber(x) >= 0 for x in data):
        result[0][2] += parseNumber(data[2])
        result[0][3] += parseNumber(data[3])
        result[0][4] += parseNumber(data[4])
        result[0][5] += parseNumber(data[5])
        result[0][6] += parseNumber(data[6])
    else:
        result[1][2] += parseNumber(data[2])
        result[1][3] += parseNumber(data[3])
        result[1][4] += parseNumber(data[4])
        result[1][5] += parseNumber(data[5])
        result[1][6] += parseNumber(data[6])

# print(result)




datas2 = [
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

datas2filter = [x for x in datas2 if x[0] != '']
print(datas2filter)