# **Spotify Data Engineering Project (ETL on AWS)**  

## **Overview**  
This project builds an end-to-end **ETL (Extract, Transform, Load) pipeline** using **AWS** to analyze data from 4 global artists -- [Taylor Swift, Drake, Coldplay and The Weeknd] spanning across Pop, Hip-Hop, Rock, and R&B genres.  

The pipeline automates the **extraction, transformation, and storage** of **Spotify artist, album, and song data**,  making it queryable using **AWS Athena** for analysis.

---

## **Architecture Overview**  
The pipeline follows the **ETL (Extract, Transform, Load) process**, as illustrated below:  

![ETL Architecture Diagram](/Architecture_Diagram.png)  

### **1. Extract Phase**  
- **Data Source:** The **Spotify API** provides metadata about songs, albums, and artists.
- **AWS CloudWatch Events:** Triggers the extraction Lambda function on a daily schedule (rate(1 day)).  
- **AWS Lambda (Data Extraction):**  
  - A Lambda function (`spotify_api_data_extract`) fetches **raw JSON data** from Spotify.  
  - This function runs at scheduled intervals, triggered by **Amazon CloudWatch Events**.  
  - Extracted data is stored in an **S3 bucket (`raw_data/to_process/`)**.  

### **2. Transformation Phase**  
- **AWS Lambda (Data Transformation):**  
  - A second Lambda function (`spotify_transformtion_load`) is triggered when new raw data is added to S3.  
  - It processes the raw JSON, extracts key fields (e.g., song name, artist, album, popularity), and converts them into **structured CSV files**.  
  - The transformed data is stored in a separate **S3 bucket (`transformed_data`)**.  

### **3. Load Phase**  
- **AWS Glue Crawler:**  
  - Scans the transformed **CSV files** in S3.  
  - Infers schemas dynamically and creates tables in the **AWS Glue Data Catalog**.  
- **AWS Glue Data Catalog:**  
  - Stores metadata about the tables for easy querying.  
- **AWS Athena:**  
  - Connects to the Glue tables to enable **SQL-based querying** of the transformed data.  

---

## **Tech Stack & AWS Services Used**  
✅ **Python** – Data extraction, transformation (**Spotipy API, Pandas**)  
✅ **AWS Lambda** – Serverless functions for ETL processing  
✅ **AWS S3** – Data storage (**Raw & Transformed**)  
✅ **AWS CloudWatch** – Event-based triggers for automation  
✅ **AWS Glue** – Schema inference & table creation  
✅ **AWS Athena** – Querying transformed data using SQL  

---

## **Data Analysis & Use Cases**  
Using **AWS Athena**, I can perform queries such as:  
- Finding the most **popular songs** and **artists**.  
- Analyzing **album trends** over time.  
- Identifying **streaming patterns** based on song release years.  

---

## **Next Steps & Future Enhancements**  
🔹 **Dashboarding** – Build interactive visualizations using **Power BI** or **Tableau**.  
🔹 **Data Quality Checks** – Implement validation layers to ensure data consistency.  
🔹 **Cost & Performance Optimization** – Explore AWS Glue job optimizations and partitioning strategies.  

---

## **Conclusion**  
This project demonstrates how **AWS serverless technologies** can be leveraged to build a scalable **ETL pipeline**  
for **Spotify data analysis**. By automating data ingestion, transformation, and storage,  
it provides a powerful foundation for querying **streaming music insights** efficiently.

---

Let me know if you'd like any refinements! 🚀
