
"""
    Tạo file user_expanded.csv
"""
import csv          # Thư viện làm việc với file CSV (đọc / ghi)
import random       # Thư viện tạo số/ngẫu nhiên
import string       # Thư viện chứa các hằng về chữ cái, chữ số, v.v.

# Hàm tạo username ngẫu nhiên
def generate_username():
    # Danh sách tên (first name)
    first_names = ['john', 'jane', 'alex', 'mike', 'sara', 'emma', 'david', 'lisa', 'chris', 'amy', 
                  'ryan', 'katie', 'tom', 'olivia', 'daniel', 'sophia', 'james', 'mia', 'robert', 'linda',
                  'william', 'elizabeth', 'matthew', 'jennifer', 'andrew', 'michelle', 'joshua', 'amanda',
                  'christopher', 'melissa', 'kevin', 'stephanie', 'brian', 'rebecca', 'justin', 'laura',
                  'eric', 'heather', 'jason', 'nicole', 'jeffrey', 'emily', 'steven', 'rachel', 'timothy',
                  'samantha', 'patrick', 'hannah', 'richard', 'victoria']
    
    # Danh sách họ (last name)
    last_names = ['smith', 'johnson', 'williams', 'brown', 'jones', 'garcia', 'miller', 'davis', 'rodriguez',
                 'martinez', 'hernandez', 'lopez', 'gonzalez', 'wilson', 'anderson', 'thomas', 'taylor',
                 'moore', 'jackson', 'martin', 'lee', 'perez', 'thompson', 'white', 'harris', 'sanchez',
                 'clark', 'ramirez', 'lewis', 'robinson', 'walker', 'young', 'allen', 'king', 'wright',
                 'scott', 'torres', 'nguyen', 'hill', 'flores', 'green', 'adams', 'nelson', 'baker', 'hall',
                 'rivera', 'campbell', 'mitchell', 'carter', 'roberts']
    
    # random.choice(...) chọn ngẫu nhiên 1 phần tử trong list
    # random.randint(10, 999) tạo số ngẫu nhiên từ 10 đến 999
    # Username dạng: first_last_XXX  (vd: john_smith_527)
    return f"{random.choice(first_names)}_{random.choice(last_names)}_{random.randint(10, 999)}"

# Hàm tạo password ngẫu nhiên
def generate_password(length=10):
    # Tập ký tự dùng để tạo password: chữ cái + số + ký tự đặc biệt
    characters = string.ascii_letters + string.digits + "!@#$%&*"
    # Ghép ngẫu nhiên 'length' ký tự lại thành 1 chuỗi password
    return ''.join(random.choice(characters) for _ in range(length))

# Hàm tạo email dựa trên username
def generate_email(username):
    # Danh sách domain email có thể dùng
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 
               'protonmail.com', 'aol.com', 'zoho.com', 'mail.com', 'yandex.com']
    # username dạng: first_last_số → tách bằng dấu "_"
    # username.split('_')[0] = first name, [1] = last name
    # Email dạng: first.last@domain  (vd: john.smith@gmail.com)
    return f"{username.split('_')[0]}.{username.split('_')[1]}@{random.choice(domains)}".lower()

# ====== Generate data cho 1000 users ======
users_data = []   # List để lưu dict thông tin từng user

for user_id in range(1, 1001):  # user_id từ 1 đến 1000
    username = generate_username()      # tạo username ngẫu nhiên
    password = generate_password()      # tạo password ngẫu nhiên
    email = generate_email(username)    # tạo email từ username
    
    # Thêm 1 user (kiểu dict) vào list users_data
    users_data.append({
        'user_id': user_id,
        'username': username,
        'password': password,
        'email': email
    })

# ====== Ghi dữ liệu ra file CSV ======
filename = 'users_expanded.csv'
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    # Định nghĩa tên các cột trong file CSV
    fieldnames = ['user_id', 'username', 'password', 'email']
    # Tạo đối tượng writer dạng DictWriter (ghi từng dòng là 1 dict)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()           # ghi dòng header (tên cột)
    for user in users_data:
        writer.writerow(user)      # ghi từng user (dict) thành 1 dòng trong CSV

print(f" File '{filename}' đã được tạo thành công!")

# ====== In thử 5 dòng đầu để preview trên console ======
print("\n Preview (5 users đầu tiên):")
print("user_id,username,password,email")
for i in range(5):
    user = users_data[i]
    # In dạng CSV: user_id,username,password,email
    print(f"{user['user_id']},{user['username']},{user['password']},{user['email']}")
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
    r"F:\Python\Project Code\img\CLOTHING",
    r"F:\Python\Project Code\img\MEN",
    r"F:\Python\Project Code\img\WOMEN",
    r"F:\Python\Project Code\img\DRESSES",
    r"F:\Python\Project Code\img\TOPS",
    r"F:\Python\Project Code\img\TROUSERS"
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
#Phần này quét toàn bộ thư mục ảnh sản phẩm để thu thập đường dẫn"
#Mỗi dòng đại diện cho 1 ảnh sản phẩm, giúp hệ thống biết sản phẩm nào có ảnh nào"
#Dùng để training model computer vision hoặc hiển thị ảnh trong app"
#Câu hỏi phản biện có thể gặp:
#Tại sao cần file này?" → Để kết nối dữ liệu sản phẩm với ảnh, phục vụ visual recommendation
#Nếu 1 sản phẩm có nhiều ảnh thì sao?" → Mỗi ảnh là 1 dòng, cùng product_id


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
# → Tạo thời gian ngẫu nhiên bằng cách cộng số giây ngẫu nhiên vào ngày bắt đầu

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
Tạo file products_expanded.csv từ:

- list_description_inshop.json  (mô tả + màu sắc)
- product_images_expanded.csv   (chứa đường dẫn ảnh)

Kết quả: các cột
- product_id
- description  (lấy từ JSON)
- color        (lấy từ JSON nếu có)
- category     (lấy từ thư mục ngay trước folder id_... trong đường dẫn ảnh)
- price        (random)
- rating       (random nhưng thiên về cao: 3.5–5.0)
- product_name = "<color> <category_clean>"
"""

import pandas as pd
import numpy as np
import json
import os
import re

# =========================================================
# 1. Đọc file JSON mô tả sản phẩm
# =========================================================
json_path = "./list_description_inshop.json"
if not os.path.exists(json_path):
    raise FileNotFoundError(f"Không tìm thấy file JSON: {json_path}")

try:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError(f"JSON bị lỗi cấu trúc: {e}")

records = []
for item in data:
    # id sản phẩm
    product_id = str(item.get("item")).strip()

    # ----- description (GIỮ NGUYÊN) -----
    desc = item.get("description", "")
    if isinstance(desc, list):
        description = " ".join(str(x).strip() for x in desc if str(x).strip())
    #chuẩn hóa description từ nhiều định dạng (list, dict, string) thành string thuần
    #Dữ liệu JSON có thể không đồng nhất, nên cần chuẩn hóa để xử lý sau này"
    elif isinstance(desc, dict):
        description = " ".join(str(v).strip() for v in desc.values() if str(v).strip())
    else:
        description = str(desc).strip()

    # màu sắc nếu có
    color = str(item.get("color", "") or "").strip()

    records.append({
        "product_id": product_id,
        "description": description,  # <-- cột description ở đây
        "color": color
    })

df = pd.DataFrame(records)
print(f"Đã đọc {len(df)} sản phẩm từ JSON.")

# =========================================================
# 2. Đọc file link ảnh để suy ra category từ path
# =========================================================
img_csv_path = "./product_images_expanded.csv"
if not os.path.exists(img_csv_path):
    raise FileNotFoundError(f"Không tìm thấy file ảnh: {img_csv_path}")

img_df = pd.read_csv(img_csv_path)

def extract_category_from_path(path: str) -> str:
    #"Dựa vào cấu trúc thư mục để tự động phân loại sản phẩm 
    # - thư mục cha của folder product_id chính là category
    """
    Lấy tên thư mục ngay trước folder id_... trong đường dẫn ảnh.

    Ví dụ:
    F:\\Python\\Project Code\\img\\WOMEN\\Blouses_Shirts\\id_00000001\\1.jpg
    --> parts = [..., 'WOMEN', 'Blouses_Shirts', 'id_00000001', '1.jpg']
    --> category = parts[-3] = 'Blouses_Shirts'
    """
    if not isinstance(path, str) or not path:
        return "Other"
    parts = re.split(r"[\\/]", path)
    if len(parts) >= 3:
        return parts[-3]
    #chọn parts[-3] mà không phải parts[-2] hay parts[-4]?"
    # Vì parts[-2] là folder product_id (id_00000001), parts[-4] là gender (WOMEN/MEN).
    # parts[-3] chính là category thực tế (Dresses, Shirts, etc.)"
    return "Other"

# Q: "Có sản phẩm nào bị mất category không?"
# => Có, những sản phẩm có đường dẫn ngắn (ít hơn 3 parts) 
# sẽ được gán "Other", đây là cách xử lý an toàn cho edge cases"
img_df["path_category"] = img_df["image_path"].apply(extract_category_from_path)

# Mỗi product_id giữ 1 dòng đại diện để merge
img_single = (
    img_df.sort_values("image_path")
          .drop_duplicates(subset="product_id", keep="first")
          [["product_id", "path_category"]]
)

# =========================================================
# 3. Gộp category vào df chính
# =========================================================
df = df.merge(img_single, on="product_id", how="left")
# Kết hợp thông tin từ JSON và đường dẫn ảnh
# Dùng left join để giữ lại tất cả sản phẩm từ JSON, kể cả những sản phẩm không có ảnh"
def clean_category(cat: str) -> str:
    if not isinstance(cat, str) or not cat.strip():
        return "Other"
    return cat.strip().replace("_", " ")

df["category"] = df["path_category"].apply(clean_category)

# =========================================================
# 4. Sinh price + rating + product_name
# =========================================================
np.random.seed(42)

# price: giữ range rộng để demo
df["price"] = np.round(np.random.uniform(5, 120, len(df)), 2)

# rating: cho cao hơn, từ 3.5 đến 5.0
df["rating"] = np.round(np.random.uniform(3.5, 5.0, len(df)), 1)

def build_product_name(row):
    color = str(row.get("color", "") or "").strip()
    cat_raw = row.get("path_category", "")
    cat_clean = clean_category(cat_raw)
# Kết hợp màu sắc + category để tên sản phẩm tự nhiên hơn
    base = cat_clean.title() if cat_clean else ""
    if color and base:
        return f"{color} {base}"
    elif base:
        return base
    elif color:
        return f"{color} Item"
    else:
        return "Fashion Item"

df["product_name"] = df.apply(build_product_name, axis=1)

# =========================================================
# 5. Xuất CSV
# =========================================================
output_path = "products_expanded.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\nĐã tạo file '{output_path}' thành công ({len(df)} dòng)!")
print(df.head(10)[["product_id", "description", "color", "category", "price", "rating", "product_name"]])

# CÂU HỎI THƯỜNG GẶP VÀ CÁCH TRẢ LỜI:
#"Tại sao phải tạo nhiều file CSV như vậy?"
# ==>Mỗi file phục vụ một mục đích khác nhau trong hệ thống recommendation, giúp modular hóa và dễ bảo trì"

#làm sao xử lý dữ liệu thật thay vì dữ liệu giả?"
# ==> Khi có dữ liệu thật, chỉ cần thay thế phần sinh dữ liệu giả bằng phần đọc từ database/log files"

#Có cách nào cải thiện việc extract category không?"
# ==>Có thể dùng ML để phân loại tự động từ description hoặc dùng computer vision để phân tích ảnh"
