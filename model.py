import pandas as pd
import logging
import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv
from sentence_transformers import SentenceTransformer
from torchvision.models import resnet50
from torchvision import transforms
from PIL import Image
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

'''Hàm gợi ý dựa trên hành vi mua sắm của người dùng khác có sở thích tương tự'''
def collaborative_filtering(user_id: int, purchases: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    logger.debug(f"Collaborative Filtering for user_id: {user_id}")
    user_purchases = purchases[purchases['user_id'] == user_id]['product_id'].unique()
    logger.debug(f"User purchases: {user_purchases}")

    other_users = purchases[purchases['product_id'].isin(user_purchases) & purchases['user_id'] != user_id]['user_id'].unique()
    other_purchases = purchases[purchases['user_id'].isin(other_users)]
    product_counts = other_purchases['product_id'].value_counts()
    recommendations = products[products['product_id'].isin(product_counts.index) &
                               ~products['product_id'].isin(user_purchases)].copy()
   
    recommendations['purchase_count'] = recommendations['product_id'].map(product_counts).fillna(0)
    recommendations['raw_score'] = recommendations['purchase_count']*recommendations['rating']
    recommendations['score'] = recommendations['raw_score']/product_counts.max()
    recommendations['source'] = 'Collaborative Filtering'
    logger.debug(f"Collaborative recommendations: \n{recommendations[['product_id', 'score', 'source']]}")
    
    return recommendations.sort_values(by='score',ascending = False)

'''Hàm gợi ý dựa trên lịch sử xem '''
def content_based_filtering(user_id: int, purchases: pd.DataFrame, browsing_history: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    logger.debug(f"Content-Based Filtering for user_id: {user_id}")
    user_history = browsing_history[browsing_history['user_id'] == user_id]['product_id'].unique()
    logger.debug(f"User browsing history: {user_history}")
    user_products = products[products['product_id'].isin(user_history)]
    if not user_products.empty and 'category' in products.columns:
        recommendations = products[products['category'].isin(user_products['category']) & 
                                   ~products['product_id'].isin(user_history)].copy()
        
        avg_rating = user_products['rating'].mean()
        recommendations['score'] = recommendations['rating']/5.0 * avg_rating
    else:
        recommendations = pd.DataFrame(columns = ['product_id', 'product_name', 'price', 'rating', 'score', 'source'])
        logger.debug("No content-based recommendations.")
    recommendations['source'] = 'Content-Based Filtering'
    logger.debug(f"Content-based recommendations:\n{recommendations[['product_id', 'score', 'source']]}")
    return recommendations

def hybrid_recommendation(user_id, purchases, browsing_history, products):
    logger.debug(f"Hybrid Recommendation for user_ id: {user_id}")
    user_purchases = purchases[purchases['user_id'] == user_id]['product_id'].unique()
    user_browsed = browsing_history[browsing_history['user_id'] == user_id]['product_id'].unique()
    user_history = set(user_purchases).union(user_browsed)
    logger.debug(f"User history (purchases + browsed): {user_history}")
    collab_recs = collaborative_filtering(user_id, purchases, products)
    content_recs = content_based_filtering(user_id, purchases, browsing_history, products)
    all_recommendations = pd.concat([collab_recs, content_recs], ignore_index=True)
    logger.debug(f"Combined recommendations:\n{all_recommendations[['product_id', 'score', 'source']]}")
    if all_recommendations.empty:
        logger.debug("No recommendations; adding popular products.")

        popular_products = purchases['product_id'].value_counts().head(3).index
        all_recommendations = products[products['product_id'].isin(popular_products) & 
                                      ~products['product_id'].isin(user_history)].copy()

        all_recommendations['score'] = 0.5
        all_recommendations['source'] = 'Popular Products'

    final_recommendations = all_recommendations.sort_values(by='score', ascending=False) \
                                               .drop_duplicates(subset=['product_id'], keep='first')  
    logger.debug(f"Final hybrid recommendations:\n{final_recommendations[['product_id', 'score', 'source']]}")
    
    return final_recommendations

class MultiModalModel(nn.Module):
    def __init__(self, num_users, num_products, embedding_dim=128):
        super().__init__() 
        self.user_emb = nn.Embedding(num_users, embedding_dim)

        self.product_emb = nn.Embedding(num_products, embedding_dim)
        
        self.image_encoder = resnet50(pretrained=True)

        self.image_encoder.fc = nn.Linear(2048, embedding_dim)
        
        self.view_embedding = nn.Embedding(4, embedding_dim)  # front, side, back, full

        self.style_projection = nn.Linear(embedding_dim, embedding_dim)
        
        for name, param in self.image_encoder.named_parameters():
            if 'layer4' in name or 'fc' in name:
                param.requires_grad = True
            else:
                param.requires_grad = False
        
        self.text_encoder = SentenceTransformer('all-MiniLM-L6-v2')

        self.text_proj = nn.Linear(384, embedding_dim)
        
        self.conv1 = GCNConv(embedding_dim, embedding_dim)
        
        self.fusion = nn.Linear(embedding_dim * 3, embedding_dim)

    def forward(self, user_ids, product_ids, text_batch, edge_index, product_images_df=None):
        """ Phần này là phần xử lý các thông tin liên quan đến các loại thông tin kết hợp về khách hàng và sản phẩm của cửa hàng """

        user_emb = self.user_emb(user_ids)

        product_emb = self.product_emb(product_ids)
        
        if len(user_emb.shape) == 2 and len(product_emb.shape) == 2 and user_emb.shape[0] == 1:
            user_emb = user_emb.expand(product_emb.shape[0], -1)
        
        """ Phần này là xử lý thông tin về các loại hình ảnh """
        if product_images_df is not None:
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            product_id_to_info = {}

            for _, row in product_images_df.iterrows():
                path = row['image_path']
                
                view_type = 0  
                if '_1_front' in path:
                    view_type = 0
                elif '_2_side' in path:
                    view_type = 1
                elif '_3_back' in path:
                    view_type = 2
                elif '_4_full' in path:
                    view_type = 3
                product_id_to_info[row['product_id']] = {'path': path, 'view_type': view_type}
           
            image_tensors = []
            view_types = []
            for pid in product_ids.cpu().numpy():
                if pid in product_id_to_info:
                    info = product_id_to_info[pid]
                    img_path = info['path']
                    if os.path.exists(img_path):
                        try:
                            img = Image.open(img_path).convert('RGB')

                            img_tensor = transform(img)
                            image_tensors.append(img_tensor)
                            view_types.append(info['view_type'])
                            logger.debug(f"Successfully loaded image for product {pid}: {img_path}")
                            
                        except Exception as e:
                            logger.error(f"Error loading image for product {pid}: {e}")
                            image_tensors.append(torch.zeros(3, 224, 224))
                            view_types.append(0)
                    else:
                        logger.warning(f"Image path does not exist for product {pid}: {img_path}")
                        image_tensors.append(torch.zeros(3, 224, 224))
                        view_types.append(0)

                else:
                    logger.warning(f"No image mapping for product {pid}")
                    image_tensors.append(torch.zeros(3, 224, 224))
                    view_types.append(0)
            
            image_batch = torch.stack(image_tensors).to(user_emb.device)
            view_batch = torch.tensor(view_types).to(user_emb.device)
            
            base_image_emb = self.image_encoder(image_batch)
            view_emb = self.view_embedding(view_batch)
            
            image_emb = self.style_projection(base_image_emb + view_emb)
        else:
            image_emb = torch.zeros(product_emb.shape[0], product_emb.shape[1]).to(user_emb.device)
        
        if isinstance(text_batch, list) and len(text_batch) > 0:
            text_features = self.text_encoder.encode(text_batch, convert_to_tensor=True).to(user_emb.device)
            text_emb = self.text_proj(text_features)
        else:
            text_emb = torch.zeros(product_emb.shape[0], product_emb.shape[1]).to(user_emb.device)
        
        cf_emb = user_emb * product_emb 
        combined = torch.cat([cf_emb, image_emb, text_emb], dim=-1) 
        return self.fusion(combined)
