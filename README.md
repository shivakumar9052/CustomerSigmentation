# Project Summary

Understanding customer behavior is critical for any business. In this project, I performed:

📊 Exploratory Data Analysis (EDA) to explore trends and transaction patterns
📦 RFM analysis to assign behavior-based scores to customers
🎯 Segmentation into categories like Champions, Loyal, At Risk, Lost
📈 Visualizations to present insights clearly and drive actionable strategies
🧰 Tools & Libraries Used

Python 3.11
Pandas, NumPy for data manipulation
Seaborn, Matplotlib for visualization
Jupyter Notebook for development
📂 Dataset

Source: UCI Repository - Online Retail Dataset
The dataset contains over 541,000 transactions from a UK-based online retailer between 2010 and 2011.

✅ Key Features of the Project

🔍 Exploratory Data Analysis (EDA)

Total spending and frequency per customer
Cancelled orders and basket size analysis
Revenue trends over time and by country
📊 RFM (Recency, Frequency, Monetary) Analysis

Recency: Days since last purchase
Frequency: Number of purchases
Monetary: Total amount spent
Quantile-based scoring system (1 to 5)
Customer segmentation based on combined RFM scores

Standardized RFM values
Elbow method to determine optimal k
Cluster labeling into:
Champions
Loyal
Potential Loyalists
At Risk
Lost
📈 Visualizations

Histograms, heatmaps, box plots
Monthly revenue trend
Top 10 spenders
Cluster distribution
Correlation heatmap
📌 How to Run This Project

Clone the repository

git clone https://github.com/your-username/customer-segmentation-rfm.git
cd customer-segmentation-rfm
Install dependencies

pip install -r requirements.txt
Run the Jupyter Notebook

jupyter notebook CustomerSegmentation.ipynb
📈 Output Highlights

Segmented over 4,000 customers
Identified high-value customers for targeted campaigns
Visual reports for business and marketing decisions
📚 References
Pandas Documentation
Seaborn Documentation
Matplotlib Documentation
