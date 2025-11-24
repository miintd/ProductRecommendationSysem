"""
    Tạo file user_expanded.csv
"""
import csv         
import random      
import string     

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
    
    return f"{random.choice(first_names)}_{random.choice(last_names)}_{random.randint(10, 999)}"

# Hàm tạo password ngẫu nhiên
def generate_password(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Hàm tạo email dựa trên username
def generate_email(username):
    # Danh sách domain email có thể dùng
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 
               'protonmail.com', 'aol.com', 'zoho.com', 'mail.com', 'yandex.com']
    return f"{username.split('_')[0]}.{username.split('_')[1]}@{random.choice(domains)}".lower()

# ====== Generate data cho 1000 users ======
users_data = []

for user_id in range(1, 1001):  
    username = generate_username()      
    password = generate_password()      
    email = generate_email(username)    
    
    users_data.append({
        'user_id': user_id,
        'username': username,
        'password': password,
        'email': email
    })

# ====== Ghi dữ liệu ra file CSV ======
filename = 'users_expanded.csv'
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['user_id', 'username', 'password', 'email']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()           
    for user in users_data:
        writer.writerow(user)      

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

np.random.seed(42)

# Số lượng người dùng và sản phẩm
n_users = 1000
n_products = 500  
n_records = 5000  

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
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                product_id = os.path.basename(dirpath)
                image_path = os.path.join(dirpath, fname)
                records.append((product_id.strip(), image_path))
#Mục đích: thu thập tất cả file ảnh trong root_dirs và ánh xạ product_id → image_path.

df = pd.DataFrame(records, columns=["product_id", "image_path"])

output_path = "product_images_expanded.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"File '{output_path}' đã được tạo thành công ({len(df)} ảnh).")
print(df.head()) 

"""
    Hàm tạo một file browsing_history_expanded.csv 
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n_users = 1000       
n_products = 500     
n_records = 10000   

# Sinh user_id / product_id ngẫu nhiên từ 1-1000/ 10000
user_ids = np.random.randint(1, n_users + 1, size=n_records)
product_ids = [f"id_{i:08d}" for i in np.random.randint(1, n_products + 1, size=n_records)]

# Sinh timestamp ngẫu nhiên trong khoảng 2023–2025
start_date =datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
total_sec = int((end_date - start_date).total_seconds())
random_seconds = np.random.randint(0, total_sec + 1, size=n_records)
timestamps = [start_date + timedelta(seconds=int(s)) for s in random_seconds]

df = pd.DataFrame({ # Tạo dictionary với 3 key-value pairs, mỗi value là một list
    'user_id': user_ids,
    'product_id': product_ids,
    'timestamp': [t.strftime("%Y-%m-%d %H:%M:%S") for t in timestamps] # Chuyển đổi datetime object thành string theo định dạng
})
df.to_csv('browsing_history_expanded.csv', index=False, encoding='utf-8')

print("File 'browsing_history_expanded.csv' đã được tạo thành công!")
print(df.head())

#===================================================================
"""
Tạo file products_expanded.csv từ:
"""

import pandas as pd
import numpy as np
import json
import os
import re

# 1. Đọc file JSON mô tả sản phẩm

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

    desc = item.get("description", "")
    if isinstance(desc, list):
        description = " ".join(str(x).strip() for x in desc if str(x).strip())
    elif isinstance(desc, dict):
        description = " ".join(str(v).strip() for v in desc.values() if str(v).strip())
    else:
        description = str(desc).strip()
    color = str(item.get("color", "") or "").strip()

    records.append({
        "product_id": product_id,
        "description": description,  
        "color": color
    })

df = pd.DataFrame(records)
print(f"Đã đọc {len(df)} sản phẩm từ JSON.")

# =========================================================
# 2. Đọc file link ảnh để suy ra category từ path

img_csv_path = "./product_images_expanded.csv"
if not os.path.exists(img_csv_path):
    raise FileNotFoundError(f"Không tìm thấy file ảnh: {img_csv_path}")

img_df = pd.read_csv(img_csv_path)

def extract_category_from_path(path: str) -> str:
    """
    Lấy tên thư mục ngay trước folder id_... trong đường dẫn ảnh.
    """
    if not isinstance(path, str) or not path:
        return "Other"
    parts = re.split(r"[\\/]", path)
    if len(parts) >= 3:
        return parts[-3]
    return "Other"

img_df["path_category"] = img_df["image_path"].apply(extract_category_from_path)

img_single = (
    img_df.sort_values("image_path")
          .drop_duplicates(subset="product_id", keep="first")
          [["product_id", "path_category"]]
)

# =========================================================
# 3. Gộp category vào df chính

df = df.merge(img_single, on="product_id", how="left")
def clean_category(cat: str) -> str:
    if not isinstance(cat, str) or not cat.strip():
        return "Other"
    return cat.strip().replace("_", " ")

df["category"] = df["path_category"].apply(clean_category)

# =========================================================
# 4. Sinh price + rating + product_name

np.random.seed(42)

df["price"] = np.round(np.random.uniform(5, 120, len(df)), 2)
df["rating"] = np.round(np.random.uniform(3.5, 5.0, len(df)), 1)

def build_product_name(row):
    color = str(row.get("color", "") or "").strip()
    cat_raw = row.get("path_category", "")
    cat_clean = clean_category(cat_raw)
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

output_path = "products_expanded.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\nĐã tạo file '{output_path}' thành công ({len(df)} dòng)!")
print(df.head(10)[["product_id", "description", "color", "category", "price", "rating", "product_name"]])


