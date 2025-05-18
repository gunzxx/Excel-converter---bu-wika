from pdfplumber import page
import re

from function.main_fuction import parseNumber, parseNumber2, toDefaultNumber, toPositif


def pdfToList(pages: list[page.Page]) -> list:
    extractData = []
    total = 0

    for page in pages:
        jenisTransaksi = ''
        rowData = ['','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        text = page.extract_text()
        custom_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "text",
            "snap_tolerance": 3,
            "join_tolerance": 3,
            "intersection_tolerance": 5
        }
        table = page.extract_table(table_settings=custom_settings)

        # for row in table:
        #     extractData.append(row)
        # continue

        # mencari transaksi jenis transaksi yang tersedia
        if text:
            cocoks = re.findall(r'jenis transaksi\s*:\s*(.*?)\s*kode', text, re.IGNORECASE)
            for cocok in cocoks:
                words = cocok.strip().split()
                if words:
                    kodeText = words[0]
                    jenisText = " ".join(words[1:]) if len(words) > 1 else ""
                    jenisTransaksi += f"{jenisText} ({kodeText})"

        # mengatur nilai rowData
        if len(extractData) > 0:
            if extractData[-1][0] == jenisTransaksi:
                rowData = extractData[-1]
            else:
                total = 0
                rowData[0] = jenisTransaksi
        else:
            total = 0
            rowData[0] = jenisTransaksi

        # mencari jumlah pengeluaran di tiap transaksi
        if table:
            for row in table:
                # if row[0].lower() == 'T O T A L'.lower():
                #     rowData[19] = row[5]

                if row[1] and row[1].strip() != 'URAIAN' and row[0].lower() != 'T O T A L'.lower() and (not row[2] or row[2].strip() == ''):
                    if row[0].startswith('132'):
                        rowData[5] = parseNumber(rowData[5]) + parseNumber(row[3])
                        rowData[6] = toDefaultNumber(parseNumber(rowData[6]) + parseNumber(row[4]))
                        total += parseNumber(row[4])
                    elif row[0].startswith('133'):
                        rowData[7] = parseNumber(rowData[7]) + parseNumber(row[3])
                        rowData[8] = toDefaultNumber(parseNumber(rowData[8]) + parseNumber(row[4]))
                        total += parseNumber(row[4])
                    elif row[0].startswith('1341'):
                        rowData[9] = parseNumber(rowData[9]) + parseNumber(row[3])
                        rowData[10] = toDefaultNumber(parseNumber(rowData[10]) + parseNumber(row[4]))
                        total += parseNumber(row[4])
                    elif row[0].startswith('135'):
                        rowData[11] = parseNumber(rowData[11]) + parseNumber(row[3])
                        rowData[12] = toDefaultNumber(parseNumber(rowData[12]) + parseNumber(row[4]))
                        total += parseNumber(row[4])
                    # elif row[0].lower() in 'hak cipta, software, lisensi':
                    elif row[0].startswith('162'):
                        rowData[15] = parseNumber(rowData[15]) + parseNumber(row[3])
                        rowData[16] = toDefaultNumber(parseNumber(rowData[16]) + parseNumber(row[4]))
                        total += parseNumber(row[4])
                    elif '166112' in row[0].strip() or row[1].strip().lower() == 'aset tetap yang tidak digunakan dalam operasi pemerintahan'.lower():
                        rowData[17] = parseNumber(rowData[17]) + parseNumber(row[3])
                        rowData[18] = toDefaultNumber(parseNumber(rowData[18]) + parseNumber(row[4]))
                        total += parseNumber(row[4])
                    else:
                        continue
                else:
                    continue
        
        # mengatur nilai data terakhir dengan nilai data baru dan memasukkan jumlah total
        rowData[-1] = toDefaultNumber(total)
        if len(extractData) > 0:
            if extractData[-1][0] == jenisTransaksi:
                extractData[-1] = rowData
            else:
                extractData.append(rowData)
        else:
            extractData.append(rowData)

    return extractData

def handleMutasiTransaksi(oldData:list=[]):
    oriData = oldData.copy()
    outputData = [
        ['Bertambah','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ['Berkurang','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]
    for data in oriData:
        # parseData = [x for x in data if checkIsNumber(x)]
        if all(parseNumber2(x) >= 0 for x in data):
            outputData[0][2] = toDefaultNumber(parseNumber(outputData[0][2]) + parseNumber(data[2]))
            outputData[0][3] = toDefaultNumber(parseNumber(outputData[0][3]) + parseNumber(data[3]))
            outputData[0][4] = toDefaultNumber(parseNumber(outputData[0][4]) + parseNumber(data[4]))
            outputData[0][5] = toDefaultNumber(parseNumber(outputData[0][5]) + parseNumber(data[5]))
            outputData[0][6] = toDefaultNumber(parseNumber(outputData[0][6]) + parseNumber(data[6]))
            outputData[0][7] = toDefaultNumber(parseNumber(outputData[0][7]) + parseNumber(data[7]))
            outputData[0][8] = toDefaultNumber(parseNumber(outputData[0][8]) + parseNumber(data[8]))
            outputData[0][9] = toDefaultNumber(parseNumber(outputData[0][9]) + parseNumber(data[9]))
            outputData[0][10] = toDefaultNumber(parseNumber(outputData[0][10]) + parseNumber(data[10]))
            outputData[0][11] = toDefaultNumber(parseNumber(outputData[0][11]) + parseNumber(data[11]))
            outputData[0][12] = toDefaultNumber(parseNumber(outputData[0][12]) + parseNumber(data[12]))
            outputData[0][13] = toDefaultNumber(parseNumber(outputData[0][13]) + parseNumber(data[13]))
            outputData[0][14] = toDefaultNumber(parseNumber(outputData[0][14]) + parseNumber(data[14]))
            outputData[0][15] = toDefaultNumber(parseNumber(outputData[0][15]) + parseNumber(data[15]))
            outputData[0][16] = toDefaultNumber(parseNumber(outputData[0][16]) + parseNumber(data[16]))
            outputData[0][17] = toDefaultNumber(parseNumber(outputData[0][17]) + parseNumber(data[17]))
            outputData[0][18] = toDefaultNumber(parseNumber(outputData[0][18]) + parseNumber(data[18]))
            outputData[0][19] = toDefaultNumber(parseNumber(outputData[0][19]) + parseNumber(data[19]))
        else:
            outputData[1][2] = toDefaultNumber(parseNumber(outputData[1][2]) + parseNumber(data[2]))
            outputData[1][3] = toDefaultNumber(parseNumber(outputData[1][3]) + parseNumber(data[3]))
            outputData[1][4] = toDefaultNumber(parseNumber(outputData[1][4]) + parseNumber(data[4]))
            outputData[1][5] = toDefaultNumber(parseNumber(outputData[1][5]) + parseNumber(data[5]))
            outputData[1][6] = toDefaultNumber(parseNumber(outputData[1][6]) + parseNumber(data[6]))
            outputData[1][7] = toDefaultNumber(parseNumber(outputData[1][7]) + parseNumber(data[7]))
            outputData[1][8] = toDefaultNumber(parseNumber(outputData[1][8]) + parseNumber(data[8]))
            outputData[1][9] = toDefaultNumber(parseNumber(outputData[1][9]) + parseNumber(data[9]))
            outputData[1][10] = toDefaultNumber(parseNumber(outputData[1][10]) + parseNumber(data[10]))
            outputData[1][11] = toDefaultNumber(parseNumber(outputData[1][11]) + parseNumber(data[11]))
            outputData[1][12] = toDefaultNumber(parseNumber(outputData[1][12]) + parseNumber(data[12]))
            outputData[1][13] = toDefaultNumber(parseNumber(outputData[1][13]) + parseNumber(data[13]))
            outputData[1][14] = toDefaultNumber(parseNumber(outputData[1][14]) + parseNumber(data[14]))
            outputData[1][15] = toDefaultNumber(parseNumber(outputData[1][15]) + parseNumber(data[15]))
            outputData[1][16] = toDefaultNumber(parseNumber(outputData[1][16]) + parseNumber(data[16]))
            outputData[1][17] = toDefaultNumber(parseNumber(outputData[1][17]) + parseNumber(data[17]))
            outputData[1][18] = toDefaultNumber(parseNumber(outputData[1][18]) + parseNumber(data[18]))
            outputData[1][19] = toDefaultNumber(parseNumber(outputData[1][19]) + parseNumber(data[19]))

    return [[str(col) if isinstance(col, int) else col for col in row] for row in outputData]

def getTransaksiBertambah(transactions:list = []):
    oriData = transactions.copy()
    newData = []
    result = []
    sumQty = 0
    sumTotal = 0
    # handle total per jenis transaksi
    for row in oriData:
        if parseNumber(row[-1]) >= 0:
            qty = sum(parseNumber(row[i]) for i in range(2,18) if i % 2 == 1)
            newData.append([row[0], qty, row[-1]])
    # handle jumlah total semua transaksi
    for idx, row in enumerate(newData, start=1):
        result.append([idx]+row)
        sumQty = toDefaultNumber(parseNumber(sumQty) + parseNumber(row[1]))
        sumTotal = toDefaultNumber(parseNumber(sumTotal) + parseNumber(row[2]))
    
    result.append(['', 'Jumlah', sumQty, sumTotal])
    return result

def getTransaksiBerkurang(transactions:list = []):
    oriData = transactions.copy()
    newData = []
    result = []
    sumQty = 0
    sumTotal = 0
    # handle total per jenis transaksi
    for row in oriData:
        if parseNumber(row[-1]) < 0:
            qty = sum(parseNumber(row[i]) for i in range(2,18) if i % 2 == 1)
            newData.append([row[0], qty, row[-1]])
    # handle jumlah total semua transaksi
    for idx, row in enumerate(newData, start=1):
        result.append([idx]+row)
        sumQty = toDefaultNumber(parseNumber(sumQty) + parseNumber(row[1]))
        sumTotal = toDefaultNumber(parseNumber(sumTotal) + parseNumber(row[2]))
    
    result.append(['', 'Jumlah', sumQty, sumTotal])
    return result

def getKolomBertambah(transactions:list, kolom:int) -> list:
    result = []
    sumQty = 0
    sumTotal = 0
    indexResult = 1
    
    filtered = [row for row in transactions if parseNumber(row[kolom]) >= 0 and parseNumber(row[kolom-1]) >= 0]

    for row in filtered:
        if parseNumber(row[kolom-1]) == 0:
            continue

        sumQty = toDefaultNumber(parseNumber(row[kolom-1]) + parseNumber(sumQty))
        sumTotal = toDefaultNumber(parseNumber(row[kolom]) + parseNumber(sumTotal))
        
        result.append([indexResult, row[0], row[kolom-1], row[(kolom)]])
        indexResult+=1
    
    result.append(['', 'Jumlah', sumQty, sumTotal])

    return result

def getKolomPersediaanBertambah(transactions:list, kolom:int) -> list:
    result = []
    sumTotal = 0
    indexResult = 1

    for row in transactions:
        if parseNumber(row[kolom]) <= 0:
            continue

        sumTotal = toDefaultNumber(parseNumber(row[kolom]) + parseNumber(sumTotal))
        
        result.append([indexResult, row[0], row[kolom-1], row[(kolom)]])
        indexResult+=1
    
    result.append(['', 'Jumlah', 0, sumTotal])

    return result

def getKolomBerkurang(transactions:list, kolom:int) -> list:
    result = []
    sumQty = 0
    sumTotal = 0
    indexResult = 1

    for row in transactions:
        if parseNumber(row[kolom]) >= 0:
            continue

        sumTotal = toDefaultNumber(parseNumber(row[kolom]) + parseNumber(sumTotal))
        sumQty = toDefaultNumber(parseNumber(row[kolom-1]) + parseNumber(sumQty))
        
        result.append([indexResult, row[0], row[kolom-1], row[(kolom)]])
        indexResult+=1
    
    result.append(['', 'Jumlah', sumQty, sumTotal])

    return result

def rekapMutasi(saldo: list = [0,0], bertambah: list = [0,0], berkurang: list = [0,0]):
    output = []
    sisa = [0,0]
    berkurang = [ toDefaultNumber(toPositif(col)) for col in berkurang ]

    sisa[0] = toDefaultNumber(parseNumber(saldo[0]) + parseNumber(bertambah[0]) - parseNumber(berkurang[0]))
    sisa[1] = toDefaultNumber(parseNumber(saldo[1]) + parseNumber(bertambah[1]) - parseNumber(berkurang[1]))

    output = saldo + bertambah + berkurang + sisa

    return [output]