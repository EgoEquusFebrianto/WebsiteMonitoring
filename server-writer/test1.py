import pandas as pd

# Load hasil prediksi
df = pd.read_csv("monitoring_data_predicted.csv")

# Pastikan kolom Label ada (hanya jika ingin dibandingkan dengan ground truth)
if 'Label' not in df.columns:
    raise ValueError("Kolom 'Label' tidak ditemukan di CSV. Tidak bisa dibandingkan.")

# Buat kolom baru untuk perbandingan (ubah ke lowercase semua)
label_lower = df['Label'].str.lower()
pred_lower = df['Prediction'].str.lower()

# Hitung jumlah yang sama dan berbeda
same_count = (label_lower == pred_lower).sum()
diff_count = (label_lower != pred_lower).sum()
total_count = len(df)

print(f"Total record: {total_count}")
print(f"Sama: {same_count}")
print(f"Berbeda: {diff_count}")
print(f"Persentase sama: {same_count/total_count*100:.2f}%")
print(f"Persentase berbeda: {diff_count/total_count*100:.2f}%")
