from flask import Blueprint, render_template, request, send_file, current_app, jsonify
import pdfplumber
import pandas as pd
from os.path import abspath
from datetime import datetime
from time import time
from pathlib import Path

from function.compress import pdfToList

compress = Blueprint('compress', __name__)
BASE_FOLDER = abspath('static/output/compress')

@compress.route('/compress')
def compress_get():
    folderStatic = Path(current_app.static_folder)/'output/compress'
    results = [f.name for f in folderStatic.glob('*.xlsx')]
    reports = [
        [
            report,
            datetime.fromtimestamp(float(report[:-5])).strftime("%d-%m-%Y %H:%M:%S")
        ]
        for report in results
    ]
    reports.reverse()
    return render_template('compress.html', reports=reports)

@compress.route('/compress', methods=['POST'])
def compress_post():
    file = request.files['pdf']
    finishData = []

    with pdfplumber.open(file) as pdf:
        finishData = pdfToList(pdf.pages)

    finishFrame = pd.DataFrame([finishData])
    output_path = 'static/output/bulanan/'+str(time())+".xlsx"
    finishFrame.to_excel(output_path, index=False)
    return finishData
    return send_file(output_path, as_attachment=True)