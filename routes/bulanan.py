from flask import Blueprint, render_template, request, send_file, current_app, jsonify
import pdfplumber
from time import time
import pandas as pd
from pathlib import Path
from datetime import datetime
import os

# import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../function')))
from function.bulanan import handleAddData, pdfToList, getTransaksiOnly, handleMutasiTransaksi, getTransaksiBertambah, getTransaksiBerkurang, getKolomBertambah, getKolomBerkurang

bulanan = Blueprint('bulanan', __name__)

BASE_FOLDER = os.path.abspath('static/output/bulanan')

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
    peralatanDanMesinBertambah = getKolomBertambah(transaksiOnly, 6)
    peralatanDanMesinBerkurang = getKolomBerkurang(transaksiOnly, 6)
    gedungDanBangunanBertambah = getKolomBertambah(transaksiOnly, 8)
    gedungDanBangunanBerkurang = getKolomBerkurang(transaksiOnly, 8)
    jalanIrigasiBertambah = getKolomBertambah(transaksiOnly, 10)
    jalanIrigasiBerkurang = getKolomBerkurang(transaksiOnly, 10)
    asetTetapLainnyaBertambah = getKolomBertambah(transaksiOnly, 12)
    asetTetapLainnyaBerkurang = getKolomBerkurang(transaksiOnly, 12)
    kdpBertambah = getKolomBertambah(transaksiOnly, 14)
    kdpBerkurang = getKolomBerkurang(transaksiOnly, 14)
    asetTidakWujudBertambah = getKolomBertambah(transaksiOnly, 16)
    asetTidakWujudBerkurang = getKolomBerkurang(transaksiOnly, 16)
    asetTidakOperasionalBertambah = getKolomBertambah(transaksiOnly, 18)
    asetTidakOperasionalBerkurang = getKolomBerkurang(transaksiOnly, 18)
    allBertambah = getTransaksiBertambah(transaksiOnly)
    allBerkurang = getTransaksiBerkurang(transaksiOnly)
    # return berkurang

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
    
    output_path = 'static/output/bulanan/'+str(time())+".xlsx"
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


@bulanan.route('/bulanan', methods=['DELETE'])
def bulanan_delete():
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