import pandas as pd

# Data awal
data1 = [
    ['row1', '', 0, 1, 0, 0],
    ['row2', '', 0, 0, '2', 0],
    ['row3', '', 0, 0, 0, '(3)'],
]
data2 = [
    ['row2', '', 1, 0, '5', 9],
    ['row3', '', 0, 0, 4, '4'],
    ['row5', '', 12, 0, 0, 0],
]

# Konversi ke DataFrame
df1 = pd.DataFrame(data1, columns=['keterangan', 'bulan', 0, 1, 2, 3])
df2 = pd.DataFrame(data2, columns=['keterangan', 'bulan', 0, 1, 2, 3])

# Tandai sumber data
df1_src = df1.copy()
df1_src['keterangan'] = ''
df1_src['bulan'] = 'data1'

df2_src = df2.copy()
df2_src['keterangan'] = ''
df2_src['bulan'] = 'data2'

# Gabung semua key yang ada
all_keys = pd.unique(df1['keterangan'].tolist() + df2['keterangan'].tolist())

result = []

# Konversi nilai string ke angka jika bisa, jika tidak biarkan
def to_number(val):
    try:
        return int(str(val).replace('(', '').replace(')', ''))
    except:
        return val

# Konversi angka ke format sebelumnya:
def toDefaultNumber(val):
    return f"({val})" if "(" in val else val

for key in all_keys:
    row1 = df1[df1['keterangan'] == key]
    row2 = df2[df2['keterangan'] == key]

    # Gabungkan nilai
    if not row1.empty or not row2.empty:
        base = [key, '', 0, 0, 0, 0]
        for col in range(2, 6):
            val1 = row1.iloc[0, col] if not row1.empty else 0
            val2 = row2.iloc[0, col] if not row2.empty else 0
            try:
                v1 = to_number(val1)
                v2 = to_number(val2)
                base[col] = v1 + v2
                # Jika ada tanda kurung pada salah satu, tambahkan ke hasil
                if '(' in str(val1) or '(' in str(val2):
                    base[col] = f"({v1 + v2})"
            except:
                base[col] = val2 or val1
        result.append(base)

        # Tambahkan referensi baris data1
        if not row1.empty:
            result.append(df1_src[df1['keterangan'] == key].values.tolist()[0])

        # Tambahkan referensi baris data2
        if not row2.empty:
            result.append(df2_src[df2['keterangan'] == key].values.tolist()[0])

# Konversi ke DataFrame hasil
finish_df = pd.DataFrame(result, columns=['keterangan', 'bulan', 0, 1, 2, 3])

# Tampilkan hasil
print(finish_df.values.tolist())
