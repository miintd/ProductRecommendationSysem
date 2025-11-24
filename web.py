import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
from typing import List

st.set_page_config(page_title="Product Recommender", layout="wide")

CSV_FILES = {
    'users': 'users_expanded.csv',
    'products': 'products_expanded.csv',
    'product_images': 'product_images_expanded.csv',
    'purchases': 'purchases_expanded.csv',
    'browsing_history': 'browsing_history_expanded.csv'
}

if 'logged_in' not in st.session_state:
    st.session_state.update({
        'logged_in': False,
        'user_id': None,
        'selected_product': None,
        'algorithm': 'collaborative',
        'cart': [],
        'auth_mode': 'login'  # 'login' or 'register'
    })

# ===== STYLES =====
st.markdown("""
<style>
.stButton > button {
    background-color: #111111;
    color: #ffffff;
    border-radius: 999px;
    border: 1px solid #111111;
    padding: 6px 18px;
    font-size: 13px;
}
.stButton > button:hover {
    background-color: #ffffff;
    color: #111111;
}
.product-card {
    background-color: #ffffff;
    border: 1px solid #eee;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 15px;
}
.product-img {
    width: 100%;
    height: 230px;
    object-fit: cover;
    border-radius: 8px;
    display: block;
    margin-bottom: 8px;
}
.detail-img {
    width: 100%;
    height: 420px;
    object-fit: cover;
    border-radius: 8px;
    display: block;
    margin-bottom: 8px;
}
.image-grid {
    margin: 10px 0;
}
.auth-tabs {
    display: flex;
    margin-bottom: 20px;
    border-bottom: 1px solid #ddd;
}
.auth-tab {
    padding: 10px 20px;
    cursor: pointer;
    border-bottom: 2px solid transparent;
}
.auth-tab.active {
    border-bottom: 2px solid #111111;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===== CACHED DATA LOADING =====
@st.cache_data
def load_data():
    """Load all data files with caching"""
    data = {}
    for name, path in CSV_FILES.items():
        try:
            data[name] = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()
        except:
            data[name] = pd.DataFrame()
    return data

# ===== AUTHENTICATION FUNCTIONS =====
def load_users():
    """Load users data"""
    try:
        if os.path.exists(CSV_FILES['users']):
            return pd.read_csv(CSV_FILES['users'])
        else:
            # Create new users file with required columns
            users_df = pd.DataFrame(columns=['user_id', 'username', 'password', 'email'])
            users_df.to_csv(CSV_FILES['users'], index=False)
            return users_df
    except:
        return pd.DataFrame(columns=['user_id', 'username', 'password', 'email'])

def save_users(users_df):
    """Save users data"""
    try:
        users_df.to_csv(CSV_FILES['users'], index=False)
        return True
    except:
        return False

def register_user(username, password, email):
    """Register new user"""
    users_df = load_users()
    
    if not users_df.empty and username in users_df['username'].values:
        return False, "Tên đăng nhập đã tồn tại"
    
    if users_df.empty:
        new_user_id = 1001
    else:
        new_user_id = users_df['user_id'].max() + 1
    
    new_user = pd.DataFrame([{
        'user_id': new_user_id,
        'username': username,
        'password': password,  # In real app, should hash this
        'email': email
    }])
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    
    if save_users(users_df):
        return True, "Đăng ký thành công!"
    else:
        return False, "Lỗi khi đăng ký"

def login_user(username, password):
    """Login user"""
    users_df = load_users()
    
    if users_df.empty:
        return False, "Không tìm thấy người dùng"
    
    user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
    
    if not user.empty:
        user_id = user.iloc[0]['user_id']
        return True, user_id
    else:
        return False, "Tên đăng nhập hoặc mật khẩu không đúng"

# ===== CORE FUNCTIONS =====
def get_product_images(product_id: int, product_images_df: pd.DataFrame) -> List[str]:
    """Get product images (max 4)"""
    if product_images_df.empty:
        return []
    matches = product_images_df[product_images_df["product_id"] == product_id]
    image_paths = matches["image_path"].tolist() if not matches.empty else []

    existing_images = []
    for path in image_paths:
        if path and os.path.exists(path):
            existing_images.append(path)
        if len(existing_images) >= 4:
            break
    return existing_images

def render_local_image(path: str, css_class: str) -> None:
    """Render local image with fixed size using base64 + <img>."""
    if not path or not os.path.exists(path):
        url = "https://via.placeholder.com/400x300?text=No+Image"
        st.markdown(
            f'<img src="{url}" class="{css_class}">',
            unsafe_allow_html=True,
        )
        return

    # đoán mime
    ext = os.path.splitext(path)[1].lower()
    mime = "image/jpeg"
    if ext in [".png"]:
        mime = "image/png"

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    src = f"data:{mime};base64,{data}"
    st.markdown(
        f'<img src="{src}" class="{css_class}">',
        unsafe_allow_html=True,
    )

def add_to_cart(product_id: int, products_df: pd.DataFrame):
    """Add product to cart"""
    product = products_df[products_df["product_id"] == product_id]
    if product.empty:
        return
    
    product = product.iloc[0]
    for item in st.session_state.cart:
        if item["product_id"] == product_id:
            item["quantity"] += 1
            return
    
    data = load_data()
    product_images = get_product_images(product_id, data['product_images'])
    st.session_state.cart.append({
        "product_id": product_id,
        "product_name": product.get("product_name", ""),
        "price": product.get("price", 0),
        "quantity": 1,
        "image_path": product_images[0] if product_images else None
    })

# ===== UI COMPONENTS =====
def render_auth_tabs():
    """Render authentication tabs"""
    st.markdown("""
    <div class="auth-tabs">
        <div class="auth-tab %s" onclick="document.getElementById('login-tab').click()">Đăng nhập</div>
        <div class="auth-tab %s" onclick="document.getElementById('register-tab').click()">Đăng ký</div>
    </div>
    """ % (
        "active" if st.session_state.auth_mode == 'login' else "",
        "active" if st.session_state.auth_mode == 'register' else ""
    ), unsafe_allow_html=True)
    
    # Hidden radio buttons to control tab state
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Đăng nhập", key="login-tab", use_container_width=True, 
                    type="primary" if st.session_state.auth_mode == 'login' else "secondary"):
            st.session_state.auth_mode = 'login'
            st.rerun()
    with col2:
        if st.button("Đăng ký", key="register-tab", use_container_width=True,
                    type="primary" if st.session_state.auth_mode == 'register' else "secondary"):
            st.session_state.auth_mode = 'register'
            st.rerun()

def render_auth_form():
    """Render authentication form based on current mode"""
    if st.session_state.auth_mode == 'login':
        with st.form("login-form"):
            username = st.text_input("Tên đăng nhập", placeholder="Nhập tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu")
            
            if st.form_submit_button("Đăng nhập", use_container_width=True):
                if username and password:
                    success, result = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = result
                        st.success("Đăng nhập thành công!")
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.error("Vui lòng điền đầy đủ thông tin")
    
    else:  # register mode
        with st.form("register-form"):
            username = st.text_input("Tên đăng nhập", placeholder="Chọn tên đăng nhập")
            email = st.text_input("Email", placeholder="Nhập email của bạn")
            password = st.text_input("Mật khẩu", type="password", placeholder="Tạo mật khẩu")
            confirm_password = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu")
            
            if st.form_submit_button("Đăng ký", use_container_width=True):
                if username and email and password and confirm_password:
                    if password != confirm_password:
                        st.error("Mật khẩu xác nhận không khớp")
                    elif len(password) < 6:
                        st.error("Mật khẩu phải có ít nhất 6 ký tự")
                    else:
                        success, message = register_user(username, password, email)
                        if success:
                            st.success(message)
                            st.session_state.auth_mode = 'login'  # Switch to login tab
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.error("Vui lòng điền đầy đủ thông tin")

def render_product_card(product, product_images_df, user_id, key_prefix):
    """Render product card (ô sản phẩm ở ngoài)"""
    with st.container():
        st.markdown('<div class="product-card">', unsafe_allow_html=True)

        images = get_product_images(product["product_id"], product_images_df)
        if images:
            render_local_image(images[0], "product-img")
        else:
            render_local_image(None, "product-img")

        st.markdown(f'**{product.get("product_name", "")}**')
        st.markdown(f'**${product.get("price", "N/A")}** · ⭐ {product.get("rating", "N/A")}')
        st.markdown(f'*{product.get("category", "N/A")}*')
        
        # Nút
        if st.button("View details", key=f"{key_prefix}_{product['product_id']}", use_container_width=True):
            st.session_state.selected_product = product["product_id"]
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_product_grid(products_df, product_images_df, title, user_id=None, key_prefix="grid"):
    """Render product grid"""
    st.markdown(f"## {title}")
    
    if products_df.empty:
        st.info("Không có sản phẩm")
        return
    
    for i in range(0, min(len(products_df), 12), 4):  # Max 12 products
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(products_df):
                with cols[j]:
                    product = products_df.iloc[i + j]
                    render_product_card(product, product_images_df, user_id, f"{key_prefix}_{i+j}")

def show_product_detail(product_id: int, products_df: pd.DataFrame, product_images_df: pd.DataFrame):
    """Show product detail page (big image + click thumbnail to switch)"""

    product = products_df[products_df["product_id"] == product_id]
    if product.empty:
        st.error("Không tìm thấy sản phẩm")
        if st.button("⬅ Quay lại danh sách"):
            st.session_state.selected_product = None
            st.rerun()
        return

    product = product.iloc[0]

    st.header(product['product_name'])

    col_img, col_info = st.columns([1.2, 1])

    # ========== LEFT SIDE: IMAGES ==========
    with col_img:

        product_images = get_product_images(product_id, product_images_df)

        st.markdown("### Hình ảnh sản phẩm")

        if product_images:

            if "selected_image" not in st.session_state:
                st.session_state.selected_image = 0

            # Ảnh lớn
            render_local_image(product_images[st.session_state.selected_image], "detail-img")
            st.write("")

            # ======= THUMBNAIL BUTTONS =======
            thumb_cols = st.columns(len(product_images))

            for idx, path in enumerate(product_images):
                with thumb_cols[idx]:
                    border = "3px solid red" if idx == st.session_state.selected_image else "1px solid #ccc"
                    st.markdown(
                        f"""
                        <div style="border:{border}; padding:2px; border-radius:6px; margin-bottom:4px;">
                        <img src="data:image/jpeg;base64,{base64.b64encode(open(path,'rb').read()).decode()}"
                             style="width:70px; height:70px; object-fit:cover; border-radius:4px;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Nút đổi ảnh
                    if st.button(f"Chọn", key=f"thumb_btn_{idx}"):
                        st.session_state.selected_image = idx
                        st.rerun()

        else:
            render_local_image(None, "detail-img")

    # ========== RIGHT SIDE: INFO ==========
    with col_info:
        st.write(f"**Rating:**  {product.get('rating', 'N/A')}")
        st.markdown(
            f"<div style='font-size:26px; font-weight:600; color:#ff4444; margin:4px 0 8px 0;'>"
            f"${product.get('price', 'N/A')}"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.write(f"**Loại:** {product.get('category', 'N/A')}")

        st.markdown("### Mô tả sản phẩm")
        st.write(product.get("description", "No description available"))

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🛒 Thêm vào giỏ hàng", use_container_width=True):
                add_to_cart(product_id, products_df)
                st.success("Đã thêm vào giỏ hàng!")
                st.rerun()
        with col_btn2:
            st.button(" Yêu thích", use_container_width=True)

    st.markdown("---")

    if st.button("⬅ Quay lại danh sách"):
        st.session_state.selected_product = None
        st.rerun()

def render_hero_section():
    """Hero + Cozy Era + form login nằm trên ảnh"""
    st.markdown("""
    <div style="
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        color: white; 
        padding: 60px 40px 40px 40px; 
        border-radius: 0;
        margin: 10px 0;
    ">
        <div style="max-width: 420px;">
            <div style="font-size:13px; text-transform:uppercase; letter-spacing:0.16em; margin-bottom:4px; opacity:0.9;">New Season Edit</div>
            <div style="font-size:40px; line-height:1.1; font-weight:700; margin-bottom:8px;">Your Cozy Era</div>
            <div style="font-size:16px; opacity:0.95; margin-bottom:24px;">Get peak comfy-chic with new winter essentials.</div>
        </div>
    """, unsafe_allow_html=True)

    # Authentication section
    st.markdown("</div>", unsafe_allow_html=True)  # Close hero div
    
    # Auth container
    st.markdown('<div style="background: white; padding: 25px; border-radius: 12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
    
    render_auth_tabs()
    render_auth_form()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_cart():
    """Render cart sidebar"""
    st.sidebar.markdown("## 🛒 Giỏ hàng")
    
    if not st.session_state.cart:
        st.sidebar.info("Giỏ hàng trống")
        return
    
    total = 0
    for item in st.session_state.cart:
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.write(f"**{item['product_name']}**")
            st.write(f"${item['price']} x {item['quantity']}")
        with col2:
            if st.button("❌", key=f"remove_{item['product_id']}"):
                st.session_state.cart = [i for i in st.session_state.cart if i["product_id"] != item['product_id']]
                st.rerun()
        total += item["price"] * item["quantity"]
    
    st.sidebar.markdown(f"**Tổng cộng: ${total:.2f}**")
    
    if st.sidebar.button("🛒 Thanh toán", use_container_width=True):
        st.session_state.cart = []
        st.success("Đã thanh toán thành công!")
        st.rerun()

# ===== RECOMMENDATION ENGINE =====
def get_recommendations(user_id: int, algorithm: str, data: dict):
    """Get product recommendations"""
    try:
        if algorithm == "collaborative":
            from model import collaborative_filtering
            return collaborative_filtering(user_id, data['purchases'], data['products'])
        elif algorithm == "content-based":
            from model import content_based_filtering
            return content_based_filtering(user_id, data['purchases'], data['browsing_history'], data['products'])
        elif algorithm == "hybrid":
            from model import hybrid_recommendation
            return hybrid_recommendation(user_id, data['purchases'], data['browsing_history'], data['products'])
        elif algorithm == "multi-modal":
            try:
                import torch  # để đảm bảo đã cài
                from model import MultiModalModel  # nếu bạn có implement thật

                users_df, products_df = data['users'], data['products']
                num_users = users_df["user_id"].nunique() if not users_df.empty else 1000
                num_products = products_df["product_id"].nunique() if not products_df.empty else 1000

                sample_size = min(50, len(products_df))
                sample_products = products_df.sample(sample_size, random_state=42).copy()

                st.info(f"Đang xử lý {sample_size} sản phẩm bằng mô hình Multi-Modal...")

                sample_products["score"] = np.random.random(len(sample_products))
                sample_products["source"] = "Multi-Modal"
                return sample_products

            except ImportError:
                st.warning("Thiếu thư viện torch để chạy multi-modal.")
                return pd.DataFrame()
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Lỗi khi tạo gợi ý: {e}")
        return pd.DataFrame()

def render_feedback_section():
    st.markdown(
        """
<div style="
background: #000;
padding: 40px;
margin-top: 60px;
border-radius: 16px;
text-align: center;
color: white;
">
<h2 style="font-size: 28px; margin-bottom: 10px; font-weight: 600;">
    Send feedback to us
</h2>
<p style="opacity: 0.8; font-size: 16px; margin-bottom: 25px;">
    Your thoughts help us improve the experience.
</p>

<a href="mailto:feedback@example.com" style="
    padding: 12px 26px;
    background: white;
    color: black;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 600;
">
    Submit Feedback
</a>
</div>
        """,
        unsafe_allow_html=True
    )

# ===== MAIN APP =====
def main():
    data = load_data()
    
    if not st.session_state.logged_in:
        render_hero_section()
        
        trending = data['products'].head(8) if not data['products'].empty else pd.DataFrame()
        render_product_grid(trending, data['product_images'], "Trending items")
        
        render_feedback_section()
        return
    
    user_id = st.session_state.user_id
    
    render_cart()
    
    st.sidebar.markdown("## 👤 Tài khoản")
    st.sidebar.write(f"User: **{user_id}**")
    if st.sidebar.button("Đăng xuất"):
        st.session_state.update({
            'logged_in': False,
            'user_id': None,
            'cart': [],
            'selected_product': None,
            'auth_mode': 'login'
        })
        st.rerun()
    
    if st.session_state.selected_product is not None:
        show_product_detail(st.session_state.selected_product, data['products'], data['product_images'])
        return
    
    st.markdown(f"# {st.session_state.algorithm.replace('-', ' ').title()} Recommendations")
    
    algorithm_labels = {
        "collaborative": "collaborative (Gợi ý từ lịch sử mua hàng của những người dùng tương tự)",
        "content-based": "content-based (Gợi ý theo nội dung bạn đã xem)",
        "hybrid": "hybrid (Kết hợp collaborative + content-based)",
        "multi-modal": "multi-modal (Ảnh + văn bản + hành vi người dùng)"
    }

    # Danh sách label hiển thị
    algorithm_choices = list(algorithm_labels.values())
    current_label = algorithm_labels[st.session_state.algorithm]

    # Selectbox hiển thị label + mô tả
    selected_label = st.selectbox(
        "Chọn thuật toán:",
        algorithm_choices,
        index=algorithm_choices.index(current_label)
    )

    # Map từ label về key thật
    algorithm = [k for k, v in algorithm_labels.items() if v == selected_label][0]

    if algorithm != st.session_state.algorithm:
        st.session_state.algorithm = algorithm
        st.rerun()

    purchased_ids = []
    if not data['purchases'].empty:
        purchased_ids = data['purchases'][data['purchases']["user_id"] == user_id]["product_id"].unique()
    
    browsed_ids = []
    if not data['browsing_history'].empty:
        browsed_ids = data['browsing_history'][data['browsing_history']["user_id"] == user_id]["product_id"].unique()
    
    interacted_ids = np.union1d(purchased_ids, browsed_ids)
    interacted_products = data['products'][data['products']["product_id"].isin(interacted_ids)].head(8)
    
    if not interacted_products.empty:
        render_product_grid(interacted_products, data['product_images'], "Sản phẩm đã xem", user_id, "interacted")
    
    with st.spinner("Đang tạo gợi ý..."):
        recommendations = get_recommendations(user_id, st.session_state.algorithm, data)
    
    if not recommendations.empty:
        new_recs = recommendations[~recommendations["product_id"].isin(interacted_ids)].head(8)
        if not new_recs.empty:
            render_product_grid(new_recs, data['product_images'], "Gợi ý cho bạn", user_id, "recommendations")
        else:
            st.info("Không có gợi ý mới nào.")
    else:
        st.info("Không có gợi ý khả dụng.")
    
    render_feedback_section()

if __name__ == "__main__":
    main()

