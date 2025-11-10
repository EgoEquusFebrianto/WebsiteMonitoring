import time
import joblib
import psutil
import random
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine, text
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from flask import Flask, request, jsonify
from threading import Thread

# =====================================
# KONFIGURASI DASAR
# =====================================
model_lr_dir = "models/logistic_regression_ddos.joblib"
model_rf_dir = "models/random_forest_ddos.joblib"
scaler_path = "models/scaler_ddos.joblib"
dataset = "monitoring_data.csv"
is_streaming = {"lr": False, "rf": False}
batch_offsets = {
    "lr": 0,
    "rf": 0
}

user = "postgres"
password = "diy3times"
db = "ta_lab"
schema = "machine_learning"
is_streaming = {"lr": False, "rf": False}
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

# =====================================
# INISIALISASI MODEL DAN DATABASE
# =====================================
app = Flask(__name__)

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:5432/{db}")
model_lr = joblib.load(model_lr_dir)
model_rf = joblib.load(model_rf_dir)
scaler = joblib.load(scaler_path)
data_source = pd.read_csv(dataset)
data_source.columns = data_source.columns.str.strip().str.replace(' ', '_')
data_source = data_source.replace([np.inf, -np.inf], np.nan).fillna(0)

# =====================================
# HELPER FUNCTIONS
# =====================================
def get_micro_batch(df, batch_size=100):
    """Generator untuk mengirimkan data per micro-batch."""
    for i in range(0, len(df), batch_size):
        yield df.iloc[i:i+batch_size]

def select_feature_batch(batch_df):
    """Membersihkan batch agar konsisten dengan data training."""
    # Ambil hanya kolom fitur yang digunakan
    batch = batch_df[selected_features].copy()

    # # Tangani nilai inf dan NaN
    # batch = batch.replace([np.inf, -np.inf], np.nan).fillna(0)

    # # Batasi nilai ekstrem agar stabil secara numerik
    # batch = batch.clip(lower=-1e10, upper=1e10)

    return batch

def insert_network_event(batch, preds, probs, model="lr"):
    """Masukkan hasil batch prediksi ke tabel NetworkEvent_lr."""
    batch["label"] = preds
    batch["probability"] = probs
    batch["timestamp"] = datetime.now()
    offset = batch_offsets[model]

    protocol_map = {0: "ICMP", 6: "TCP", 17: "UDP"}

    with engine.begin() as conn:
        records = []
        for _, row in batch.iterrows():
            records.append({
                "timestamp": row["timestamp"],
                "src_ip": row.get("Source_IP", "0.0.0.0"),
                "dst_ip": row.get("Destination_IP", "0.0.0.0"),
                "protocol": protocol_map.get(int(row.get("Protocol", 6)), "TCP"),
                "packet_count": int(row.get("Total_Fwd_Packets", 0) + row.get("Total_Backward_Packets", 0)),
                "byte_count": float(row.get("Flow_Bytes/s", 0)),
                "flow_duration": float(row.get("Flow_Duration", 0)),
                "label": row["label"],
                "probability": float(row["probability"]),
                "stream_offset": offset
            })
        conn.execute(
            text(f"""
                INSERT INTO "{schema}"."NetworkEvent_{model}"
                (timestamp, src_ip, dst_ip, protocol, packet_count, byte_count, flow_duration, label, probability, stream_offset)
                VALUES (:timestamp, :src_ip, :dst_ip, :protocol, :packet_count, :byte_count, :flow_duration, :label, :probability, :stream_offset)
            """),
            records
        )

def insert_attack_summary(batch, model="lr"):
    """Agregasi batch ke tabel AttackSummary_lr."""
    total = len(batch)
    benign = int((batch["label"] == "BENIGN").sum())
    ddos = int((batch["label"] == "DDOS").sum())
    ddos_ratio = round(ddos / total * 100, 2)
    offset = batch_offsets[model]

    with engine.begin() as conn:
        conn.execute(text(f"""
            INSERT INTO "{schema}"."AttackSummary_{model}"
            (date, total_flows, benign_count, ddos_count, ddos_ratio, stream_offset)
            VALUES (:date, :total_flows, :benign_count, :ddos_count, :ddos_ratio, :stream_offset)
        """), {
            "date": datetime.now(),
            "total_flows": total,
            "benign_count": benign,
            "ddos_count": ddos,
            "ddos_ratio": ddos_ratio,
            "stream_offset": offset
        })
    batch_offsets[model] += 1

# def insert_system_performance(batch, preds):
#     """Hitung performa model (dummy, karena tanpa label asli)."""
#     true_labels = np.random.choice(["BENIGN", "DDOS"], size=len(batch))
#     acc = accuracy_score(true_labels, preds)
#     prec = precision_score(true_labels, preds, pos_label="DDOS")
#     rec = recall_score(true_labels, preds, pos_label="DDOS")
#     f1 = f1_score(true_labels, preds, pos_label="DDOS")

#     latency = random.uniform(50, 150)
#     cpu = psutil.cpu_percent()
#     mem = psutil.virtual_memory().percent

#     with engine.begin() as conn:
#         conn.execute(text(f"""
#             INSERT INTO "{schema}"."SystemPerformance_lr"
#             (accuracy, precision, recall, f1_score, latency_ms, cpu_usage, memory_usage)
#             VALUES (:accuracy, :precision, :recall, :f1_score, :latency_ms, :cpu_usage, :memory_usage)
#         """), {
#             "accuracy": acc,
#             "precision": prec,
#             "recall": rec,
#             "f1_score": f1,
#             "latency_ms": latency,
#             "cpu_usage": cpu,
#             "memory_usage": mem
#         })

# =====================================
# STREAMING FUNCTION
# =====================================
def start_streaming_microbatch_lr(interval=3, batch_size=100):
    global is_streaming

    while is_streaming["lr"]:
        """Simulasi streaming micro-batch ke DB."""
        print("Memulai streaming micro-batch...")
        for batch in get_micro_batch(data_source, batch_size=batch_size):
            if not is_streaming["lr"]:
                print("🛑 Streaming Logistic Regression dihentikan (mid-loop).")
                return
            
            used_batch = select_feature_batch(batch)
            X_scaled = scaler.transform(used_batch)

            # lakukan prediksi
            preds = model_lr.predict(X_scaled)
            probs = model_lr.predict_proba(X_scaled)[:, 1]

            # konversi hasil probabilitas ke label string
            label_str = np.where(preds == 1, "DDOS", "BENIGN")

            # tulis hasil ke database
            insert_network_event(batch.copy(), label_str, probs)
            insert_attack_summary(pd.DataFrame({"label": label_str}))
            # insert_system_performance(batch.copy(), label_str)

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Batch {len(batch)} rows terkirim ✅")
            time.sleep(interval)
    print("🛑 Streaming Logistic Regression dihentikan.")

def start_streaming_microbatch_rf(interval=3, batch_size=100):
    global is_streaming

    while is_streaming["rf"]:
        """Simulasi streaming micro-batch dengan Random Forest."""
        print("Memulai streaming micro-batch dengan Random Forest...")
        for batch in get_micro_batch(data_source, batch_size=batch_size):
            if not is_streaming["rf"]:
                print("🛑 Streaming Random Forest dihentikan (mid-loop).")
                return
            
            # Ambil fitur yang sesuai
            used_batch = select_feature_batch(batch)
            X_used = used_batch 

            # Prediksi
            preds = model_rf.predict(X_used)
            probs = model_rf.predict_proba(X_used)[:, 1]

            # Label string
            label_str = np.where(preds == 1, "DDOS", "BENIGN")

            # Tulis hasil ke database
            insert_network_event(batch.copy(), label_str, probs, model="rf")
            insert_attack_summary(pd.DataFrame({"label": label_str}), model="rf")

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Batch {len(batch)} rows terkirim ✅ (RF)")
            time.sleep(interval)
    print("🛑 Streaming Random Forest dihentikan.")

# =====================================
# FLASK ENDPOINT
# =====================================

@app.route("/start", methods=["GET"])
def start_stream():
    """Memulai proses streaming berdasarkan model yang dipilih."""
    model_type = request.args.get("model", "").lower()

    if model_type not in is_streaming:
        return jsonify({"error": "Model tidak valid. Gunakan 'lr' atau 'rf'."}), 400

    if is_streaming[model_type]:
        return jsonify({"message": f"⚠️ Model {model_type.upper()} sudah berjalan."}), 409
    
    is_streaming[model_type] = True

    if model_type == "lr":
        batch_offsets["lr"] = 0
        Thread(target=start_streaming_microbatch_lr).start()
    elif model_type == "rf":
        batch_offsets["rf"] = 0
        Thread(target=start_streaming_microbatch_rf).start()

    return jsonify({"message": f"✅ Streaming model {model_type.upper()} dimulai."}), 200


@app.route("/stop", methods=["GET"])
def stop_stream():
    model_type = request.args.get("model", "").lower()

    if model_type not in is_streaming:
        return jsonify({"error": "Model tidak valid. Gunakan 'lr' atau 'rf'."}), 400

    if not is_streaming[model_type]:
        return jsonify({"message": f"⚠️ Model {model_type.upper()} tidak sedang berjalan."}), 409

    # ubah flag menjadi False
    is_streaming[model_type] = False

    return jsonify({"message": f"🛑 Streaming model {model_type.upper()} dihentikan."}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)
