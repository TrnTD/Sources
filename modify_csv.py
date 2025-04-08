import pandas as pd
import os

def process_csv(input_path, columns_to_drop=None, columns_to_rename=None):
    try:
        # Tạo đường dẫn output
        dir_name, file_name = os.path.split(input_path)
        base_name, ext = os.path.splitext(file_name)
        output_path = os.path.join(dir_name, f"{base_name}_MOD{ext}")
        
        # Đọc file CSV
        df = pd.read_csv(input_path)
        
        # Bỏ các cột không cần thiết
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop, errors='ignore')
        
        # Đổi tên các cột
        if columns_to_rename:
            df = df.rename(columns=columns_to_rename)
        
        # Xử lý duplicate cột Fwd Header Length
        if 'Fwd Header Length' in df.columns:
            # Tạo bản sao cột
            duplicated_col = df['Fwd Header Length'].copy()
            
            # Tìm vị trí chèn (sau 'Avg Bwd Segment Size')
            target_col = 'Avg Bwd Segment Size'
            if target_col in df.columns:
                insert_pos = df.columns.get_loc(target_col) + 1
                
                # Tạm thời đổi tên cột gốc để tránh trùng lặp
                df.rename(columns={'Fwd Header Length': 'Fwd_Header_Length_TEMP'}, inplace=True)
                
                # Chèn bản sao với tên gốc
                df.insert(insert_pos, 'Fwd Header Length', duplicated_col)
                
                # Đổi lại tên cột gốc
                df.rename(columns={'Fwd_Header_Length_TEMP': 'Fwd Header Length'}, inplace=True)
                
                print(f"Đã nhân bản cột 'Fwd Header Length' và chèn sau cột '{target_col}'")
            else:
                print(f"Không tìm thấy cột '{target_col}' để chèn cột nhân bản")
        
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
            "Protocol", "Timestamp"
        ]
        
        # Dictionary đổi tên cột đầy đủ
        columns_to_rename = {
            "Dst Port": "Destination Port",
            "Total Fwd Packet": "Total Fwd Packets",
            "Total Bwd packets": "Total Backward Packets",
            "Total Length of Fwd Packet": "Total Length of Fwd Packets",
            "Total Length of Bwd Packet": "Total Length of Bwd Packets",
            "Packet Length Min": "Min Packet Length",
            "Packet Length Max": "Max Packet Length",
            "CWR Flag Count": "CWE Flag Count",
            "Fwd Segment Size Avg": "Avg Fwd Segment Size",
            "Bwd Segment Size Avg": "Avg Bwd Segment Size",
            "Fwd Bytes/Bulk Avg": "Fwd Avg Bytes/Bulk",
            "Fwd Packet/Bulk Avg": "Fwd Avg Packets/Bulk",
            "Fwd Bulk Rate Avg": "Fwd Avg Bulk Rate",
            "Bwd Bytes/Bulk Avg": "Bwd Avg Bytes/Bulk",
            "Bwd Packet/Bulk Avg": "Bwd Avg Packets/Bulk",
            "Bwd Bulk Rate Avg": "Bwd Avg Bulk Rate",
            "FWD Init Win Bytes": "Init_Win_bytes_forward",
            "Bwd Init Win Bytes": "Init_Win_bytes_backward",
            "Fwd Act Data Pkts": "act_data_pkt_fwd",
            "Fwd Seg Size Min": "min_seg_size_forward"
        }
        
        # Thực hiện xử lý
        process_csv(input_path,
                   columns_to_drop=columns_to_drop,
                   columns_to_rename=columns_to_rename)
