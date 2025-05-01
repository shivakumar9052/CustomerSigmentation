
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

raw_df = pd.read_excel('/Users/mshivakumar/Programming Files/INT375DSToolbox/Online Retail.xlsx')

df = raw_df.copy()
df.head()
df.info()

df = df.dropna(subset = ['CustomerID'])   # remove rows without customer ID
df['CustomerID'] = df['CustomerID'].astype(int)
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']  # Added a colmun of Amount spent for each purchase
df['IsCanceled'] = df['InvoiceNo'].astype(str).str.startswith('C')
df.info()

customer_spending = df.groupby('CustomerID')['TotalPrice'].sum().reset_index().rename(columns={'TotalPrice': 'TotalSpent'})
customer_spending

orders_per_customer = df.groupby('CustomerID')['InvoiceNo'].nunique().reset_index().rename(columns={'InvoiceNo': 'TotalOrders'})
orders_per_customer

plt.figure(figsize=(10,6))
ax = sns.histplot(orders_per_customer['TotalOrders'], bins=30, kde=False, color='mediumseagreen')
plt.yscale('log')


for rect in ax.patches:
    height = rect.get_height()
    if height > 0:
        ax.text(
            rect.get_x() + rect.get_width()/2,
            height,
            f"{int(height)}",
            ha='center',
            va='bottom',
            fontsize=8
        )

plt.title('Distribution of Orders per Customer')
plt.xlabel('Total Orders')
plt.ylabel('Number of Customers (Log Scale)')
plt.tight_layout()
plt.show()

df_clean = df[~df['InvoiceNo'].astype(str).str.startswith('C')] #Dataframe without cancled data
basket_size = df_clean.groupby('InvoiceNo')['Quantity'].sum().reset_index().rename(columns={'Quantity': 'BasketSize'})
basket_size

top_customers = customer_spending.nlargest(10, 'TotalSpent')
plt.figure(figsize=(10,6))
ax = sns.barplot(
    data=top_customers,
    x='CustomerID',
    y='TotalSpent',
    palette='magma',
    order=top_customers.sort_values('TotalSpent', ascending=False)['CustomerID'].astype(str)
)

for bar in ax.patches:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height, f'£{height:,.0f}', ha='center', va='bottom', fontsize=9)

plt.title('Top 10 Customers by Total Spending')
plt.xlabel('Customer ID')
plt.ylabel('Total Spending (£)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

canceled_orders = df[df['IsCanceled']].groupby('CustomerID')['InvoiceNo'].nunique().reset_index().rename(columns={'InvoiceNo': 'CanceledOrders'})
canceled_orders

plt.figure(figsize=(10,6))
ax = sns.histplot(basket_size['BasketSize'], bins=50, color='skyblue')
plt.yscale('log')

for rect in ax.patches:
    height = rect.get_height()
    if height > 0:
        ax.text(
            rect.get_x() + rect.get_width()/2,
            height,
            f"{int(height)}",
            ha='center',
            va='bottom',
            fontsize=8)

plt.title('Distribution of Basket Size per Order (Log Scale)')
plt.xlabel('Number of Items per Order')
plt.ylabel('Number of Orders (Log Scale)')
plt.tight_layout()
plt.show()

from functools import reduce
dfs = [customer_spending, orders_per_customer, canceled_orders]
customer_behavior = reduce(lambda left, right: pd.merge(left, right, on='CustomerID', how='outer'), dfs)

customer_behavior['CanceledOrders'] = customer_behavior['CanceledOrders'].fillna(0).astype(int)

customer_behavior = customer_behavior.dropna()

customer_behavior.head()

plt.figure(figsize=(10,6))
ax = sns.histplot(customer_behavior['CanceledOrders'], bins=20, kde=False, color='salmon')
plt.yscale('log')

max_height = max([rect.get_height() for rect in ax.patches])
plt.ylim(1, max_height * 1.5)

for rect in ax.patches:
    height = rect.get_height()
    if height > 0:
        plt.text(
            rect.get_x() + rect.get_width()/2,
            height,
            f"{int(height)}",
            ha='center',
            va='bottom',
            fontsize=9)

plt.title('Distribution of Canceled Orders per Customer (Log Scale)')
plt.xlabel('Number of Canceled Orders')
plt.ylabel('Number of Customers (Log Scale)')
plt.tight_layout()
plt.show()

df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')

monthly_revenue = df.groupby('InvoiceMonth')['TotalPrice'].sum().reset_index()
monthly_revenue['InvoiceMonth'] = monthly_revenue['InvoiceMonth'].astype(str)

plt.figure(figsize=(14,6))
sns.lineplot(data=monthly_revenue, x='InvoiceMonth', y='TotalPrice', marker='o', color='darkblue')
plt.title('Monthly Revenue Over Time')
plt.xlabel('Month')
plt.ylabel('Revenue (£)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

country_revenue = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=country_revenue.values, y=country_revenue.index, palette='crest')
plt.title('Top 10 Countries by Revenue')
plt.xlabel('Total Revenue (£)')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

country_avg_spending = df.groupby('Country').agg({'TotalPrice': 'sum', 'InvoiceNo': 'nunique'})
country_avg_spending['AvgSpendingPerOrder'] = country_avg_spending['TotalPrice'] / country_avg_spending['InvoiceNo']
top_avg_spending = country_avg_spending.sort_values('AvgSpendingPerOrder', ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_avg_spending['AvgSpendingPerOrder'], y=top_avg_spending.index, palette='flare')
plt.title('Top 10 Countries by Avg Spending per Order')
plt.xlabel('Avg Spending per Order (£)')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

df = raw_df.copy()
df = df.dropna(subset=['CustomerID'])
df['TotalPrice'] = df['UnitPrice'] * df['Quantity']

reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (reference_date - x.max()).days, # Recency : less is better
    'InvoiceNo': 'nunique', # Frequency : more is better
    'TotalPrice': 'sum' # Monetary : more is better
    }).reset_index()
rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels = [5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method ='first'), 5, labels = [1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels = [1, 2, 3, 4, 5])

rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis = 1).astype(int)
rfm.head()

plt.figure(figsize=(11,6))
sns.histplot(rfm['RFM_Score'], bins=10, kde = True, color='dodgerblue')
plt.title('Distribution of RFM Scores')
plt.xlabel('RFM Score')
plt.ylabel('Number of Customers')
plt.xticks(range(rfm['RFM_Score'].min(), rfm['RFM_Score'].max() + 1))
plt.yticks(range(0, 900, 100))
plt.tight_layout()
plt.show()

def segment_customer(row):
    r = int(row['R_Score'])
    f = int(row['F_Score'])
    score = row['RFM_Score']

    if score >= 13:
        return 'Champions'
    elif score >= 10:
        return 'Loyal'
    elif r >= 4 and f >= 3:
        return 'Potential Loyalist'
    elif r >= 3 and f <= 2:
        return 'Need Attention'
    elif r <= 2 and f >= 3:
        return 'At Risk'
    elif r == 1 and f == 1:
        return 'Lost'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

segment_counts = rfm['Segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'Count']

plt.figure(figsize=(10, 6))
sns.barplot(data=segment_counts, x='Segment', y='Count', palette='Set2')
plt.title('Customer Segments Count')
plt.xlabel('Customer Segment')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


rfm_for_clustering = rfm[['Recency', 'Frequency', 'Monetary']]

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_for_clustering)


inertia = []  
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(rfm_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(K_range, inertia, marker='o', linestyle='--', color='teal')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia (Sum of Squared Distances)')
plt.title('Elbow Method - Optimal k')
plt.xticks(K_range)
plt.grid(True)
plt.tight_layout()
plt.show()
