
"""
    Tạo file user_expanded.csv
"""
import pandas as pd

# Tạo DataFrame chỉ có cột user_id
df = pd.DataFrame({'user_id': range(1, 1001)})

# Xuất ra file CSV
df.to_csv('user_expanded.csv', index=False, encoding='utf-8')

print(" File 'user_expanded.csv' đã được tạo thành công!")

"""
    Tạo file purchases_expanded.csv
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Đặt seed để tái lập kết quả ngẫu nhiên
np.random.seed(42)

# Số lượng người dùng và sản phẩm
n_users = 1000
n_products = 500  # bạn có thể đổi nếu biết chính xác số lượng sản phẩm
n_records = 5000  # tổng số dòng mua hàng

# Sinh ngẫu nhiên user_id và product_id
user_ids = np.random.randint(1, n_users + 1, size=n_records)
product_ids = [f"id_{i:08d}" for i in np.random.randint(1, n_products + 1, size=n_records)]

# Sinh ngẫu nhiên timestamp trong khoảng 2023–2025
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
random_seconds = np.random.randint(0, int((end_date - start_date).total_seconds()), size=n_records)
timestamps = [start_date + timedelta(seconds=int(s)) for s in random_seconds]

# Tạo DataFrame
df = pd.DataFrame({
    'user_id': user_ids,
    'product_id': product_ids,
    'timestamp': [t.strftime("%Y-%m-%d %H:%M:%S") for t in timestamps]
})

# Xuất ra file CSV
df.to_csv('purchases_expanded.csv', index=False, encoding='utf-8')

print("File 'purchases_expanded.csv' đã được tạo thành công!")
print(df.head())
"""
    Tạo một file product_images_expanded.csv
"""
import os
import pandas as pd

# Các thư mục gốc cần quét
root_dirs = [
    r"F:\Python\Project Code\img\img\CLOTHING",
    r"F:\Python\Project Code\img\MEN",
    r"F:\Python\Project Code\img\WOMEN"
]

records = []

for root_dir in root_dirs:
    if not os.path.exists(root_dir):
        print(f"Root folder không tồn tại, bỏ qua: {root_dir}")
        continue
    # CHỈ DÙNG os.walk LÀ ĐỦ
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                product_id = os.path.basename(dirpath)
                image_path = os.path.join(dirpath, fname)
                records.append((product_id.strip(), image_path))
#Mục đích: thu thập tất cả file ảnh trong root_dirs và ánh xạ product_id → image_path.
#Cách hoạt động:
#- Trước tiên kiểm tra root_dir có tồn tại không; nếu không thì bỏ qua và in cảnh báo.
#- Dùng os.walk(root_dir) để đệ quy, duyệt mọi thư mục con và file.
#- Với mỗi file ảnh (dựa vào extension), lấy product_id bằng basename(dirpath) — tức tên thư mục chứa file — và lưu cặp (product_id, image_path).

#Cách giải thích ngắn khi thầy hỏi: dùng os.listdir nhiều cấp, dễ nổ khi thư mục không tồn tại 
# hoặc cấu trúc thư mục khác. os.walk linh hoạt và an toàn hơn cho cấu trúc không đồng nhất.

# 🔹 Tạo DataFrame chỉ có 2 cột ID sản phầm và đường đến dẫn file ảnh
df = pd.DataFrame(records, columns=["product_id", "image_path"])

# Xuất ra CSV
output_path = "product_images_expanded.csv"
df.to_csv(output_path, index=False, encoding="utf-8")
# Lưu dữ liệu ra file để sử dụng sau này

print(f"File '{output_path}' đã được tạo thành công ({len(df)} ảnh).")
print(df.head()) 

#==> Tạo một bảng (CSV) ánh xạ product_id → image_path để dùng cho các bước sau: 
# nối (join) với thông tin sản phẩm, huấn luyện retrieval/model, hoặc hiển thị ảnh trong app.

"""
    Hàm tạo một file browsing_history_expanded.csv => các sản phẩm user đã từng xem qua
    Mô phỏng lịch sử người dùng xem sản phẩm (view events). Dùng để phân tích hành vi, 
#xây funnel (view → add-to-cart → purchase), huấn luyện recommender systems.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Đặt seed để tái lập kết quả
np.random.seed(42)
# Mục đích: Đảm bảo mỗi lần chạy code sẽ cho KẾT QUẢ GIỐNG NHAU 

# Thông số
n_users = 1000        # số lượng user
n_products = 500      # số lượng sản phẩm
n_records = 10000     # tổng số lượt xem

# Sinh user_id / product_id ngẫu nhiên từ 1-1000/ 10000
user_ids = np.random.randint(1, n_users + 1, size=n_records)
product_ids = [f"id_{i:08d}" for i in np.random.randint(1, n_products + 1, size=n_records)]

# Sinh timestamp ngẫu nhiên trong khoảng 2023–2025
start_date =datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
total_sec = int((end_date - start_date).total_seconds())
random_seconds = np.random.randint(0, total_sec + 1, size=n_records)
timestamps = [start_date + timedelta(seconds=int(s)) for s in random_seconds]


# Tạo DataFrame
df = pd.DataFrame({ # Tạo dictionary với 3 key-value pairs, mỗi value là một list


    'user_id': user_ids,
    'product_id': product_ids,
    'timestamp': [t.strftime("%Y-%m-%d %H:%M:%S") for t in timestamps] # Chuyển đổi datetime object thành string theo định dạng
})

# Xuất ra file CSV
df.to_csv('browsing_history_expanded.csv', index=False, encoding='utf-8')

print("File 'browsing_history_expanded.csv' đã được tạo thành công!")
print(df.head())


#===================================================================
"""
    *************Tạo một file products_expanded.csv
    Chuyển JSON mô tả sản phẩm thành table có product_id, description,
    cộng thêm một số thuộc tính giả lập (category, price, rating, product_name) 
    để dùng cho testing, demo, hoặc training.
"""
import pandas as pd
import numpy as np
import json
import os
import re

# ===== 1. Đọc file JSON =====
json_path = "./list_description_inshop.json"
if not os.path.exists(json_path):
    raise FileNotFoundError(f"Không tìm thấy file JSON: {json_path}")
# Bảo đảm file tồn tại, nếu không sẽ dừng script sớm với lỗi rõ ràng.

# ===== 1. Đọc file JSON ============================
try:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Không tìm thấy file JSON: {json_path}")
except json.JSONDecodeError as e:
    raise ValueError(f"JSON bị lỗi cấu trúc: {e}")
#Mục đích: bắt lỗi phổ biến khi đọc JSON:
#- file không tồn tại → báo rõ và dừng,
#- file tồn tại nhưng JSON corrupt/invalid → báo lỗi cấu trúc (có thông tin exception).

#json.JSONDecodeError giúp trả lỗi có thông tin (ví dụ dòng/cột bị sai) để dễ s

# Chuyển JSON thành DataFrame
records = []
for item in data:
    product_id = item.get("item")
    product_id = str(product_id).strip()  # chuẩn hoá   
    desc = item.get("description", "")
    if isinstance(desc, list):
        description = " ".join([str(x).strip() for x in desc if str(x).strip()])
    elif isinstance(desc, dict):
        description = " ".join([str(v).strip() for v in desc.values() if str(v).strip()])
    else:
        description = str(desc).strip()
    records.append({"product_id": product_id, "description": description})

#Mục đích: đảm bảo description luôn là chuỗi text hợp lệ, bất kể input là list, dict hay string.
#- Nếu là list: join các phần tử (thường là dòng mô tả) bằng khoảng trắng.
#- Nếu dict: join các giá trị — hữu ích nếu JSON lưu description dưới dạng object (ví dụ {"short": "...", "long": "..."}).
#- Nếu rỗng hoặc None → trở thành ""

#==> Em làm chức năng ‘normalize’ để mọi description đều là string chuẩn, 
# giúp downstream processing (category detect, tag extract) hoạt động ổn định.”

df = pd.DataFrame(records)

# ===== 2. Đọc file attribute (list_attr_cloth.txt) =====
attr_path = "./list_attr_cloth.txt"
if not os.path.exists(attr_path):
    raise FileNotFoundError(f" Không tìm thấy file: {attr_path}")

# Đọc từng dòng (bỏ dòng trống, bỏ xuống dòng)
# ===== 2. Đọc file attribute (list_attr_cloth.txt) =====
try:
    with open(attr_path, "r", encoding="utf-8") as f:
        attributes = [line.strip().lower() for line in f if line.strip()]
except FileNotFoundError:
    raise FileNotFoundError(f" Không tìm thấy file thuộc tính: {attr_path}")
except UnicodeDecodeError:
    raise UnicodeError(f" Lỗi encoding khi đọc file thuộc tính: {attr_path}")
# kiểm tra file attributes để tránh lỗi encoding và để pipeline biết rõ nguyên nhân nếu file không đọc được.”
  
    ## Đọc file chứa các thuộc tính quần áo để phân loại.
    #==> Mỗi dòng file list_attr_cloth.txt được strip và lower. 
    # Dùng để sau này match tags/thuộc tính (ví dụ color, material).

#loại bỏ dòng trống
# Thầy có thể hỏi: "attributes dùng để làm gì?" 
#  trả lời: có thể dùng để tìm màu, chất liệu trong description bằng cách
#  dò từng attribute trong text (với regex \b{attr}\b) rồi lưu as tags.

print(f"Đã đọc {len(attributes)} dòng thuộc tính từ list_attr_cloth.txt")

# ===== 3. Danh sách category chính ==========================================
# (có thể mở rộng thêm các loại lấy từ attributes nếu muốn)
main_categories = [
    "dress", "blouse", "jacket", "skirt", "top", "tee", "jeans",
    "sweater", "pants", "shorts", "cardigan", "coat", "hoodie",
    "romper", "leggings", "vest", "jumpsuit", "shirt", "polo", "tank"
]

# =================== 4. Xác định category dựa vào description ===========================
def detect_category(text):
    text = text.lower()
    for cat in main_categories:
        if re.search(rf"\b{cat}\b", text):
            return cat.capitalize()
    return "Other"

df["category"] = df["description"].apply(detect_category)

# ===== 5. Sinh dữ liệu giả cho price, rating, product_name =====
np.random.seed(42)

df["price"] = np.round(np.random.uniform(5, 120, len(df)), 2)
df["rating"] = np.round(np.random.uniform(1.0, 5.0, len(df)), 1)

prefixes = ["Elegant", "Modern", "Classic", "Casual", "Trendy", "Vintage", "Sporty"]
items = ["Top", "Blouse", "Jacket", "Skirt", "Dress", "Tee", "Jeans", "Sweater"]

df["product_name"] = [
    f"{np.random.choice(prefixes)} {np.random.choice(items)}"
    for _ in range(len(df))
]

# ===== 6. Xuất ra file CSV =====
output_path = "products_expanded.csv"  
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\n Đã tạo file '{output_path}' thành công ({len(df)} dòng)!")
print(df.head(10))

# "Tại sao dùng index=False?"
# "Để tránh tạo cột index thừa trong file CSV, giữ dữ liệu sạch sẽ và tiết kiệm dung lượng."

#"utf-8-sig khác utf-8 thế nào?"
#→ "utf-8-sig thêm BOM giúp Excel tự động nhận diện encoding, trong khi utf-8 thông thường có thể làm Excel hiển thị tiếng Việt sai."

# "Tại sao in head(10) thay vì toàn bộ DataFrame?"
#→ "Để kiểm tra nhanh kết quả mà không làm tràn console với quá nhiều dữ liệu."

# "Có cách nào khác để xuất DataFrame không?"
#→ "Có ạ, ngoài CSV còn có thể xuất Excel (.xlsx) với to_excel(), JSON với to_json(), hoặc SQL database trực tiếp."




#  ====================TÓM TẮT QUY TRÌNH TỔNG THỂ===========
# Khởi tạo → Thiết lập seed và tham số
#Đọc dữ liệu gốc → JSON, file text, duyệt thư mục ảnh
#Tiền xử lý → Chuyển đổi định dạng, làm sạch dữ liệu
#Sinh dữ liệu giả → Random values cho các trường còn thiếu
#Tạo cấu trúc → Chuyển thành DataFrame có cấu trúc
#Xuất file → Ghi ra CSV với encoding phù hợp