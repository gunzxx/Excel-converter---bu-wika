# Fungsi bantu untuk ubah nilai string jadi angka
def parseNumber(val) ->int:
    strExport = int(str(val).replace('(', '').replace(')', '').replace(',','').replace('.',''))
    return -strExport if "(" in str(val) else strExport

def parseNumber2(val):
    try:
        strExport = int(str(val).replace('(', '').replace(')', '').replace(',','').replace('.',''))
        return -strExport if "(" in str(val) else strExport
    except:
        return 0

# Fungsi untuk mengkonversi angka ke format sebelumnya:
def toDefaultNumber(val):
    # return f"({'{:,}'.format(val)})" if "(" in str(srcStr) else '{:,}'.format(val)
    return '{:,}'.format(val).replace(',','.')


# Fungsi untuk menambahkan data dengan tanda kurung
def addNumber(a, b):
    if isinstance(a, str) or isinstance(b, str):
        # Jika salah satu bentuknya dalam tanda kurung (negatif)
        a = parseNumber(a)
        b = parseNumber(b)
    # return parseNumber(a) + parseNumber(b)
    return a + b

def checkIsNumber(val)->bool:
    try:
        int(str(val).replace('(', '').replace(')', '').replace(',','').replace('.',''))
        return True
    except:
        return False

def toPositif(val)->bool:
    return abs(parseNumber(val))