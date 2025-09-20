from flask import Blueprint, render_template, request, send_file, current_app, jsonify
import pdfplumber
from time import time
import pandas as pd
from pathlib import Path
from datetime import datetime
# import os
from os.path import abspath, join, exists
from os import remove

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../function')))
from function.bulanan import handleAddData, handleAddDoubleData, pdfToList, kdpPdfToList, atbPdfToList, handleSaldo, handleKuantitas, getTransaksiOnly, getBertambahBerkurangAll, getKolomBertambah, getKolomPersediaanBertambah, getKolomBerkurang, rekapMutasi, rekapMutasiPersediaan, handlePenyusutan, handleLaporanKdp, handleLaporanAtb

bulanan = Blueprint('bulanan', __name__)

BASE_FOLDER = abspath('static/output/bulanan')

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
    
@bulanan.route('/', methods=['POST'])
@bulanan.route('/bulanan', methods=['POST'])
def bulanan_post():
    laporans = request.files.getlist('laporan')
    
    saldoInput = request.files['saldo']
    kuantitasInput = request.files['kuantitas']
    laporanAtb = request.files['laporanAtb']
    
    kdpDatas = request.files.getlist('kdpDatas')
    atbDatas = request.files.getlist('atbDatas')

    finishData = []
    saldo = []
    penyusutan = []
    months = ['JANUARI', 'FEBRUARI', 'MARET', 'APRIL', 'MEI', 'JUNI', 'JULI', 'AGUSTUS', 'SEPTEMBER', 'OKTOBER', 'NOVEMBER', 'DESEMBER', 'INTRAKOMPTABEL', 'EKSTRAKOMPTABEL']


    for i in range(len(laporans)):
        if laporans[i]:
            with pdfplumber.open(laporans[i]) as pdf:
                data1 = pdfToList(pages=pdf.pages)
                finishData = handleAddData(oldData=finishData, inputList=data1, month=months[i])
    
    # return finishData
    tes = []
    for i in range(len(atbDatas)):
        if atbDatas[i]:
            with pdfplumber.open(atbDatas[i]) as pdf:
                atbData = atbPdfToList(pages=pdf.pages)
                finishData = handleAddDoubleData(oldData=finishData, newData=atbData, month=months[i])
    # return finishData

    
    for i in range(len(kdpDatas)):
        if kdpDatas[i]:
            with pdfplumber.open(kdpDatas[i]) as pdf:
                kdpData = kdpPdfToList(pages=pdf.pages)
                # tes.append(kdpData)
                finishData = handleAddDoubleData(oldData=finishData, newData=kdpData, month=months[i])
    # return tes
    # return finishData

        

    with pdfplumber.open(saldoInput) as pdf:
        saldo = handleSaldo(pages=pdf.pages)
        penyusutan = handlePenyusutan(pages=pdf.pages)
    with pdfplumber.open(kuantitasInput) as pdf:
        saldo = handleKuantitas(pages=pdf.pages, saldo=saldo)
        # penyusutan = handleKuantitas(pages=pdf.pages)
    # kuantitasFrame = pd.read_excel(kuantitasInput)
    # kuantitas = kuantitasFrame.values.tolist()[0]
    # saldo = handleKuantitas(kuantitas=kuantitas, saldo=saldo)
    # return saldo
    # with pdfplumber.open(laporanKdp) as pdf:
    #     saldo = handleLaporanKdp(pages=pdf.pages, saldo=saldo)
    with pdfplumber.open(laporanAtb) as pdf:
        saldo = handleLaporanAtb(pages=pdf.pages, saldo=saldo)
    # return saldo

    
    transaksiOnly = getTransaksiOnly(finishData)
    bertambahBerkurang = getBertambahBerkurangAll(transaksiOnly)
    
    finishData.insert(0, saldo)
    finishData.append(penyusutan)
    # return finishData
    
    persediaanBertambah = getKolomPersediaanBertambah(transaksiOnly, 2)
    persediaanBerkurang = getKolomBerkurang(transaksiOnly, 2)
    rekapPersediaan = rekapMutasiPersediaan(saldo=saldo[2], bertambah=persediaanBertambah[-1][2:4], berkurang=persediaanBerkurang[-1][2:4])
    
    tanahBertambah = getKolomBertambah(transaksiOnly, 4)
    tanahBerkurang = getKolomBerkurang(transaksiOnly, 4)
    rekapTanah = rekapMutasi([saldo[3], saldo[4]], tanahBertambah[-1][2:4], tanahBerkurang[-1][2:4])
    
    peralatanDanMesinBertambah = getKolomBertambah(transaksiOnly, 6)
    peralatanDanMesinBerkurang = getKolomBerkurang(transaksiOnly, 6)
    rekapPeralatanDanMesin = rekapMutasi([saldo[5], saldo[6]], peralatanDanMesinBertambah[-1][2:4], peralatanDanMesinBerkurang[-1][2:4])
    
    gedungDanBangunanBertambah = getKolomBertambah(transaksiOnly, 8)
    gedungDanBangunanBerkurang = getKolomBerkurang(transaksiOnly, 8)
    rekapGedungDanBangunan = rekapMutasi([saldo[7], saldo[8]], gedungDanBangunanBertambah[-1][2:4], gedungDanBangunanBerkurang[-1][2:4])
    
    jalanIrigasiBertambah = getKolomBertambah(transaksiOnly, 10)
    jalanIrigasiBerkurang = getKolomBerkurang(transaksiOnly, 10)
    rekapJalanIrigasi = rekapMutasi([saldo[9], saldo[10]], jalanIrigasiBertambah[-1][2:4], jalanIrigasiBerkurang[-1][2:4])
    
    asetTetapLainnyaBertambah = getKolomBertambah(transaksiOnly, 12)
    asetTetapLainnyaBerkurang = getKolomBerkurang(transaksiOnly, 12)
    rekapAsetTetapLainnya = rekapMutasi([saldo[11], saldo[12]], asetTetapLainnyaBertambah[-1][2:4], asetTetapLainnyaBerkurang[-1][2:4])
    
    kdpBertambah = getKolomBertambah(transaksiOnly, 14)
    kdpBerkurang = getKolomBerkurang(transaksiOnly, 14)
    rekapKdp = rekapMutasi([saldo[13], saldo[14]], kdpBertambah[-1][2:4], kdpBerkurang[-1][2:4])
    
    asetTidakWujudBertambah = getKolomBertambah(transaksiOnly, 16)
    asetTidakWujudBerkurang = getKolomBerkurang(transaksiOnly, 16)
    rekapAsetTidakWujud = rekapMutasi([saldo[15], saldo[16]], asetTidakWujudBertambah[-1][2:4], asetTidakWujudBerkurang[-1][2:4])
    
    asetTidakOperasionalBertambah = getKolomBertambah(transaksiOnly, 18)
    asetTidakOperasionalBerkurang = getKolomBerkurang(transaksiOnly, 18)
    rekapAsetTidakOperasional = rekapMutasi([saldo[17], saldo[18]], asetTidakOperasionalBertambah[-1][2:4], asetTidakOperasionalBerkurang[-1][2:4])
    # return rekapPersediaan

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
    
    output_path = 'static/output/bulanan/'+str(time())+".xlsx"
    with pd.ExcelWriter(output_path) as writer:
        rincian.to_excel(writer, sheet_name='RINCIAN', index=False)
        sheetBertambahBerkurang.to_excel(writer, sheet_name='RINCIAN', index=False, startrow=len(rincian) + 3)
        
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


@bulanan.route('/', methods=['DELETE'])
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
    file_path = join(BASE_FOLDER, filename)

    # Cek ulang agar file_path tetap di BASE_FOLDER (anti traversal check)
    if not file_path.startswith(BASE_FOLDER):
        return jsonify({'error': 'Invalid file path detected'}), 400

    if not exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        remove(file_path)
        return jsonify({'message': f'File {filename} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500