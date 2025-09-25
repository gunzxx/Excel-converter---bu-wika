from pdfplumber import page
import re
from collections import OrderedDict

from function.main_fuction import parseNumber, parseNumber2, toDefaultNumber, addNumber, toPositif


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
            "intersection_tolerance": 5,
        }
        table = page.extract_table(table_settings=custom_settings)

        # mencari transaksi jenis transaksi yang tersedia
        if text:
            cocoks = re.findall(r'jenis transaksi\s*:\s*(.*?)\s*akun', text, re.IGNORECASE)
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
            table = table[3:]
            for row in table:
                # if row[0].lower() == 'T O T A L'.lower():
                #     rowData[19] = row[5]

                if row[0] and row[0].strip() != 'KODE' and row[0].lower() != 'T O T A L'.lower() and (not row[2] or row[2].strip() == ''):
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
                    elif row[0].startswith('162') or 'aset tak berwujud' in row[0].lower():
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
        if any(any(cell and cell.strip() for cell in row) for row in table[3:-1]):
            rowData[-1] = toDefaultNumber(total)
            if len(extractData) > 0:
                if extractData[-1][0] == jenisTransaksi:
                    extractData[-1] = rowData
                else:
                    extractData.append(rowData)
            else:
                extractData.append(rowData)

            return extractData


def kdpPdfToList(pages:list[page.Page], ) -> list:
    extractData = []

    for page in pages:
        jenisTransaksi = ''
        rowData = ['','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        text = page.extract_text()
        custom_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "text",
            "snap_tolerance": 3,
            "join_tolerance": 3,
            "intersection_tolerance": 5,
        }
        table = page.extract_table(table_settings=custom_settings)
        # mencari transaksi jenis transaksi yang tersedia
        if text:
            cocoks = re.findall(r"(?i)jenis transaksi :[:\-]?\s*(.*?)\s*kode", text, flags=re.MULTILINE | re.IGNORECASE)
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

        # mencari nilai kdp di tiap transaksi
        if table:
            table = table[3:]
            for row in table:

                if row[0] and row[0].strip() != 'KODE' and row[0].lower() != 'T O T A L'.lower() and (not row[2] or row[2].strip() == ''):
                    if row[0].startswith('1361'):
                        rowData[13] = parseNumber(rowData[13]) + parseNumber(row[3])
                        rowData[14] = toDefaultNumber(parseNumber(rowData[14]) + parseNumber(row[4]))
                        total += parseNumber(row[4])
                    else:
                        continue
                else:
                    continue
        
        # mengatur nilai data terakhir dengan nilai data baru dan memasukkan jumlah total
        if any(any(cell and cell.strip() for cell in row) for row in table[3:-1]):
            rowData[-1] = toDefaultNumber(total)
            if len(extractData) > 0:
                if extractData[-1][0] == jenisTransaksi:
                    extractData[-1] = rowData
                else:
                    extractData.append(rowData)
            else:
                extractData.append(rowData)

            return extractData


def atbPdfToList(pages:list[page.Page], ) -> list:
    extractData = []

    for page in pages:
        jenisTransaksi = ''
        rowData = ['','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        text = page.extract_text()
        custom_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "text",
            "snap_tolerance": 3,
            "join_tolerance": 3,
            "intersection_tolerance": 5,
        }
        table = page.extract_table(table_settings=custom_settings)
        
        # mencari transaksi jenis transaksi yang tersedia
        if text:
            cocoks = re.findall(rf"(?i)jenis transaksi :[:\-]?\s*(.*?)\s*kode", text, flags=re.MULTILINE | re.IGNORECASE)
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

        # mencari nilai kdp di tiap transaksi
        if table:
            table = table[3:]
            for row in table:

                if row[0] and row[0].lower() != 'T O T A L'.lower():
                    if row[0].startswith('162'):
                        rowData[15] = parseNumber(rowData[15]) + parseNumber(row[3])
                        rowData[16] = toDefaultNumber(parseNumber(rowData[16]) + parseNumber(row[4]))
                        total += parseNumber(row[4])
                    else:
                        continue
                else:
                    continue

        # mengatur nilai data terakhir dengan nilai data baru dan memasukkan jumlah total
        rowData[-1] = toDefaultNumber(total)

        if any(any(cell and cell.strip() for cell in row) for row in table[3:-1]):
            if len(extractData) > 0:
                if extractData[-1][0] == jenisTransaksi:
                    extractData[-1] = rowData
                else:
                    extractData.append(rowData)
            else:
                extractData.append(rowData)

            return extractData


def handleAddDoubleData(oldData:list, newData:list, month:str) -> list:
    if not newData:
        return oldData

    outputData = []
    structured = OrderedDict()

    # Helper untuk tambah data
    def add_row_data(jenis, bulan, data):
        if jenis not in structured:
            structured[jenis] = {}
            # structured[jenis][''] = data
        if bulan not in structured[jenis]:
            structured[jenis][bulan] = [0] * 18
        for i in range(18):
            structured[jenis][bulan][i] += parseNumber(data[i])

    i = 0
    while i < len(oldData):
        jenis = oldData[i][0]
        i += 1
        while i < len(oldData) and oldData[i][0] == '':
            bulan = oldData[i][1]
            data = oldData[i][2:]
            add_row_data(jenis, bulan, data)
            i += 1

    for data in newData:
        jenis = data[0]
        base = data[2:]
        if(jenis != ''):
            add_row_data(jenis,month, base)
    # return structured

    # proses dictionary
    for jenisTransaksi in structured:
        headerTransaksi = [jenisTransaksi, ''] + [0] * 18
        for bulan in [data for data in structured[jenisTransaksi]]:
            for i in range(len(structured[jenisTransaksi][bulan])):
                headerTransaksi[i+2] += structured[jenisTransaksi][bulan][i]
                headerTransaksi[i+2] = toDefaultNumber(headerTransaksi[i+2])
        outputData.append(headerTransaksi)

        for bulan in [data for data in structured[jenisTransaksi]]:
            outputData.append(['',bulan] + [toDefaultNumber(x) for x in structured[jenisTransaksi][bulan]])
    return outputData


def handleSaldo(pages: list[page.Page]) -> list:
    total = 0
    jenisData = [
        "Barang Konsumsi, Bahan untuk Pemeliharaan, Suku Cadang, Bahan Baku, Persediaan Lainnya",
        "Tanah",
        "Peralatan dan Mesin",
        "Gedung dan Bangunan",
        "Jalan dan Jembatan, 134112 Irigasi , 134113 Jaringan",
        "Aset Tetap Lainnya",
        "Konstruksi Dalam Pengerjaan",
        "Hak Cipta,Software,Lisensi,Aset Tak Berwujud Lainnya",
        "Aset Tetap yang tidak digunakan dalam operasi pemerintahan",
    ]
    rowData = ['','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for page in pages:
        tahunAnggaran = ''
        text = page.extract_text()
        custom_settings = {
            # "vertical_strategy": "lines",
            # "horizontal_strategy": "text",
            # "snap_tolerance": 3,
            # "join_tolerance": 3,
            # "intersection_tolerance": 5,
        }
        table = page.extract_table()

        # mencari tahun jenis anggaran
        if text:
            cocoks = re.findall(r'^tahun anggaran\s*(.*)', text, re.MULTILINE | re.IGNORECASE)
            tahunAnggaran += f"1 Januari {parseNumber(cocoks[0]) + 1}" if len(cocoks) > 0 else ''

        rowData[0] = tahunAnggaran

        # mencari jumlah pengeluaran di tiap transaksi
        if table:
            table = table[3:]
            for row in table:
                if any(kolom == '' or kolom == None or '(' in kolom for kolom in row): continue
                # rowData.append(row)
                # continue

                if row[1].lower() in jenisData[0].lower():
                    rowData[2] = toDefaultNumber(parseNumber(rowData[2]) + parseNumber(row[2]))
                    total += parseNumber(row[2])
                elif row[1].lower() in jenisData[1].lower():
                    rowData[4] = toDefaultNumber(parseNumber(rowData[4]) + parseNumber(row[2]))
                    total += parseNumber(row[2])
                elif row[1].lower() in jenisData[2].lower():
                    rowData[6] = toDefaultNumber(parseNumber(rowData[6]) + parseNumber(row[2]))
                    total += parseNumber(row[2])
                elif row[1].lower() in jenisData[3].lower():
                    rowData[8] = toDefaultNumber(parseNumber(rowData[8]) + parseNumber(row[2]))
                    total += parseNumber(row[2])
                elif row[1].lower() in jenisData[4].lower():
                    rowData[10] = toDefaultNumber(parseNumber(rowData[10]) + parseNumber(row[2]))
                    total += parseNumber(row[2])
                elif row[1].lower() in jenisData[5].lower():
                    rowData[12] = toDefaultNumber(parseNumber(rowData[12]) + parseNumber(row[2]))
                    total += parseNumber(row[2])
                elif row[1].lower() in jenisData[6].lower():
                    rowData[14] = toDefaultNumber(parseNumber(rowData[14]) + parseNumber(row[2]))
                    total += parseNumber(row[2])
                elif row[1].lower() in jenisData[7].lower():
                    rowData[16] = toDefaultNumber(parseNumber(rowData[16]) + parseNumber(row[2]))
                    total += parseNumber(row[2])
                elif row[1].lower() in jenisData[8].lower():
                    rowData[18] = toDefaultNumber(parseNumber(rowData[18]) + parseNumber(row[2]))
                    total += parseNumber(row[2])

    rowData[-1] = toDefaultNumber(total)
    return rowData

# def handleKuantitas(kuantitas: list, saldo: list):
#     rowData = saldo.copy()

#     if kuantitas[3]:
#         rowData[3] = toDefaultNumber(parseNumber(rowData[3]) + parseNumber(kuantitas[3]))
#     if kuantitas[5]:
#         rowData[5] = toDefaultNumber(parseNumber(rowData[5]) + parseNumber(kuantitas[5]))
#     if kuantitas[7]:
#         rowData[7] = toDefaultNumber(parseNumber(rowData[7]) + parseNumber(kuantitas[7]))
#     if kuantitas[9]:
#         rowData[9] = toDefaultNumber(parseNumber(rowData[9]) + parseNumber(kuantitas[9]))
#     if kuantitas[11]:
#         rowData[11] = toDefaultNumber(parseNumber(rowData[11]) + parseNumber(kuantitas[11]))
#     if kuantitas[13]:
#         rowData[13] = toDefaultNumber(parseNumber(rowData[13]) + parseNumber(kuantitas[13]))
#     if kuantitas[15]:
#         rowData[15] = toDefaultNumber(parseNumber(rowData[15]) + parseNumber(kuantitas[15]))
#     if kuantitas[17]:
#         rowData[17] = toDefaultNumber(parseNumber(rowData[17]) + parseNumber(kuantitas[17]))
#     return rowData


def handleKuantitas(pages: list[page.Page], saldo: list) -> list:
    rowData = saldo.copy()
    jenisData = [
        "Tanah",
        "Peralatan dan Mesin",
        "Gedung dan Bangunan",
        "Jalan dan Jembatan, Irigasi, Jaringan",
        "Aset Tetap Lainnya",
        "Konstruksi Dalam Pengerjaan",
        "Hak Cipta,Software,Lisensi,Aset Tak Berwujud Lainnya",
        "Aset Tetap yang tidak digunakan dalam operasi pemerintahan",
    ]

    for page in pages:
        tahunAnggaran = ''
        text = page.extract_text()
        table = page.extract_table()

        # mencari tahun jenis anggaran
        if text:
            cocoks = re.findall(r'^tahun anggaran\s*(.*)', text, re.MULTILINE | re.IGNORECASE)
            tahunAnggaran += f"1 Januari {parseNumber(cocoks[0]) + 1}" if len(cocoks) > 0 else ''

        # mencari jumlah pengeluaran di tiap transaksi
        if table:
            table = table[4:]
            # table = [row for row in table if row[2] != '' or row[2] != None]
            for row in table:
                if (row[2] == '' or row[2] == None) and (row[1] != None or row[1] != '') and row[0] != 'TOTAL':
                    # extract.append(row)
                    if row[1].lower() in jenisData[0].lower():
                        rowData[3] = toDefaultNumber(parseNumber(rowData[3]) + parseNumber(row[9]))
                    elif row[1].lower() in jenisData[1].lower():
                        rowData[5] = toDefaultNumber(parseNumber(rowData[5]) + parseNumber(row[9]))
                    elif row[1].lower() in jenisData[2].lower():
                        rowData[7] = toDefaultNumber(parseNumber(rowData[7]) + parseNumber(row[9]))
                    elif row[1].lower() in jenisData[3].lower():
                        rowData[9] = toDefaultNumber(parseNumber(rowData[9]) + parseNumber(row[9]))
                    elif row[1].lower() in jenisData[4].lower():
                        rowData[11] = toDefaultNumber(parseNumber(rowData[11]) + parseNumber(row[9]))
                    elif row[1].lower() in jenisData[5].lower():
                        rowData[13] = toDefaultNumber(parseNumber(rowData[13]) + parseNumber(row[9]))
                    elif row[1].lower() in jenisData[6].lower():
                        rowData[15] = toDefaultNumber(parseNumber(rowData[15]) + parseNumber(row[9]))
                    elif row[1].lower() in jenisData[7].lower():
                        rowData[17] = toDefaultNumber(parseNumber(rowData[17]) + parseNumber(row[9]))
    return rowData


# Fungsi untuk menambah data ketika spreadsheet kosong
def handleAddData(oldData:list[list], inputList: list[list], month:str):
    if not inputList:
        return oldData

    if(len(oldData) > 0) :
        rowMap = {}
        newData = []
        i = 0

        while i < len(oldData):
            row = oldData[i]
            if row[0] != '':
                rowKey = row[0]
                rowMap[rowKey] = len(newData)
                newData.append(row)
                
                i+=1
                while i < len(oldData) and oldData[i][0] == '':
                    newData.append(oldData[i])
                    i+=1
            else:
                i+=1
        # return newData
        
        for row in inputList:
            rowKey = row[0]
            original = row.copy()
            
            if rowKey.strip() != '' and rowKey in rowMap and row[1] == '':
                idx = rowMap[rowKey]

                for j in range(2, len(row)):
                    newData[idx][j] = toDefaultNumber(addNumber(newData[idx][j], row[j]))
                
                insert_pos = idx+1
                while insert_pos < len(newData) and newData[insert_pos][0].strip() == '':
                    insert_pos += 1
                newData.insert(insert_pos, ['', month] + original[2:])
                    
                for key in rowMap:
                    if rowMap[key] >= insert_pos:
                        rowMap[key] += 1
            
            # Tambah row baru jika belum ada sebelumnya
            elif rowKey.strip() != '' and rowKey not in rowMap :
            # else:
                newData.append([rowKey, ''] + row[2:])
                newData.append(['', month] + row[2:])
        
        return newData
    
    else:
        result = []
        for row in inputList:
            modified = row.copy()
            modified[0] = ''
            modified[1] = month
            result.append(row)
            result.append(modified)
        return result
    

def getTransaksiOnly(oldData:list = []):
    # oriData = oldData.copy()
    return [x for x in oldData if x[0]!= '']


def getBertambahBerkurangAll(oldData:list=[]):
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

def rekapMutasiPersediaan(saldo: int | str, bertambah: list = [0,0], berkurang: list = [0,0]):
    output = []
    sisa = ['',0]
    berkurang = [ toDefaultNumber(toPositif(col)) for col in berkurang ]

    sisa[1] = toDefaultNumber(parseNumber(saldo) + parseNumber(bertambah[1]) - parseNumber(berkurang[1]))

    output = ['', saldo] + bertambah + berkurang + sisa

    return [output]

def handlePenyusutan(pages: list[page.Page]) -> list:
    rowData = [0 for x in range(20)]
    total = 0
    # rowData = []

    for page in pages:
        table = page.extract_table()

        rowData[0] = 'Akumulasi Penyusutan'
        rowData[1] = ''

        # mencari jumlah pengeluaran di tiap transaksi
        if table:
            table = table[3:]
            # table = [row for row in table if row[2] != '' or row[2] != None]
            for row in table:
                if row[0] != 'J U M L A H' and '(' in row[2]:
                    # rowData.append(row)
                    # continue
                    if 'persediaan' in row[1].lower():
                        rowData[2] = toDefaultNumber(parseNumber(rowData[2]) + parseNumber(row[2]))
                    elif 'tanah' in row[1].lower():
                        rowData[4] = toDefaultNumber(parseNumber(rowData[4]) + parseNumber(row[2]))
                    elif 'peralatan dan mesin' in row[1].lower():
                        rowData[6] = toDefaultNumber(parseNumber(rowData[6]) + parseNumber(row[2]))
                    elif 'gedung dan bangunan' in row[1].lower():
                        rowData[8] = toDefaultNumber(parseNumber(rowData[8]) + parseNumber(row[2]))
                    elif 'jalan dan jembatan' in row[1].lower() or 'irigasi' in row[1].lower() or 'jaringan' in row[1].lower():
                        rowData[10] = toDefaultNumber(parseNumber(rowData[10]) + parseNumber(row[2]))
                    elif 'aset tetap lainnya' in row[1].lower():
                        rowData[12] = toDefaultNumber(parseNumber(rowData[12]) + parseNumber(row[2]))
                    elif 'hak cipta' in row[1].lower() or 'lisensi' in row[1].lower() or 'software' in row[1].lower() or 'aset tak berwujud' in row[1].lower():
                        rowData[16] = toDefaultNumber(parseNumber(rowData[16]) + parseNumber(row[2]))
                    elif'aset tetap yang tidak digunakan' in row[1].lower():
                        rowData[18] = toDefaultNumber(parseNumber(rowData[18]) + parseNumber(row[2]))
                    total = toDefaultNumber(parseNumber(total) + parseNumber(row[2]))
    rowData[-1] = total
    return rowData

def handleSaldoTerakhir(oldSaldo:list, penyusutan:list) -> list:
    oriOldSaldo = oldSaldo.copy()
    oriPenyusutan = penyusutan.copy()
    saldoTerakhir = []
    return saldoTerakhir

def handleLaporanKdp(pages: list[page.Page], saldo:list):
    return saldo

def handleLaporanAtb(pages: list[page.Page], saldo:list):
    for page in pages:
        table = page.extract_table()
        if table:
            table = table[4:]
            for row in table:
                if row[2] == '' and  row[1] != '':
                    saldo[15] = toDefaultNumber(parseNumber(saldo[15]) + parseNumber(row[9]))
    return saldo