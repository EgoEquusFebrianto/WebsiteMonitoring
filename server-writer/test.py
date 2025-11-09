# import pandas as pd
# import numpy as np
# from joblib import load
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score
# import seaborn as sns
# import matplotlib.pyplot as plt

# # ======== Load Model dan Scaler ========
# model_path = "models/logistic_regression_ddos.joblib"
# scaler_path = "models/scaler_ddos.joblib"
# model = load(model_path)
# scaler = load(scaler_path)

# # ======== Load Dataset Monitoring ========
# monitoring_file = "monitoring_data.csv"
# selected_features = [
#     'Flow_Duration', 'Total_Fwd_Packets', 'Total_Backward_Packets',
#     'Flow_Bytes/s', 'Flow_Packets/s',
#     'Min_Packet_Length', 'Max_Packet_Length', 'Packet_Length_Mean',
#     'Packet_Length_Std', 'Packet_Length_Variance',
#     'Flow_IAT_Mean', 'Flow_IAT_Std', 'Fwd_IAT_Mean', 'Fwd_IAT_Std',
#     'Bwd_IAT_Mean', 'Bwd_IAT_Std',
#     'SYN_Flag_Count', 'RST_Flag_Count', 'ACK_Flag_Count',
#     'Fwd_Header_Length', 'Bwd_Header_Length',
#     'Subflow_Fwd_Packets', 'Subflow_Bwd_Packets',
#     'Subflow_Fwd_Bytes', 'Subflow_Bwd_Bytes',
#     'Init_Win_bytes_forward', 'Init_Win_bytes_backward'
# ]

# df = pd.read_csv(monitoring_file)
# df.columns = df.columns.str.strip().str.replace(' ', '_')

# # Pastikan Label ada
# if 'Label' not in df.columns:
#     raise ValueError("Dataset harus memiliki kolom 'Label' sebagai target")

# # Mapping label string ke angka
# label_mapping = {'BENIGN': 0, 'DDoS': 1}
# y_true = df['Label'].map(label_mapping)

# # Ambil fitur
# X = df[selected_features].replace([np.inf, -np.inf], np.nan).fillna(0)

# # ======== Scaling dengan Scaler dari Training ========
# X_scaled = scaler.transform(X)

# # ======== Prediksi ========
# threshold = 0.5  # bisa diubah, misal 0.3 untuk meningkatkan recall DDOS
# y_prob = model.predict_proba(X_scaled)[:,1]
# y_pred = (y_prob >= threshold).astype(int)

# # ======== Evaluasi ========
# accuracy = accuracy_score(y_true, y_pred)
# precision = precision_score(y_true, y_pred)
# recall = recall_score(y_true, y_pred)
# f1 = f1_score(y_true, y_pred)
# roc_auc = roc_auc_score(y_true, y_prob)
# cm = confusion_matrix(y_true, y_pred)
# report = classification_report(y_true, y_pred, target_names=['BENIGN','DDoS'])

# print("=== Performance Metrics ===")
# print(f"Akurasi  : {accuracy:.4f}")
# print(f"Precision: {precision:.4f}")
# print(f"Recall   : {recall:.4f}")
# print(f"F1-score : {f1:.4f}")
# print(f"ROC-AUC  : {roc_auc:.4f}\n")
# print("Classification Report:")
# print(report)

# # ======== Visualisasi Confusion Matrix ========
# plt.figure(figsize=(5,4))
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['BENIGN','DDoS'], yticklabels=['BENIGN','DDoS'])
# plt.xlabel("Predicted Label")
# plt.ylabel("True Label")
# plt.title(f"Confusion Matrix - Threshold {threshold}")
# plt.show()

# # ======== Prediksi per baris (String) ========
# df['Prediction'] = np.where(y_pred==1, 'DDoS','BENIGN')
# print("5 baris prediksi pertama:")
# print(df[['Prediction']].head())

import pandas as pd
import numpy as np
from joblib import load
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

# ======== Paths ========
model_path = "models/logistic_regression_ddos.joblib"
scaler_path = "models/scaler_ddos.joblib"
monitoring_file = "monitoring_data.csv"

# ======== Load model dan scaler ========
model = load(model_path)
scaler = load(scaler_path)

# ======== Load monitoring data ========
df = pd.read_csv(monitoring_file)
df.columns = df.columns.str.strip().str.replace(' ', '_')

# ======== Pilih fitur ========
selected_features = [
    'Flow_Duration', 'Total_Fwd_Packets', 'Total_Backward_Packets',
    'Flow_Bytes/s', 'Flow_Packets/s',
    'Min_Packet_Length', 'Max_Packet_Length', 'Packet_Length_Mean',
    'Packet_Length_Std', 'Packet_Length_Variance',
    'Flow_IAT_Mean', 'Flow_IAT_Std', 'Fwd_IAT_Mean', 'Fwd_IAT_Std',
    'Bwd_IAT_Mean', 'Bwd_IAT_Std',
    'SYN_Flag_Count', 'RST_Flag_Count', 'ACK_Flag_Count',
    'Fwd_Header_Length', 'Bwd_Header_Length',
    'Subflow_Fwd_Packets', 'Subflow_Bwd_Packets',
    'Subflow_Fwd_Bytes', 'Subflow_Bwd_Bytes',
    'Init_Win_bytes_forward', 'Init_Win_bytes_backward'
]

X_monitoring = df[selected_features].replace([np.inf, -np.inf], np.nan).fillna(0)

# ======== Scaling ========
X_scaled = scaler.transform(X_monitoring)

# ======== Prediksi ========
threshold = 0.5  # bisa diubah untuk meningkatkan recall DDOS
y_prob = model.predict_proba(X_scaled)[:, 1]
y_pred = (y_prob >= threshold).astype(int)

# ======== Tambahkan kolom Prediction (string) ========
df['Prediction'] = np.where(y_pred == 1, 'DDOS', 'BENIGN')

# ======== Simpan hasil prediksi ========
df.to_csv("monitoring_data_predicted.csv", index=False)

# ======== (Opsional) Tampilkan 5 baris pertama ========
print(df[['Prediction']].head())

# ======== (Opsional) Visualisasi distribusi prediksi ========

sns.countplot(x='Prediction', data=df)
plt.title(f"Distribusi Prediksi Monitoring Data (Threshold {threshold})")
plt.show()