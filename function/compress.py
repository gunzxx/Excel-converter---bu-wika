from pdfplumber import page
from function.main_fuction import parseNumber, toDefaultNumber
from re import MULTILINE, IGNORECASE, findall

# def pdfToList(pages: list[page.Page]) -> list:
#     return []

def pdfToList(pages: list[page.Page]):
    rowData = ['','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    extract = []
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

    for page in pages[:len(pages)-1]:
        tahunAnggaran = ''
        text = page.extract_text()
        table = page.extract_table()

        # mencari tahun jenis anggaran
        if text:
            cocoks = findall(r'^tahun anggaran\s*(.*)', text, MULTILINE | IGNORECASE)
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