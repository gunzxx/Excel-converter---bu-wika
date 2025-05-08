from flask import Blueprint, render_template, request, send_file, current_app
import pdfplumber
from time import time
import pandas as pd
from pathlib import Path
from datetime import datetime

from function.tahunan import pdfToList

tahunan = Blueprint('tahunan', __name__)

@tahunan.route('/tahunan')
def tahunan_get():
    folderStatic = Path(current_app.static_folder)/'output/tahunan'
    results = [f.name for f in folderStatic.glob('*.xlsx')]
    reports = [
        [
            report,
            datetime.fromtimestamp(float(report[:-5])).strftime("%d-%m-%Y %H:%M:%S")
        ]
        for report in results
    ]
    reports.reverse()
    return render_template('tahunan.html', reports=reports)


@tahunan.route('/tahunan', methods=['POST'])
def tahunan_post():
    file = request.files['pdf']
    finishData = []

    with pdfplumber.open(file) as pdf:
        finishData = pdfToList(pdf.pages)
    
    # return finishData
    
    output_path = 'static/output/tahunan/'+str(time())+".xlsx"
    
    headerTable = ['KETERANGAN', '', 'Persediaan', '', 'Tanah', '', 'Peralatan dan Mesin', '', 'Gedung dan Bangunan', '', 'Jalan, Irigasi, Jaringan & Jembatan', '', 'Aset Tetap Lainnya', '', 'KDP', '', 'Aset Tidak Wujud', '', 'Aset Tidak Operasional', 'Total']
    df = pd.DataFrame(finishData, columns=headerTable)

    df.to_excel(output_path, index=False)
    
    return send_file(output_path, as_attachment=True)