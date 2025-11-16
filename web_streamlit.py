# --------- LẤY SẢN PHẨM ĐÃ TƯƠNG TÁC (đã mua/đã xem) ---------
purchased_ids = purchases[purchases['user_id'] == user_id]['product_id'].unique() 
#Lấy danh sách sản phẩm người dùng đã mua
browsed_ids = browsing_history[browsing_history['user_id'] == user_id]['product_id'].unique()
#Lấy danh sách sản phẩm người dùng đã xem

#Gộp các sản phẩm đã mua hoặc đã xem để hiển thị cho người dùng, tạo bản sao để tránh ảnh hưởng đến dữ liệu gốc
interacted = products[products['product_id'].isin(np.union1d(purchased_ids, browsed_ids))].copy() 
if not interacted.empty:  #kiểm tra nếu tương tác k rỗng 
    #Gắn nhãn nguồn tương tác: Purchased hay Browsed
    #Thêm cột source để xác định xem sản phẩm đó được mua hay chỉ xem
    interacted['source'] = interacted['product_id'].apply(   
        lambda x: "Purchased" if x in purchased_ids else "Browsed"
    )

st.subheader("Sản phẩm đã tương tác") #Hiển thị tiêu đề trên streamlit
st.dataframe(interacted)              #Hiển thị bảng tương tác 

# --------- CHẠY THUẬT TOÁN GỢI Ý ---------
st.subheader("Gợi ý") #Hiển thị tiêu đề gợi ý 
try:                  #Bắt đầu khối xử lí lỗi (vì các mô hình có thể sinh lỗi khi chạy nếu thiếu dữ liệu)
    if algorithm == "collaborative":    #Kiểm tra thuật toán collaborative
        #Nếu là collaborative, gọi hàm collaborative_filtering để tạo gợi ý dựa trên hành vi người dùng khác
        recs = collaborative_filtering(user_id, purchases, products)

    elif algorithm == "content-based":  #Kiểm tra thuật toán content-based 
        #Nếu là content-based, gọi hàm content_based_filtering dựa trên nội dung sản phẩm
        recs = content_based_filtering(user_id, purchases, browsing_history, products)

    elif algorithm == "hybrid":         #Kiểm tra thuật toán hybrid
        #Nếu là hybrid, gọi hàm hybrid_recommmendation dựa trên kết hợp 2 thuật toán collaborative và content-based
        recs = hybrid_recommendation(user_id, purchases, browsing_history, products)

    elif algorithm == "multi-modal":    #Kiểm tra thuật toán multi-modal
        
        if not multimodal_ok:      #Kiểm tra xem có đủ dữ liệu để chạy
            st.warning("⚠️ Thiếu phụ thuộc để chạy multi-modal.")   #Hiển thị cảnh báo nếu thiếu 
            recs = pd.DataFrame()  #Tạo dataframe rỗng nếu k thể chạy 
        else:                      #Nếu đủ điều kiện bắt đầu chạy multi modal
        
            num_users = users['user_id'].nunique()           #Đếm số lượng người dùng 
            num_products = products['product_id'].nunique()  #Đếm số lượng sản phẩm 
            model = MultiModalModel(num_users, num_products) #Khởi tạo mô hình 
           
            #Chuyển đổi product_id thành số nguyên 
            products['product_index'] = (
                products['product_id'].astype(str).str.extract(r'(\d+)').astype(int)
            )
            #Giới hạn sản phẩm để tránh tràn RAM
            sample_n = min(50, len(products))                                    #Lấy giới hạn 50 sản phẩm 
            products_sample = products.sample(sample_n, random_state=42).copy()  #Lấy mẫu ngẫu nhiên từ DataFrame

            st.info(f"🧠 Đang xử lý {sample_n} sản phẩm bằng mô hình Multi-Modal... Vui lòng chờ vài giây ⏳")  #Hiển thị thông báo 

            #Chuẩn bị input cho mô hình:
            #Chuyển danh sách product_id từ products thành torch.LongTensor để đưa vào Embedding
            product_ids_tensor = torch.LongTensor(products['product_id'].values) - 1  #Thêm -1 để product_id chuyển sang 0-index 

            #Lấy danh sách mô tả sản phẩm 
            texts = products['description'].fillna("").tolist() #Nếu thiếu thì điền rỗng để tránh lỗi 

            
            with torch.no_grad():   #Tắt tính toán gradient (tăng tốc, tiết kiệm bộ nhớ)

                outputs = model(
                    torch.LongTensor([user_id - 1]),   #Truyền user_id (0-indexed) vào model
                    product_ids_tensor,                #Truyền toàn bộ ID sản phẩm vào model để tính điểm
                    texts,                             #Truyền mô tả văn bản song song với product_ids
                    edge_index=None,                   #Không dùng graph (GNN) 
                    product_images_df=product_images   #Truyền thông tin ảnh sản phẩm nếu có 
                )

            #Rút gọn vector đặc trưng của từng sản phẩm thành 1 giá trị duy nhất (score) và chuyển về dạng NumPy
            scores = outputs.mean(dim=1).cpu().numpy()  #outputs có shape[num_products, embedding_dim], lấy trung bình của toàn bộ các giá trị trong vector embedding
            recs = products.copy()              #Tạo bản sao DataFrame products
            recs['score'] = scores              #Gán cột score cho từng sản phẩm 
            recs['source'] = 'Multi-Modal'      #Gán source là Multi-Modal
    else:
        #Nếu thuật toán k trùng với case nào, trả về dataframe rỗng 
        recs = pd.DataFrame()

except Exception as e:  
    #Nếu lỗi xảy ra ở khối try, bắt exception và xử lý
    st.exception(e)  #Hiển thị lỗi trực tiếp 
    st.stop()        #Dừng chạy nếu có lỗi 

# --------- HẬU XỬ LÝ VÀ HIỂN THỊ KẾT QUẢ ---------
if recs is None or recs.empty:           #Kiểm tra nếu gợi ý là k có hoặc rỗng
    st.info("Không có gợi ý khả dụng.")  #Hiển thị thông báo nếu k có gợi ý 
else:
    #Nếu có dữ liệu, lọc và bỏ sản phẩm người dùng đã tương tác (tránh gợi ý lại những cái đã mua hoặc đã xem)
    recs = recs[
        ~recs['product_id'].isin(purchased_ids) &
        ~recs['product_id'].isin(browsed_ids)
    ].copy()

    #Cột score là điểm đánh giá độ phù hợp sản phẩm, xếp hạng và so sánh kết quả giữa các thuật toán 
    if 'score' not in recs.columns: #Kiểm tra nếu chưa có cột score
        recs['score'] = 0.0         #Gán tạm giá trị 0.0 cho tất cả nếu chưa có cột score 

    #Sắp xếp gợi ý theo score giảm dần và lấy ra các sản phẩm đứng đầu (k sản phẩm đầu tiên)
    recs = recs.sort_values('score', ascending=False).head(top_k)

    #Hiển thị bảng kết quả gợi ý
    st.markdown("### 💡 Kết quả gợi ý")  
    for _, row in recs.iterrows():       #Chạy vòng lặp từng dòng 
        col1, col2 = st.columns([1, 3])  #Chia 2 cột 
        with col1:
            img_path = None  #Khởi tạo đường dẫn ảnh mặc định bằng k có ảnh 
            match = product_images[product_images['product_id'] == row['product_id']] #Tìm ảnh tương ứng với sản phẩm
            if not match.empty:   #Kiểm tra xem có tìm được ảnh 
                img_path = match.iloc[0]['image_path'] #Lấy đường dẫn ảnh từ dòng đầu 
            if img_path and os.path.exists(img_path):  #Kiểm tra xem file, đường dẫn có tồn tại 
                st.image(img_path, use_container_width=True) #Hiển thị hình ảnh 
            else:                           #Nếu k có ảnh
                st.write("🖼️ (No image)")  #Hiển thị thông báo 
        with col2:
            st.markdown(f"**{row['product_name']}**")    #Hiển thị tên sản phẩm
            st.write(f"⭐ {row['rating']} | 💵 {row['price']}$ | 🏷️ {row.get('category', 'N/A')}") #Hiển thị rating, giá và category 
            st.caption(row['description'][:200] + "...") #Hiển thị mô tả 
            st.write(f"**Score:** {row['score']:.3f}")   #Hiển thị score 
        st.markdown("---")  #Thêm đường phân cách giữa các sản phẩm 


#Chú thích cuối trang: mô tả ngắn gọn về hệ thống 
st.caption(
    "UI viết bằng Streamlit (1 file). Các thuật toán: collaborative, content-based, hybrid, multi-modal (giới hạn mẫu để tránh tràn RAM)."
)
