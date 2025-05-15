from flask import Blueprint, render_template, request, send_file, current_app, jsonify
import pdfplumber
from time import time
import pandas as pd
from pathlib import Path
from datetime import datetime
import os

from function.tahunan import pdfToList, handleMutasiTransaksi, getTransaksiBertambah, getTransaksiBerkurang, getKolomBertambah, getKolomBerkurang

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

    bertambahBerkurang = handleMutasiTransaksi(finishData)
    peralatanDanMesinBertambah = getKolomBertambah(finishData, 6)
    peralatanDanMesinBerkurang = getKolomBerkurang(finishData, 6)
    gedungDanBangunanBertambah = getKolomBertambah(finishData, 8)
    gedungDanBangunanBerkurang = getKolomBerkurang(finishData, 8)
    jalanIrigasiBertambah = getKolomBertambah(finishData, 10)
    jalanIrigasiBerkurang = getKolomBerkurang(finishData, 10)
    asetTetapLainnyaBertambah = getKolomBertambah(finishData, 12)
    asetTetapLainnyaBerkurang = getKolomBerkurang(finishData, 12)
    kdpBertambah = getKolomBertambah(finishData, 14)
    kdpBerkurang = getKolomBerkurang(finishData, 14)
    asetTidakWujudBertambah = getKolomBertambah(finishData, 16)
    asetTidakWujudBerkurang = getKolomBerkurang(finishData, 16)
    asetTidakOperasionalBertambah = getKolomBertambah(finishData, 18)
    asetTidakOperasionalBerkurang = getKolomBerkurang(finishData, 18)
    allBertambah = getTransaksiBertambah(finishData)
    allBerkurang = getTransaksiBerkurang(finishData)
    # return peralatanDanMesinBerkurang
    
    output_path = 'static/output/tahunan/'+str(time())+".xlsx"
    
    headerTable = ['KETERANGAN', '', 'Persediaan', '', 'Tanah', '', 'Peralatan dan Mesin', '', 'Gedung dan Bangunan', '', 'Jalan, Irigasi, Jaringan & Jembatan', '', 'Aset Tetap Lainnya', '', 'KDP', '', 'Aset Tidak Wujud', '', 'Aset Tidak Operasional', 'Total']
    headerBertambahBerkurang = ['No', 'Jenis Transaksi', 'Qty', 'Intrakompatabel']
    rincian = pd.DataFrame(finishData, columns=headerTable)
    sheetBertambahBerkurang = pd.DataFrame(bertambahBerkurang, columns=headerTable)
    sheetPeralatanDanMesinBertambah = pd.DataFrame(peralatanDanMesinBertambah, columns=headerBertambahBerkurang)
    sheetPeralatanDanMesinBerkurang = pd.DataFrame(peralatanDanMesinBerkurang, columns=headerBertambahBerkurang)
    sheetGedungDanBangunanBertambah = pd.DataFrame(gedungDanBangunanBertambah, columns=headerBertambahBerkurang)
    sheetGedungDanBangunanBerkurang = pd.DataFrame(gedungDanBangunanBerkurang, columns=headerBertambahBerkurang)
    sheetJalanIrigasiBertambah = pd.DataFrame(jalanIrigasiBertambah, columns=headerBertambahBerkurang)
    sheetJalanIrigasiBerkurang = pd.DataFrame(jalanIrigasiBerkurang, columns=headerBertambahBerkurang)
    sheetAsetTetapLainnyaBertambah = pd.DataFrame(asetTetapLainnyaBertambah, columns=headerBertambahBerkurang)
    sheetAsetTetapLainnyaBerkurang = pd.DataFrame(asetTetapLainnyaBerkurang, columns=headerBertambahBerkurang)
    sheetKdpBertambah = pd.DataFrame(kdpBertambah, columns=headerBertambahBerkurang)
    sheetKdpBerkurang = pd.DataFrame(kdpBerkurang, columns=headerBertambahBerkurang)
    sheetAsetTidakWujudBertambah = pd.DataFrame(asetTidakWujudBertambah, columns=headerBertambahBerkurang)
    sheetAsetTidakWujudBerkurang = pd.DataFrame(asetTidakWujudBerkurang, columns=headerBertambahBerkurang)
    sheetAsetTidakOperasionalBertambah = pd.DataFrame(asetTidakOperasionalBertambah, columns=headerBertambahBerkurang)
    sheetAsetTidakOperasionalBerkurang = pd.DataFrame(asetTidakOperasionalBerkurang, columns=headerBertambahBerkurang)
    sheetAllBertambah = pd.DataFrame(allBertambah, columns=headerBertambahBerkurang)
    sheetAllBerkurang = pd.DataFrame(allBerkurang, columns=headerBertambahBerkurang)

    with pd.ExcelWriter(output_path) as writer:
        rincian.to_excel(writer, sheet_name='RINCIAN', index=False)
        sheetBertambahBerkurang.to_excel(writer, sheet_name='Bertambah dan Berkurang', index=False)
        sheetPeralatanDanMesinBertambah.to_excel(writer, sheet_name="Peralatan dan Mesin", index=False, startrow=0)
        sheetPeralatanDanMesinBerkurang.to_excel(writer, sheet_name="Peralatan dan Mesin", index=False, startrow=len(sheetPeralatanDanMesinBertambah) + 3)
        sheetGedungDanBangunanBertambah.to_excel(writer, sheet_name="Gedung dan Bangunan", index=False, startrow=0)
        sheetGedungDanBangunanBerkurang.to_excel(writer, sheet_name="Gedung dan Bangunan", index=False, startrow=len(sheetGedungDanBangunanBertambah) + 3)
        sheetJalanIrigasiBertambah.to_excel(writer, sheet_name="Jalan, Irigasi, Jaringan & Jembatan", index=False, startrow=0)
        sheetJalanIrigasiBerkurang.to_excel(writer, sheet_name="Jalan, Irigasi, Jaringan & Jembatan", index=False, startrow=len(sheetJalanIrigasiBertambah) + 3)
        sheetAsetTetapLainnyaBertambah.to_excel(writer, sheet_name="Aset Tetap Lainnya", index=False, startrow=0)
        sheetAsetTetapLainnyaBerkurang.to_excel(writer, sheet_name="Aset Tetap Lainnya", index=False, startrow=len(sheetAsetTetapLainnyaBertambah) + 3)
        sheetKdpBertambah.to_excel(writer, sheet_name="KDP", index=False, startrow=0)
        sheetKdpBerkurang.to_excel(writer, sheet_name="KDP", index=False, startrow=len(sheetKdpBertambah) + 3)
        sheetAsetTidakWujudBertambah.to_excel(writer, sheet_name="Aset Tidak Wujud", index=False, startrow=0)
        sheetAsetTidakWujudBerkurang.to_excel(writer, sheet_name="Aset Tidak Wujud", index=False, startrow=len(sheetAsetTidakWujudBertambah) + 3)
        sheetAsetTidakOperasionalBertambah.to_excel(writer, sheet_name="Aset Tidak Operasional", index=False, startrow=0)
        sheetAsetTidakOperasionalBerkurang.to_excel(writer, sheet_name="Aset Tidak Operasional", index=False, startrow=len(sheetAsetTidakOperasionalBertambah) + 3)
        sheetAllBertambah.to_excel(writer, sheet_name='Total Bertambah Semua Jenis Transaksi', index=False)
        sheetAllBerkurang.to_excel(writer, sheet_name='Total Berkurang Semua Jenis Transaksi', index=False)
    
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