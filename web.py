# ------------------------------------------------------------
# Streamlit UI for Product Recommender System (1-file version)
# ------------------------------------------------------------
# Cách chạy:
#   pip install streamlit pandas torch sentence-transformers torch-geometric torchvision
#   streamlit run streamlit_web1.py
# ------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import logging
import os

# Cố gắng import mô hình
multimodal_ok = True
try:
    import torch
    from model import (
        collaborative_filtering,
        content_based_filtering,
        hybrid_recommendation,
        MultiModalModel,
    )
except Exception:
    multimodal_ok = False
    try:
        from model import (
            collaborative_filtering,
            content_based_filtering,
            hybrid_recommendation,
        )
    except Exception:
        raise

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("streamlit-app")

st.set_page_config(page_title="Product Recommender", layout="wide")

# ========== SESSION STATE ==========
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None


# ========== AUTH MODULE HERO ==========
def save_users(users_df: pd.DataFrame, path: str = "users_expanded.csv"):
    """Ghi lại dữ liệu user vào CSV (ghi đè)."""
    try:
        users_df.to_csv(path, index=False, encoding="utf-8")
    except PermissionError:
        st.error(" Không ghi được file users_expanded.csv (có thể đang mở trong Excel).")


def auth_hero(
    users_df: pd.DataFrame,
    products: pd.DataFrame,
    purchases: pd.DataFrame,
    product_images: pd.DataFrame,
):
    """
    Màn hình hero giống layout Figma + Trending items bên dưới:
    - Thanh đen trên cùng
    - Ảnh nền to
    - Text “Your Cozy Era…”
    - Ô Enter User ID + nút mũi tên
    - Nút RUN RECOMMENDATION
    - Dải Trending items (top sản phẩm theo lượt mua) ở dưới hero
    """

    # ===== Thanh đen trên cùng =====
    st.markdown(
        """
        <div style="
            width:100%;
            background-color:#111111;
            color:#ffffff;
            text-align:center;
            padding:6px 0;
            font-size:12px;
            font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
        ">
            Get early access on launches and offers. <u>Sign Up For Texts</u> &rarr;
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ===== CSS cho hero =====
    st.markdown(
        """
        <style>
        .auth-hero-wrapper {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 0 16px 0;
        }
        .auth-hero {
            border-radius: 0;
            overflow: hidden;
            position: relative;
            min-height: 420px;
            background-image: url('https://images.pexels.com/photos/6311650/pexels-photo-6311650.jpeg?auto=compress&cs=tinysrgb&w=1600');
            background-size: cover;
            background-position: center;
        }
        .auth-hero-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, rgba(0,0,0,0.65), rgba(0,0,0,0.15));
        }
        .auth-hero-content {
            position: relative;
            z-index: 2;
            padding: 80px 80px;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            gap: 16px;
            max-width: 420px;
            font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
        }
        .auth-tagline {
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            margin-bottom: 4px;
            opacity: 0.9;
        }
        .auth-title {
            font-size: 40px;
            line-height: 1.1;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .auth-subtitle {
            font-size: 16px;
            opacity: 0.95;
            margin-bottom: 24px;
        }
        .auth-input-label {
            font-size: 12px;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 6px;
            opacity: 0.9;
        }
        .auth-run-btn > button {
            border-radius: 0;
            padding: 10px 26px;
            background-color: #ffffff;
            color: #111111;
            border: 1px solid #111111;
            font-size: 12px;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ===== Hero container =====
    st.markdown('<div class="auth-hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-hero">', unsafe_allow_html=True)
    st.markdown('<div class="auth-hero-overlay"></div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-hero-content">', unsafe_allow_html=True)

    # Text giống Figma
    st.markdown('<div class="auth-tagline">New Season Edit</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Your Cozy Era</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="auth-subtitle">Get peak comfy-chic with new winter essentials.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="auth-input-label">ENTER USER ID</div>', unsafe_allow_html=True)

    # Hàng input + nút mũi tên
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        user_id_text = st.text_input(
            label="",
            placeholder="Enter User ID",
            label_visibility="collapsed",
            key="hero_user_id",
        )
    with col_btn:
        arrow_clicked = st.button("➜", key="hero_arrow")

    # Nút RUN RECOMMENDATION
    run_clicked = st.container()
    with run_clicked:
        run_btn = st.button("RUN RECOMMENDATION", key="hero_run")

    # Logic login: dùng user_id
    triggered = arrow_clicked or run_btn
    if triggered:
        if not user_id_text:
            st.error("Vui lòng nhập User ID trước.")
        else:
            try:
                uid = int(user_id_text)
            except ValueError:
                st.error("User ID phải là số.")
            else:
                if "user_id" in users_df.columns and uid in users_df["user_id"].values:
                    st.session_state.logged_in = True
                    st.session_state.user_id = int(uid)
                    st.success(" Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error(" User ID không tồn tại trong dữ liệu.")

    st.markdown("</div>", unsafe_allow_html=True)   # auth-hero-content
    st.markdown("</div>", unsafe_allow_html=True)   # auth-hero
    st.markdown("</div>", unsafe_allow_html=True)   # auth-hero-wrapper

    # ====== Trending items bên dưới hero (khi chưa login) ======
    trending_df = build_trending(products, purchases, top_n=20)
    render_product_carousel(
        trending_df,
        product_images,
        title="Trending items",
        subtitle="Beautifully Functional. Purposefully Designed. Consciously Crafted.",
        key_prefix="trending_public",
        user_id=None,
        enable_view_button=False,
    )


def require_login(
    users_df: pd.DataFrame,
    products: pd.DataFrame,
    purchases: pd.DataFrame,
    product_images: pd.DataFrame,
):
    """
    Nếu đã login → trả về user_id.
    Nếu chưa login → hiển thị hero + trending items và dừng app.
    """
    if st.session_state.get("logged_in") and st.session_state.get("user_id") is not None:
        return int(st.session_state.user_id)

    # chưa login → hiện hero + trending
    auth_hero(users_df, products, purchases, product_images)
    return None


# ========== HÀM ĐỌC / GHI CSV CƠ BẢN ==========
def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def load_users(path: str = "users_expanded.csv") -> pd.DataFrame:
    df = load_csv(path)
    if df.empty:
        return pd.DataFrame(columns=["user_id", "user_name", "user_password"])
    return df


# ========== HELPER: TRENDING + CAROUSEL ==========

def build_trending(
    products: pd.DataFrame,
    purchases: pd.DataFrame,
    top_n: int = 20,
) -> pd.DataFrame:
    """Tạo danh sách Trending items theo số lượt mua giảm dần."""
    if products is None or products.empty:
        return pd.DataFrame()

    if purchases is None or purchases.empty or "product_id" not in purchases.columns:
        return products.head(top_n).copy()

    counts = (
        purchases.groupby("product_id")
        .size()
        .reset_index(name="purchase_count")
    )

    df = products.merge(counts, on="product_id", how="left")
    df["purchase_count"] = df["purchase_count"].fillna(0)
    df = df.sort_values("purchase_count", ascending=False).head(top_n)
    return df


def render_product_carousel(
    df: pd.DataFrame,
    product_images: pd.DataFrame,
    title: str,
    subtitle: str = None,
    key_prefix: str = "carousel",
    user_id: int = None,
    enable_view_button: bool = False,
):
    """
    Hiển thị một dải sản phẩm dạng slider ngang:
    - Mỗi trang 4 sản phẩm
    - Có nút ◀ ▶ để chuyển trang (giả lập kéo ngang)
    """
    if df is None or df.empty:
        st.info("Không có sản phẩm để hiển thị.")
        return

    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(
            f"<div style='text-align:center; font-size:13px; color:#555; "
            f"margin-top:4px; margin-bottom:24px;'>{subtitle}</div>",
            unsafe_allow_html=True,
        )

    per_page = 4
    total = len(df)
    total_pages = int(np.ceil(total / per_page))

    page_key = f"{key_prefix}_page"
    if page_key not in st.session_state:
        st.session_state[page_key] = 0
    page = st.session_state[page_key]
    page = max(0, min(page, total_pages - 1))

    start = page * per_page
    end = min(start + per_page, total)
    subset = df.iloc[start:end]

    cols = st.columns(len(subset))

    for col, (_, row) in zip(cols, subset.iterrows()):
        with col:
            st.markdown(
                "<div style='background-color:#ffffff; border:1px solid #eee;"
                "border-radius:10px; padding:10px 10px 14px 10px; "
                "font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;'>",
                unsafe_allow_html=True,
            )

            # Ảnh
            img_path = None
            if product_images is not None and not product_images.empty:
                match = product_images[
                    product_images["product_id"] == row["product_id"]
                ]
                if not match.empty:
                    img_path = match.iloc[0].get("image_path")
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.write(" (No image)")

            # Tên + giá + rating + category
            st.markdown(
                f"<div style='font-size:13px; margin-top:8px; font-weight:500;'>"
                f"{row.get('product_name', '')}</div>",
                unsafe_allow_html=True,
            )

            price = row.get("price", "N/A")
            rating = row.get("rating", "N/A")
            category = row.get("category", "N/A")

            st.markdown(
                f"<div style='font-size:13px; color:#333; margin-top:2px;'>"
                f"${price} &nbsp;&nbsp;·&nbsp;&nbsp; {rating}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='font-size:12px; color:#777; margin-top:2px;'>"
                f"{category}</div>",
                unsafe_allow_html=True,
            )

            if enable_view_button and user_id is not None:
                if st.button(
                    "View details",
                    key=f"{key_prefix}_detail_{row['product_id']}",
                ):
                    log_browsing(user_id, row["product_id"])
                    st.session_state.selected_product = row["product_id"]
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # Nút chuyển trang
    if total_pages > 1:
        nav1, nav2, nav3 = st.columns([1, 3, 1])
        with nav1:
            if st.button("◀", key=f"{key_prefix}_prev") and page > 0:
                st.session_state[page_key] = page - 1
                st.rerun()
        with nav2:
            st.write(f"Trang {page + 1}/{total_pages}")
        with nav3:
            if st.button("▶", key=f"{key_prefix}_next") and page < total_pages - 1:
                st.session_state[page_key] = page + 1
                st.rerun()


# ========== HÀM GHI LỊCH SỬ XEM / MUA ==========
def log_browsing(user_id, product_id):
    """Ghi một dòng vào browsing_history_expanded.csv."""
    bh = load_csv("browsing_history_expanded.csv")
    if bh.empty:
        bh = pd.DataFrame(columns=["user_id", "product_id"])
    row = {col: None for col in bh.columns}
    if "user_id" in bh.columns:
        row["user_id"] = user_id
    if "product_id" in bh.columns:
        row["product_id"] = product_id
    bh = pd.concat([bh, pd.DataFrame([row])], ignore_index=True)
    try:
        bh.to_csv("browsing_history_expanded.csv", index=False, encoding="utf-8")
    except PermissionError:
        st.warning(
            " Không ghi được file browsing_history_expanded.csv (có thể đang mở trong Excel)."
        )


def log_purchase(user_id, product_id):
    """Ghi một dòng vào purchases_expanded.csv."""
    p = load_csv("purchases_expanded.csv")
    if p.empty:
        p = pd.DataFrame(columns=["user_id", "product_id"])
    row = {col: None for col in p.columns}
    if "user_id" in p.columns:
        row["user_id"] = user_id
    if "product_id" in p.columns:
        row["product_id"] = product_id
    p = pd.concat([p, pd.DataFrame([row])], ignore_index=True)
    try:
        p.to_csv("purchases_expanded.csv", index=False, encoding="utf-8")
    except PermissionError:
        st.warning(
            " Không ghi được file purchases_expanded.csv (có thể đang mở trong Excel)."
        )


# ========== HÀM HIỂN THỊ TRANG CHI TIẾT SẢN PHẨM ==========
def show_product_detail(user_id, product_id, products, product_images):
    """Hiển thị trang chi tiết sản phẩm + nút mua, nút quay lại."""
    product_df = products[products["product_id"] == product_id]
    if product_df.empty:
        st.error("Không tìm thấy sản phẩm.")
        if st.button("⬅ Quay lại danh sách"):
            st.session_state.selected_product = None
            st.rerun()
        return

    product = product_df.iloc[0]

    st.header(f"{product['product_name']}")

    col_img, col_info = st.columns([1, 2])

    with col_img:
        match = product_images[product_images["product_id"] == product_id]
        img_path = None
        if not match.empty:
            img_path = match.iloc[0].get("image_path")
        if img_path and os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.write(" (No image)")

    with col_info:
        st.write(f"**Rating:** {product.get('rating', 'N/A')}")
        st.write(f"**Giá:** {product.get('price', 'N/A')}$")
        st.write(f"**Loại:** {product.get('category', 'N/A')}")
        st.write("### Mô tả")
        st.write(product.get("description", ""))

        if st.button(" Mua ngay"):
            log_purchase(user_id, product_id)
            st.success(" Đã ghi nhận mua sản phẩm!")
            st.rerun()

    st.markdown("---")
    if st.button("⬅ Quay lại"):
        st.session_state.selected_product = None
        st.rerun()


# ====== NẠP DỮ LIỆU ======
users = load_users("users_expanded.csv")
products = load_csv("products_expanded.csv")
product_images = load_csv("product_images_expanded.csv")
purchases = load_csv("purchases_expanded.csv")
browsing_history = load_csv("browsing_history_expanded.csv")

# ====== LOGIN / LANDING ======
logged_user_id = require_login(users, products, purchases, product_images)
if logged_user_id is None:
    st.stop()   # chỉ hiển thị hero + trending, không chạy tiếp

user_id = logged_user_id

# ====== ACCOUNT / LOGOUT ======
st.sidebar.markdown("## 👤 Tài khoản")
st.sidebar.write(f"Đang đăng nhập: **User {user_id}**")

if st.sidebar.button("⬅ Quay lại trang đăng nhập ban đầu"):
    # reset trạng thái đăng nhập + trang chi tiết + các trang carousel
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.selected_product = None

    # reset page của các carousel (nếu có)
    for k in list(st.session_state.keys()):   # ⬅ CHỈ keys(), không có 's'
        if k.endswith("_page"):
            del st.session_state[k]

    st.rerun()

# Sau khi login mới hiện title
st.title("🛍️ Product Recommender — Streamlit Demo")

# Nếu đang ở trang chi tiết sản phẩm → hiển thị chi tiết & dừng
if st.session_state.selected_product is not None:
    show_product_detail(user_id, st.session_state.selected_product, products, product_images)
    st.stop()

# ====== SAU KHI LOGIN: DASHBOARD RECOMMENDATION ======

# 1. Thiết lập gợi ý (chỉ hiện sau login)
st.sidebar.header("⚙️ Thiết lập gợi ý")
algorithms = ["collaborative", "content-based", "hybrid"]
if multimodal_ok:
    algorithms.append("multi-modal")
algorithm = st.sidebar.selectbox("Thuật toán", algorithms, index=0)
top_k = st.sidebar.slider("Số gợi ý tối đa", 1, 50, 10)

st.header(" Recommendation dashboard")
st.markdown("#### 1. Recommendation settings")
st.write(f"Thuật toán hiện tại: **{algorithm}** — Số gợi ý tối đa: **{top_k}**")

# 2. Sản phẩm đã tương tác
purchased_ids = purchases[purchases.get("user_id") == user_id]["product_id"].unique() \
    if not purchases.empty and "user_id" in purchases.columns else []
browsed_ids = browsing_history[browsing_history.get("user_id") == user_id]["product_id"].unique() \
    if not browsing_history.empty and "user_id" in browsing_history.columns else []

interacted = products[
    products["product_id"].isin(np.union1d(purchased_ids, browsed_ids))
].copy()
if not interacted.empty:
    interacted["source"] = interacted["product_id"].apply(
        lambda x: "Purchased" if x in purchased_ids else "Browsed"
    )

st.markdown("#### 2. Products you interacted with")
render_product_carousel(
    interacted,
    product_images,
    title="Products you've interacted with",
    subtitle=None,
    key_prefix="interacted",
    user_id=user_id,
    enable_view_button=True,
)

# 3. Gợi ý sản phẩm
st.markdown("#### 3. Recommended for you")

try:
    if algorithm == "collaborative":
        recs = collaborative_filtering(user_id, purchases, products)

    elif algorithm == "content-based":
        recs = content_based_filtering(
            user_id, purchases, browsing_history, products
        )

    elif algorithm == "hybrid":
        recs = hybrid_recommendation(
            user_id, purchases, browsing_history, products
        )

    elif algorithm == "multi-modal":
        if not multimodal_ok:
            st.warning(" Thiếu phụ thuộc để chạy multi-modal.")
            recs = pd.DataFrame()
        else:
            num_users = users["user_id"].nunique()
            num_products = products["product_id"].nunique()
            model = MultiModalModel(num_users, num_products)

            products["product_index"] = (
                products["product_id"].astype(str).str.extract(r"(\d+)").astype(int)
            )

            sample_n = min(50, len(products))
            products_sample = products.sample(sample_n, random_state=42).copy()

            st.info(
                f" Đang xử lý {sample_n} sản phẩm bằng mô hình Multi-Modal..."
            )

            product_ids_tensor = (
                torch.LongTensor(products_sample["product_index"].values) - 1
            )
            texts = products_sample["description"].fillna("").tolist()

            with torch.no_grad():
                outputs = model(
                    torch.LongTensor([user_id - 1]),
                    product_ids_tensor,
                    texts,
                    edge_index=None,
                    product_images_df=product_images,
                )

            scores = outputs.mean(dim=1).cpu().numpy()
            recs = products_sample.copy()
            recs["score"] = scores
            recs["source"] = "Multi-Modal"

    else:
        recs = pd.DataFrame()

except Exception as e:
    st.exception(e)
    st.stop()

# Chuẩn hóa product_id
if recs is not None and not recs.empty and "product_id" in recs.columns:
    recs["product_id"] = recs["product_id"].astype(str)
    recs["product_id"] = recs["product_id"].apply(
        lambda x: f"id_{int(x):08d}" if not str(x).startswith("id_") else x
    )

if recs is None or recs.empty:
    st.info("ℹ Không có gợi ý khả dụng.")
else:
    # Không gợi ý lại các sản phẩm đã mua/xem
    recs = recs[
        ~recs["product_id"].isin(purchased_ids)
        & ~recs["product_id"].isin(browsed_ids)
    ].copy()

    if "score" not in recs.columns:
        recs["score"] = 0.0

    recs = recs.sort_values("score", ascending=False).head(top_k)

    render_product_carousel(
        recs,
        product_images,
        title="Trending items just for you",
        subtitle="Gợi ý dựa trên hành vi và lịch sử tương tác của bạn.",
        key_prefix="recs",
        user_id=user_id,
        enable_view_button=True,
    )
