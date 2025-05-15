from flask import Blueprint, render_template, request, send_file, current_app, jsonify
import pdfplumber
from time import time
import pandas as pd
from pathlib import Path
from datetime import datetime
import os

from function.tahunan import pdfToList, handleMutasiTransaksi, getTransaksiBertambah, getTransaksiBerkurang

tahunan = Blueprint('tahunan', __name__)
BASE_FOLDER = os.path.abspath('static/output/tahunan')

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

    bertambahBerkurang = handleMutasiTransaksi(finishData)
    bertambah = getTransaksiBertambah(finishData)
    berkurang = getTransaksiBerkurang(finishData)
    
    output_path = 'static/output/tahunan/'+str(time())+".xlsx"
    
    headerTable = ['KETERANGAN', '', 'Persediaan', '', 'Tanah', '', 'Peralatan dan Mesin', '', 'Gedung dan Bangunan', '', 'Jalan, Irigasi, Jaringan & Jembatan', '', 'Aset Tetap Lainnya', '', 'KDP', '', 'Aset Tidak Wujud', '', 'Aset Tidak Operasional', 'Total']
    headerBertambahBerkurang = ['No', 'Jenis Transaksi', 'Qty', 'Intrakompatabel']
    df1 = pd.DataFrame(finishData, columns=headerTable)
    df2 = pd.DataFrame(bertambahBerkurang, columns=headerTable)
    df3 = pd.DataFrame(bertambah, columns=headerBertambahBerkurang)
    df4 = pd.DataFrame(berkurang, columns=headerBertambahBerkurang)

    with pd.ExcelWriter(output_path) as writer:
        df1.to_excel(writer, sheet_name='RINCIAN', index=False)
        df2.to_excel(writer, sheet_name='Bertambah dan Berkurang', index=False)
        df3.to_excel(writer, sheet_name='Bertambah', index=False)
        df4.to_excel(writer, sheet_name='Berkurang', index=False)
    
    return send_file(output_path, as_attachment=True)


@tahunan.route('/tahunan', methods=['DELETE'])
def tahunan_delete():
    data = request.get_json()

    if not data or 'filename' not in data:
        return jsonify({'error': 'Filename is required'}), 400
    
    filename = data.get('filename')

    # Cegah path traversal (hanya nama file yang diijinkan)
    if '/' in filename or '\\' in filename:
        return jsonify({'error': 'Invalid filename'}), 400

    # Buat path absolut dari base + filename
    file_path = os.path.join(BASE_FOLDER, filename)

    # Cek ulang agar file_path tetap di BASE_FOLDER (anti traversal check)
    if not file_path.startswith(BASE_FOLDER):
        return jsonify({'error': 'Invalid file path detected'}), 400

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        os.remove(file_path)
        return jsonify({'message': f'File {filename} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500