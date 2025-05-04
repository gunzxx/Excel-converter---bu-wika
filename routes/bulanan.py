from flask import Blueprint, render_template, request, send_file, jsonify
import pdfplumber
from time import time
import pandas as pd

# import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../function')))
from function.bulanan import handleAddData, pdfToList

bulanan = Blueprint('bulanan', __name__)

@bulanan.route('/bulanan')
def bulanan_get():
    return render_template('bulanan.html')
    
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
    
    # return [data1, finishData]
    # return data2

    df = pd.DataFrame(finishData, columns=headerTable)
    # df = pd.DataFrame(finishData)
    output_path = 'output/'+str(time())+".xlsx"
    df.to_excel(output_path, index=False)
    return send_file(output_path, as_attachment=True)