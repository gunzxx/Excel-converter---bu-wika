from flask import Blueprint, render_template, request, send_file, current_app
import pdfplumber
from time import time
import pandas as pd
from pathlib import Path
from datetime import datetime

# import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../function')))
from function.bulanan import handleAddData, pdfToList, getTransaksiOnly, handleMutasiTransaksi, getTransaksiBertambah, getTransaksiBerkurang

bulanan = Blueprint('bulanan', __name__)

@bulanan.route('/bulanan')
def bulanan_get():
    folderStatic = Path(current_app.static_folder)/'output/bulanan'
    results = [f.name for f in folderStatic.glob('*.xlsx')]
    reports = [
        [
            report,
            datetime.fromtimestamp(float(report[:-5])).strftime("%d-%m-%Y %H:%M:%S")
        ]
        for report in results
    ]
    reports.reverse()

    return render_template('bulanan.html', reports=reports)
    
@bulanan.route('/bulanan', methods=['POST'])
def bulanan_post():
    files = request.files.getlist('pdf')

    headerTable = ['KETERANGAN', '', 'Persediaan', '', 'Tanah', '', 'Peralatan dan Mesin', '', 'Gedung dan Bangunan', '', 'Jalan, Irigasi, Jaringan & Jembatan', '', 'Aset Tetap Lainnya', '', 'KDP', '', 'Aset Tidak Wujud', '', 'Aset Tidak Operasional', 'Total']

    finishData = []

    if(files[0]):
        with pdfplumber.open(files[0]) as pdf:
            data1 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data1, month="JANUARI")
    if(files[1]):
        with pdfplumber.open(files[1]) as pdf:
            data2 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data2, month="FEBRUARI")
    if(files[2]):
        with pdfplumber.open(files[2]) as pdf:
            data3 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data3, month="MARET")
    if(files[3]):
        with pdfplumber.open(files[3]) as pdf:
            data4 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data4, month="APRIL")
    if(files[4]):
        with pdfplumber.open(files[4]) as pdf:
            data5 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data5, month="MEI")
    if(files[5]):
        with pdfplumber.open(files[5]) as pdf:
            data6 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data6, month="JUNI")
    if(files[6]):
        with pdfplumber.open(files[6]) as pdf:
            data7 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data7, month="JULI")
    if(files[7]):
        with pdfplumber.open(files[7]) as pdf:
            data8 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data8, month="AGUSTUS")
    if(files[8]):
        with pdfplumber.open(files[8]) as pdf:
            data9 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data9, month="SEPTEMBER")
    if(files[9]):
        with pdfplumber.open(files[9]) as pdf:
            data10 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data10, month="OKTOBER")
    if(files[10]):
        with pdfplumber.open(files[10]) as pdf:
            data11 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data11, month="NOVEMBER")
    if(files[11]):
        with pdfplumber.open(files[11]) as pdf:
            data12 = pdfToList(pages=pdf.pages)
            finishData = handleAddData(oldData=finishData, inputList=data12, month="DESEMBER")
    
    transaksiOnly = getTransaksiOnly(finishData)
    bertambahBerkurang = handleMutasiTransaksi(transaksiOnly)
    bertambah = getTransaksiBertambah(transaksiOnly)
    berkurang = getTransaksiBerkurang(transaksiOnly)
    headerBertambahBerkurang = ['No', 'Jenis Transaksi', 'Qty', 'Intrakompatabel']
    # return berkurang

    df1 = pd.DataFrame(finishData, columns=headerTable)
    df2 = pd.DataFrame(bertambahBerkurang, columns=headerTable)
    df3 = pd.DataFrame(bertambah, columns=headerBertambahBerkurang)
    df4 = pd.DataFrame(berkurang, columns=headerBertambahBerkurang)
    
    output_path = 'static/output/bulanan/'+str(time())+".xlsx"
    # df1.to_excel(output_path, index=False)
    with pd.ExcelWriter(output_path) as writer:
        df1.to_excel(writer, sheet_name='RINCIAN', index=False)
        df2.to_excel(writer, sheet_name='Bertambah dan Berkurang', index=False)
        df3.to_excel(writer, sheet_name='Bertambah', index=False)
        df4.to_excel(writer, sheet_name='Berkurang', index=False)
    return send_file(output_path, as_attachment=True)