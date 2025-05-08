from pdfplumber import page
import re

from function.main_fuction import parseNumber, toDefaultNumber, addNumber


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