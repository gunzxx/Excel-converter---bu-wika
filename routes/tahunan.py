from flask import Blueprint, render_template, request, send_file, current_app, jsonify
import pdfplumber
import pandas as pd
from time import time
from pathlib import Path
from datetime import datetime
import os

from function.tahunan import pdfToList, handleMutasiTransaksi, getKolomPersediaanBertambah, getKolomBertambah, getKolomBerkurang, rekapMutasi

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

    persediaanBertambah = getKolomPersediaanBertambah(finishData, 2)
    persediaanBerkurang = getKolomBerkurang(finishData, 2)
    rekapPersediaan = rekapMutasi([0,0], persediaanBertambah[-1][2:4], persediaanBerkurang[-1][2:4])
    
    tanahBertambah = getKolomBertambah(finishData, 4)
    tanahBerkurang = getKolomBerkurang(finishData, 4)
    rekapTanah = rekapMutasi([0,0], tanahBertambah[-1][2:4], tanahBerkurang[-1][2:4])
    
    peralatanDanMesinBertambah = getKolomBertambah(finishData, 6)
    peralatanDanMesinBerkurang = getKolomBerkurang(finishData, 6)
    rekapPeralatanDanMesin = rekapMutasi([0,0], peralatanDanMesinBertambah[-1][2:4], peralatanDanMesinBerkurang[-1][2:4])
    
    gedungDanBangunanBertambah = getKolomBertambah(finishData, 8)
    gedungDanBangunanBerkurang = getKolomBerkurang(finishData, 8)
    rekapGedungDanBangunan = rekapMutasi([0,0], gedungDanBangunanBertambah[-1][2:4], gedungDanBangunanBerkurang[-1][2:4])
    
    jalanIrigasiBertambah = getKolomBertambah(finishData, 10)
    jalanIrigasiBerkurang = getKolomBerkurang(finishData, 10)
    rekapJalanIrigasi = rekapMutasi([0,0], jalanIrigasiBertambah[-1][2:4], jalanIrigasiBerkurang[-1][2:4])
    
    asetTetapLainnyaBertambah = getKolomBertambah(finishData, 12)
    asetTetapLainnyaBerkurang = getKolomBerkurang(finishData, 12)
    rekapAsetTetapLainnya = rekapMutasi([0,0], asetTetapLainnyaBertambah[-1][2:4], asetTetapLainnyaBerkurang[-1][2:4])
    
    kdpBertambah = getKolomBertambah(finishData, 14)
    kdpBerkurang = getKolomBerkurang(finishData, 14)
    rekapKdp = rekapMutasi([0,0], kdpBertambah[-1][2:4], kdpBerkurang[-1][2:4])
    
    asetTidakWujudBertambah = getKolomBertambah(finishData, 16)
    asetTidakWujudBerkurang = getKolomBerkurang(finishData, 16)
    rekapAsetTidakWujud = rekapMutasi([0,0], asetTidakWujudBertambah[-1][2:4], asetTidakWujudBerkurang[-1][2:4])
    
    asetTidakOperasionalBertambah = getKolomBertambah(finishData, 18)
    asetTidakOperasionalBerkurang = getKolomBerkurang(finishData, 18)
    rekapAsetTidakOperasional = rekapMutasi([0,0], asetTidakOperasionalBertambah[-1][2:4], asetTidakOperasionalBerkurang[-1][2:4])
    # return rekapPeralatanDanMesin
    
    output_path = 'static/output/tahunan/'+str(time())+".xlsx"
    
    headerTable = ['KETERANGAN', '', 'Persediaan', '', 'Tanah', '', 'Peralatan dan Mesin', '', 'Gedung dan Bangunan', '', 'Jalan, Irigasi, Jaringan & Jembatan', '', 'Aset Tetap Lainnya', '', 'KDP', '', 'Aset Tidak Wujud', '', 'Aset Tidak Operasional', 'Total']
    headerBertambahBerkurang = ['No', 'Jenis Transaksi', 'Qty', 'Intrakomptabel']
    headerMutasi = ['Kuantitas', 'Niai/Harga(Rp)', 'Kuantitas', 'Niai/Harga(Rp)', 'Kuantitas', 'Niai/Harga(Rp)', 'Kuantitas', 'Niai/Harga(Rp)']
    rincian = pd.DataFrame(finishData, columns=headerTable)
    sheetBertambahBerkurang = pd.DataFrame(bertambahBerkurang, columns=headerTable)
    
    sheetPersediaanBertambah = pd.DataFrame(persediaanBertambah, columns=headerBertambahBerkurang)
    sheetPersediaanBerkurang = pd.DataFrame(persediaanBerkurang, columns=headerBertambahBerkurang)
    srPersediaan = pd.DataFrame(rekapPersediaan, columns=headerMutasi)
    
    sheetTanahBertambah = pd.DataFrame(tanahBertambah, columns=headerBertambahBerkurang)
    sheetTanahBerkurang = pd.DataFrame(tanahBerkurang, columns=headerBertambahBerkurang)
    srTanah = pd.DataFrame(rekapTanah, columns=headerMutasi)
    
    sheetPeralatanDanMesinBertambah = pd.DataFrame(peralatanDanMesinBertambah, columns=headerBertambahBerkurang)
    sheetPeralatanDanMesinBerkurang = pd.DataFrame(peralatanDanMesinBerkurang, columns=headerBertambahBerkurang)
    srPeralatanDanMesin = pd.DataFrame(rekapPeralatanDanMesin, columns=headerMutasi)
    
    sheetGedungDanBangunanBertambah = pd.DataFrame(gedungDanBangunanBertambah, columns=headerBertambahBerkurang)
    sheetGedungDanBangunanBerkurang = pd.DataFrame(gedungDanBangunanBerkurang, columns=headerBertambahBerkurang)
    srGedungDanBangunan = pd.DataFrame(rekapGedungDanBangunan, columns=headerMutasi)
    
    sheetJalanIrigasiBertambah = pd.DataFrame(jalanIrigasiBertambah, columns=headerBertambahBerkurang)
    sheetJalanIrigasiBerkurang = pd.DataFrame(jalanIrigasiBerkurang, columns=headerBertambahBerkurang)
    srJalanIrigasi = pd.DataFrame(rekapJalanIrigasi, columns=headerMutasi)
    
    sheetAsetTetapLainnyaBertambah = pd.DataFrame(asetTetapLainnyaBertambah, columns=headerBertambahBerkurang)
    sheetAsetTetapLainnyaBerkurang = pd.DataFrame(asetTetapLainnyaBerkurang, columns=headerBertambahBerkurang)
    srAsetTetapLainnya = pd.DataFrame(rekapAsetTetapLainnya, columns=headerMutasi)
    
    sheetKdpBertambah = pd.DataFrame(kdpBertambah, columns=headerBertambahBerkurang)
    sheetKdpBerkurang = pd.DataFrame(kdpBerkurang, columns=headerBertambahBerkurang)
    srKdp = pd.DataFrame(rekapKdp, columns=headerMutasi)
    
    sheetAsetTidakWujudBertambah = pd.DataFrame(asetTidakWujudBertambah, columns=headerBertambahBerkurang)
    sheetAsetTidakWujudBerkurang = pd.DataFrame(asetTidakWujudBerkurang, columns=headerBertambahBerkurang)
    srAsetTidakWujud = pd.DataFrame(rekapAsetTidakWujud, columns=headerMutasi)
    
    sheetAsetTidakOperasionalBertambah = pd.DataFrame(asetTidakOperasionalBertambah, columns=headerBertambahBerkurang)
    sheetAsetTidakOperasionalBerkurang = pd.DataFrame(asetTidakOperasionalBerkurang, columns=headerBertambahBerkurang)
    srAsetTidakOperasional = pd.DataFrame(rekapAsetTidakOperasional, columns=headerMutasi)

    output_path = 'static/output/tahunan/'+str(time())+".xlsx"
    with pd.ExcelWriter(output_path) as writer:
        rincian.to_excel(writer, sheet_name='RINCIAN', index=False)
        sheetBertambahBerkurang.to_excel(writer, sheet_name='Bertambah dan Berkurang', index=False)
        
        sheetPersediaanBertambah.to_excel(writer, sheet_name="Persediaan", index=False, startrow=0)
        sheetPersediaanBerkurang.to_excel(writer, sheet_name="Persediaan", index=False, startrow=len(sheetPersediaanBertambah) + 3)
        srPersediaan.to_excel(writer, sheet_name="Persediaan", index=False, startrow=len(sheetPersediaanBertambah) + len(sheetPersediaanBerkurang) + 6)
        
        sheetTanahBertambah.to_excel(writer, sheet_name="Tanah", index=False, startrow=0)
        sheetTanahBerkurang.to_excel(writer, sheet_name="Tanah", index=False, startrow=len(sheetTanahBertambah) + 3)
        srTanah.to_excel(writer, sheet_name="Tanah", index=False, startrow=len(sheetTanahBertambah) + len(sheetTanahBerkurang) + 6)
        
        sheetPeralatanDanMesinBertambah.to_excel(writer, sheet_name="Peralatan dan Mesin", index=False, startrow=0)
        sheetPeralatanDanMesinBerkurang.to_excel(writer, sheet_name="Peralatan dan Mesin", index=False, startrow=len(sheetPeralatanDanMesinBertambah) + 3)
        srPeralatanDanMesin.to_excel(writer, sheet_name="Peralatan dan Mesin", index=False, startrow=len(sheetPeralatanDanMesinBertambah) + len(sheetPeralatanDanMesinBerkurang) + 6)
        
        sheetGedungDanBangunanBertambah.to_excel(writer, sheet_name="Gedung dan Bangunan", index=False, startrow=0)
        sheetGedungDanBangunanBerkurang.to_excel(writer, sheet_name="Gedung dan Bangunan", index=False, startrow=len(sheetGedungDanBangunanBertambah) + 3)
        srGedungDanBangunan.to_excel(writer, sheet_name="Gedung dan Bangunan", index=False, startrow=len(sheetGedungDanBangunanBertambah) + len(sheetGedungDanBangunanBerkurang) + 6)
        
        sheetJalanIrigasiBertambah.to_excel(writer, sheet_name="Jalan, Irigasi, Jaringan & Jembatan", index=False, startrow=0)
        sheetJalanIrigasiBerkurang.to_excel(writer, sheet_name="Jalan, Irigasi, Jaringan & Jembatan", index=False, startrow=len(sheetJalanIrigasiBertambah) + 3)
        srJalanIrigasi.to_excel(writer, sheet_name="Jalan, Irigasi, Jaringan & Jembatan", index=False, startrow=len(sheetJalanIrigasiBertambah) + len(sheetJalanIrigasiBerkurang) + 6)
        
        sheetAsetTetapLainnyaBertambah.to_excel(writer, sheet_name="Aset Tetap Lainnya", index=False, startrow=0)
        sheetAsetTetapLainnyaBerkurang.to_excel(writer, sheet_name="Aset Tetap Lainnya", index=False, startrow=len(sheetAsetTetapLainnyaBertambah) + 3)
        srAsetTetapLainnya.to_excel(writer, sheet_name="Aset Tetap Lainnya", index=False, startrow=len(sheetAsetTetapLainnyaBertambah) + len(sheetAsetTetapLainnyaBerkurang) + 6)
        
        sheetKdpBertambah.to_excel(writer, sheet_name="KDP", index=False, startrow=0)
        sheetKdpBerkurang.to_excel(writer, sheet_name="KDP", index=False, startrow=len(sheetKdpBertambah) + 3)
        srKdp.to_excel(writer, sheet_name="KDP", index=False, startrow=len(sheetKdpBertambah) + len(sheetKdpBerkurang) + 6)
        
        sheetAsetTidakWujudBertambah.to_excel(writer, sheet_name="Aset Tidak Wujud", index=False, startrow=0)
        sheetAsetTidakWujudBerkurang.to_excel(writer, sheet_name="Aset Tidak Wujud", index=False, startrow=len(sheetAsetTidakWujudBertambah) + 3)
        srAsetTidakWujud.to_excel(writer, sheet_name="Aset Tidak Wujud", index=False, startrow=len(sheetAsetTidakWujudBertambah) + len(sheetAsetTidakWujudBerkurang) + 6)
        
        sheetAsetTidakOperasionalBertambah.to_excel(writer, sheet_name="Aset Tidak Operasional", index=False, startrow=0)
        sheetAsetTidakOperasionalBerkurang.to_excel(writer, sheet_name="Aset Tidak Operasional", index=False, startrow=len(sheetAsetTidakOperasionalBertambah) + 3)
        srAsetTidakOperasional.to_excel(writer, sheet_name="Aset Tidak Operasional", index=False, startrow=len(sheetAsetTidakOperasionalBertambah) + len(sheetAsetTidakOperasionalBerkurang) + 6)
    
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