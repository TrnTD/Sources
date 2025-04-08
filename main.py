
import pandas as pd
import torch

# Tải mô hình đã huấn luyện
model_path = 'C:/Users/Admin/Desktop/An Toàn Mạng Nâng Cao/tabnet_clf_1_two_label.pth'
clf_0 = torch.load(model_path, weights_only=False)  # Sử dụng weights_only=False

# Đọc tệp CSV chứa các đặc trưng đã trích xuất
df_features = pd.read_csv('brute_force2_ISCX.csv')
selected_columns = [
   'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Std', 'Flow IAT Mean', 'Flow IAT Std', 'Fwd IAT Total', 'Fwd IAT Std', 'Bwd IAT Mean', 'Bwd IAT Min', 'Bwd URG Flags', 'Packet Length Min', 'Packet Length Max', 'Packet Length Std', 'URG Flag Count', 'Fwd Avg Packets/Bulk', 'Init Bwd Win Bytes', 'Idle Mean', 'Idle Max'

]
print(len(selected_columns))
# Trích xuất các đặc trưng từ DataFrame
df_selected_features = df_features[selected_columns]

# Kiểm tra lại dữ liệu sau khi trích xuất
print(df_selected_features)

# Chuyển các đặc trưng thành NumPy array
X_new = df_selected_features.values  # Chuyển đổi DataFrame thành mảng NumPy

# Dự đoán nhãn với mô hình
predictions = clf_0.predict(X_new)  # Dự đoán nhãn

# Ánh xạ nhãn số thành tên nhãn
label_mapping = {
    0: 'Benign',
    1: 'Malicious'
}

# Chuyển đổi nhãn dự đoán thành tên nhãn
predicted_labels = [label_mapping[pred] for pred in predictions]

# Hiển thị kết quả dự đoán
print(predicted_labels)

