# Product Recommendation System
## 1. Introduction
### Goal:
This project develops a product recommendation system for an ecommerce platform. The system uses several recommendation techniques including collaborative filtering, content-based filtering, hybrid approach, and a multi-modal deep learning model to provide highly personalized product suggestions to users based on purchase history, browsing behavior, product metadata, images, and graph relationships.
### Main Features
- **Collaborative Filtering**: Recommends products based on users with similar purchasing behavior.
- **Content-based Filtering**: Recommends products based on the attributes of the products the users interacted with.
- **Hybrid Approach**: Combines collaborative and content-based filtering for more robust recommendations, includes fallback with most popular products.
- **Multi-Modal Deep Learning**: Integrates user–item interactions, product images, text descriptions, and product–graph relationships into a unified multi-modal deep learning architecture for highly accurate recommendations.
- **Web Interface**: A web application built with Sreamlit for easy interaction and visualization of recommendations.
### General Workflow
## 2. Task Allocation
- Nguyễn Đức Quang (Leader): 17.5%
  - Assign task for team members
  - Prepare dataset
  - Building Multi-Modal Deep Learning Model for recommending products
  - Building a user authentication interface (login and registration) together with the functionality for adding products to the shopping cart
  - Responsible for the login interface
- Nguyễn Thị Diễm My (Vice Leader): 16.5%
  - Find the idea for the project
  - Building 3 recommendation systems: Collaborative Filtering, Content-based Filtering, Hybrid Approach
  - Prepare the slides for presentation
- Nguyễn Trung Tùng: 16.5%
  - Prepare data set (browsing_history_expanded.csv, products_expanded.csv)
  - Prepare the slides for the presentation
- Lê Cẩm Tú: 16.5%
  - Find the idea for web design 
  -Prepare data set (3 file csv remain)
- Đào Minh Dũng: 16.5%
  -Convert design to code
  -Responsible for the product display module
  -Responsible for displaying product images in the product listing
  -Responsible for the main interface / landing page UI
  -Responsible for the feedback interface
- Phạm Thu Hường: 16.5%
  -Responsible for:
    -Post-processing and Result Visualization
    -Running the Recommendation Algorithms
    -Fetching User-Interacted Products
  -Prepare the slides for presentation 
## 3. Instructions for installing and running the program
### Prerequisites
- Python 3.
- PyTorch
- Streamlit
- Sentence Transformers
- PyTorch Geometric
- Torchvision
- PIL
