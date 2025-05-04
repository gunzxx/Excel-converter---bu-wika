from flask import Blueprint, render_template, request, send_file
import pdfplumber
from time import time
import re
import pandas as pd

from function.tahunan import pdfToList, handleAddData

tahunan = Blueprint('tahunan', __name__)

@tahunan.route('/tahunan')
def tahunan_get():
    return render_template('tahunan.html')


@tahunan.route('/tahunan', methods=['POST'])
def tahunan_post():
    file = request.files['pdf']
    finishData = []

    with pdfplumber.open(file) as pdf:
        finishData = pdfToList(pdf.pages)
    
    # return finishData
    
    output_path = 'output/'+str(time())+".xlsx"
    
    headerTable = ['KETERANGAN', '', 'Persediaan', '', 'Tanah', '', 'Peralatan dan Mesin', '', 'Gedung dan Bangunan', '', 'Jalan, Irigasi, Jaringan & Jembatan', '', 'Aset Tetap Lainnya', '', 'KDP', '', 'Aset Tidak Wujud', '', 'Aset Tidak Operasional', 'Total']
    df = pd.DataFrame(finishData, columns=headerTable)

    df.to_excel(output_path, index=False)
    
    return send_file(output_path, as_attachment=True)