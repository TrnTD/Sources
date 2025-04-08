import pandas as pd
import os

def process_csv(input_path, columns_to_drop=None, columns_to_rename=None):
    try:
        # Tạo đường dẫn output
        dir_name, file_name = os.path.split(input_path)
        base_name, ext = os.path.splitext(file_name)
        output_path = os.path.join(dir_name, f"{base_name}_MOD2{ext}")
        
        # Đọc file CSV
        df = pd.read_csv(input_path)
        
        # Bỏ các cột không cần thiết
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop, errors='ignore')
        
        # Đổi tên các cột
        if columns_to_rename:
            df = df.rename(columns=columns_to_rename)
        
        # Lưu file kết quả
        df.to_csv(output_path, index=False)
        print(f"\nXử lý hoàn tất! File kết quả được lưu tại:\n{output_path}")
        
        return output_path
    
    except Exception as e:
        print(f"\nCó lỗi xảy ra: {str(e)}")
        return None

if __name__ == "__main__":
    # Nhập đường dẫn file input
    input_path = input("Nhập đường dẫn file CSV cần xử lý: ").strip('"').strip()
    
    if not os.path.isfile(input_path):
        print("\nLỗi: File không tồn tại hoặc đường dẫn không đúng!")
    else:
        # Danh sách cột cần xóa
        columns_to_drop = [
            "Flow ID", "Src IP", "Src Port", "Dst IP",
            "Dst Port", "Timestamp"
        ]
        
        # Dictionary đổi tên cột đầy đủ
        columns_to_rename = {
            "Total Fwd Packet": "Total Fwd Packets",
            "Total Bwd packets": "Total Backward Packets",
            "Total Length of Fwd Packet": "Fwd Packets Length Total",
            "Total Length of Bwd Packet": "Bwd Packets Length Total",
            "CWR Flag Count": "CWE Flag Count",
            "Average Packet Size": "Avg Packet Size",
            "Fwd Segment Size Avg": "Avg Fwd Segment Size",
            "Bwd Segment Size Avg": "Avg Bwd Segment Size",
            "Fwd Bytes/Bulk Avg": "Fwd Avg Bytes/Bulk",
            "Fwd Packet/Bulk Avg": "Fwd Avg Packets/Bulk",
            "Fwd Bulk Rate Avg": "Fwd Avg Bulk Rate",
            "Bwd Bytes/Bulk Avg": "Bwd Avg Bytes/Bulk",
            "Bwd Packet/Bulk Avg": "Bwd Avg Packets/Bulk",
            "Bwd Bulk Rate Avg": "Bwd Avg Bulk Rate",
            "FWD Init Win Bytes": "Init Fwd Win Bytes",
            "Bwd Init Win Bytes": "Init Bwd Win Bytes",
            "Fwd Act Data Pkts": "Fwd Act Data Packets"
        }
        
        # Thực hiện xử lý
        process_csv(input_path,
                   columns_to_drop=columns_to_drop,
                   columns_to_rename=columns_to_rename)
