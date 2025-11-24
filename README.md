# Product Recommendation System
## 1. Introduction
### Goal:
This project develops a product recommendation system for an ecommerce platform. The system uses several recommendation techniques including collaborative filtering, content-based filtering, hybrid approach, and a multi-modal deep learning model to provide highly personalized product suggestions to users based on purchase history, browsing behavior, product metadata, images, and graph relationships. To demonstrate how these recommendation systems work, we use Streamlit to build a web store where users can log in, browse products, select a recommendation system type, add products to their cart, and make a purchase.
### Main Features
- **Collaborative Filtering**: Recommends products based on users with similar purchasing behavior.
- **Content-based Filtering**: Recommends products based on the attributes of the products the users interacted with.
- **Hybrid Approach**: Combines collaborative and content-based filtering for more robust recommendations, includes fallback with most popular products.
- **Multi-Modal Deep Learning**: Integrates user–item interactions, product images, text descriptions, and product–graph relationships into a unified multi-modal deep learning architecture for highly accurate recommendations.
- **Web Interface**: A web application built with Sreamlit for easy interaction and visualization of recommendations.
### General Workflow
The application simulates an ecommerce environment and allows users to log in with demo accounts through a Streamlit web interface. Product data, user interactions, and purchase history are generated from synthetic datasets for experimentation and demonstration purposes.
- User Interaction via Streamlit UI:
Users select a predefined demo account to simulate browsing and shopping behavior.
- Loading Simulated Data:
The system loads user information, product information, product images, interaction history, purchase history.
- Recommendation Engine Execution:
Users can choose among four recommendation modes: Collaborative Filtering, Content-Based Filtering, Hybrid Approach, Multi-Modal Deep Learning Model
- Ranking and Output Generation:
The recommendation scores are ranked and formatted into displayable product lists.
- Display on Streamlit UI:
Recommended products are shown with images, names of products, prices, rates and categories.  
**Note:** This project is a demonstration prototype. User accounts, interaction logs, and product data are simulated for experimentation and do not represent real commercial activity.
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
  - Prepare data set (3 file csv remain)
- Đào Minh Dũng: 16.5%
  - Convert design to code  
  - Responsible for the product display module
  - Responsible for displaying product images in the product listing
  - Responsible for the main interface / landing page UI
  - Responsible for the feedback interface
- Phạm Thu Hường: 16.5%
  - Prepare the slides for presentation 
  - Responsible for:
    - Post-processing and Result Visualization
    - Running the Recommendation Algorithms
    - Fetching User-Interacted Products
## 3. Instructions for installing and running the program
### Python version
Python 3.10
### Required libraries
Install libraries from file 'requirements.txt'
```bash
pip install -r requirement
```
### Running the Application
1. Clone repository
```bash
git clone https://github.com/miintd/Group_3_DSEB_66B_Product_Recommendation_System.git
```
3. Run Streamlit app
```bash
streamlit run web.py
```
## 4. App user manual
First, user enter username and password to login. If you do not have an account, click register and fill these information: username, email and password.  
Then, the screen display the selection box for the suggested algorithm and trending items, include their image, name, price, rating and category. If you already have an account, select a recommendation method (collaborative, content-based, hybrid, or multi-modal). If you are new user, our system recommend trending items. You can click 'View detail' to see more information and add to your shopping cart or your favorite.  
After choosing a recommendation method, the screen will display a list of suggested products based on that algorithm. Then the user can browse through each product and select the product they like and want to buy.  
The shopping cart will be displayed on the left side of the screen and you can click the "checkout" button. However, we have not built a complete checkout page yet, as this is just a web simulation of how the 4 recommendation algorithms work.  
Finally, users can send feedback to us so we can improve our website for better experiences.
