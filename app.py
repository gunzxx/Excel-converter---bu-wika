from flask import Flask, request, send_file, render_template
import pandas as pd
import pdfplumber
import re
from time import time

app = Flask(__name__, template_folder="pages", static_folder="static")

@app.route('/')
def home():
    return render_template('index.html')

def is_blue(color):
    if not color:
        return False
    r, g, b = color
    return r < 0.3 and g < 0.3 and b > 0.7

def tambah_data(frameData, key, kolom_list, nilai_list):
    if key not in frameData:
        # Buat entri baru
        frameData[key] = {
            kolom: nilai.copy() for kolom, nilai in zip(kolom_list, nilai_list)
        }
    else:
        # Tambahkan ke entri yang sudah ada
        for kolom, nilai_baru in zip(kolom_list, nilai_list):
            if kolom in frameData[key]:
                frameData[key][kolom].extend(nilai_baru)
            else:
                frameData[key][kolom] = nilai_baru.copy()

        # Opsional: hilangkan duplikat & jaga urutan
        for kolom in frameData[key]:
            frameData[key][kolom] = list(dict.fromkeys(frameData[key][kolom]))


@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['pdf']
    
    # filtered_data = []
    hasilTransaksi = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            table = page.extract_table()
            jenisTransaksi = ''
            rowData = ['',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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
            if len(hasilTransaksi) > 0:
                if(hasilTransaksi[-1][1] == jenisTransaksi):
                    rowData = hasilTransaksi[-1]
                else:
                    rowData[0] = jenisTransaksi
                    # rowData = [jenisTransaksi,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            else:
                rowData[0] = jenisTransaksi

            # mencari jumlah pengeluaran di tiap transaksi
            if table:
                for row in table:
                    col2 = row[1]
                    col3 = row[2]
                    if row[0].lower() == 'T O T A L'.lower():
                        rowData[18] = row[3]

                    elif col2 and col2.strip() != 'URAIAN' and (not col3 or col3.strip() == ''):
                        if(row[1].lower() == 'peralatan dan mesin'):
                            rowData[4] = row[3]
                            rowData[5] = row[4]
                        elif(row[1].lower() in 'gedung dan bangunan'):
                            rowData[6] = row[3]
                            rowData[7] = row[4]
                        elif(row[1].lower() in 'jalan, irigasi, jaringan, dan jembatan'):
                            rowData[8] = row[3]
                            rowData[9] = row[4]
                        elif(row[1].lower() in 'aset tetap lainnya'):
                            rowData[10] = row[3]
                            rowData[11] = row[4]
                        elif(row[1].lower() in 'hak cipta, software'):
                            rowData[14] = row[3]
                            rowData[15] = row[4]
                        elif('166112' == row[0]):
                            rowData[16] = row[3]
                            rowData[17] = row[4]
                        else:
                            continue
                    else:
                        continue

            # if len(hasilTransaksi) > 0:
            #     if(hasilTransaksi[-1][0] == jenisTransaksi):
            #         hasilTransaksi[-1] =  rowData
            #     else:
            #         hasilTransaksi.append(rowData)
            # else:
            #     hasilTransaksi.append(rowData)
            hasilTransaksi.append(rowData)
        
    
    # output_path = "output.xlsx"
    output_path = str(time())+".xlsx"
    
    headerTable = ['KETERANGAN', 'Persediaan', '', 'Tanah', '', 'Peralatan dan Mesin', '', 'Gedung dan Bangunan', '', 'Jalan, Irigasi, Jaringan & Jembatan', '', 'Aset Tetap Lainnya', '', 'KDP', '', 'Aset Tidak Wujud', '', 'Aset Tidak Operasional', 'Total']
    df = pd.DataFrame(hasilTransaksi, columns=headerTable)


    def merge_values(group):
        return group.replace(0, None).bfill(axis=0).fillna(0).iloc[0]
    df_grouped = df.groupby("KETERANGAN", sort=False).agg(merge_values).reset_index()
    df_grouped.to_excel(output_path, index=False, header=headerTable)
    
    # df_unique = df.drop_duplicates()
    # df_unique.to_excel(output_path, index=False)
    
    return send_file(output_path, as_attachment=True)

    # tabel_html = df_grouped.to_html(index=False)
    # return render_template('table.html', tabel=tabel_html)

if __name__ == "__main__":
    app.run(debug=True)