# Clueless: The Ultimate Outfit Explorer Web Application

Welcome to our project!

### Project Overview
Clueless Outfit Explorer and Manager is a web application that caters to many user personas; however its main functionality is for the general consumer to view, manage, organize, and add to a digital wardrobe for easy accessibility and planning. With an intuitive UI, the user can explore for outfit inspiration, view and add clothing items to closets organized by the user, and build/view outfits of clothing items for future wardrobe planning. Along with the general consumer, Clueless allows for brands to view data on consumer interests based on what consumers save to their digital wishlists and closets. This solves potential user indecisiveness, saves time on outfit planning, reduces overconsumption as the user knows exactly what is in their closet, and allows for brands to have insight on what the general consumer wants, eliminating potential deadstock.

### Project Links & Deliverables:
- **Link to Demo Video**: https://drive.google.com/file/d/1pn-LhD3tTi--uOr50C_lu-4Ff4sPd620/view?usp=sharing
- **Link to Project Submission Doc**: https://github.com/averyneuner/25F-Project-Clueless.git

### Key Personas:
1) General Consumer (Rachel)
2) Business/Brand (Rebecca)
3) Data Analyst (Alison)
4) Administration (Owen)

### Key Elements: 
1) **Smart Digital Closet & Outfit Planning (Consumer Focus)**: 

   - **Enables**: Users to digitize, organize, view their wardrobe, and plan outfits using an intuitive UI and leveraging their existing items.

   - **Addresses**: Need for easy organization, quick outfit planning, and exploration of new clothing combinations.

   - **Pages**:
      
      - 00_Consumer_Home.py
      - 00_Consumer_Profile.py
      - 00_Consumer_Closet.py
      - 00_Consumer_Wishlist.py
      - 01_Consumer_Clothing_Items.py
      - 01_Consumer_Outfits.py
      - 01_Consumer_Profile_Editing.py


2) **Match Wishlist to Business Pipeline (Business Focus)**:

   - **Enables**: Linking business wishlists (desired items) directly to business inventory and facilitating intentional shopping.

   - **Addresses**: Need to reduce dead stock, market effectively, and ensure business is stocking items users actually want and need.

   - **Pages**:
      
      - _36_Business_Home.py
      - 37_Business_Add_Item.py
      - 38_Business_Inventory.py
      - 39_Business_Wishlist.py
      - 40_Business_Notifications.py

3) **Data-Driven Fashion Insights (Analyst Focus)**:

   - **Enables**: Collection and analysis of user data (closet contents & wishlists) to reveal emerging fashion trends, popular items, and aesthetic preferences.

      - **Addresses**: Need for a centralized, quantitative view of consumer interests to advise brands on future catalogs.

      - **Pages**:
         
         - 31_Data_Analyst_Home.py
         - 32_Data_Analyst_Brands.py
         - 33_Data_Analyst_Trending.py
         - 34_Data_Analyst_Wish_List.py
         - 35_Data_Analyst_Closet_Staples.py

4) **Centralized System & Vendor Administration (Admin Focus)**:

   - **Enables**: System administrators to manage user and business accounts, monitor system performance (lag/capacity), and ensure data integrity.

   - **Addresses**: Need for efficient management of the platform, including: workflows, security, and smooth operation.

   - **Pages**:
      
      - 20_Admin_Home.py
      - 21_ML_Model_Mgmt.py
      - 22_Dashboard_Overview.py
      - 23_Business_Client_Mgmt.py
      - 24_Wishlist_Match.py
      - 25_Notif_Alert.py
      - 26_Setting_Permission.py
      - 27_Client_Prof.py
      - 28_Add_Client.py

## Built With
* MySQL and Docker Compose for backend and integration
* Streamlit & Python for frontend

## Authors/Contributors
1) Avery Neuner
2) Arvind Kashyap 
3) Chayapa Nakasiri
4) Isha Madhusudhan 
5) Varsha Baskar

*****
## Structure of the Repo

- This repository is organized into five main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
  - `./datasets` - folder for storing datasets

- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database. 

*****
## Docker and Viewing the Application

1) Have Docker Desktop installed and running
2) Clone this project repository (ideally in VSCode)
3) Within the terminal of VSCode, run: 

   ```docker compose up --build -d```
   
   This should set up the containers and make them run. 
   There should be 3 docker containers runnning: the web-app, the web-api, and mysql-db. 

   To check if they're running run this in terminal:

   ```docker compose ps```

   Helpful information for docker compose containers can be found in: docker-compose.yaml


4) Once docker is up and running, you can view our web application with this link in your browser:

   https://localhost:8501