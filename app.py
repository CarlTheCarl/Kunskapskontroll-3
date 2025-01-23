import sqlite3
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

connection = sqlite3.connect("Köksglädje.db")

sales_total_query = '''SELECT Products.CategoryName as Kategori, SUM(PriceAtPurchase) as "Sammanlagd Försäljningsumma"
FROM TransactionDetails
JOIN Products on TransactionDetails.ProductID = Products.ProductID
GROUP BY Kategori
ORDER BY "Sammanlagd Försäljningsumma" DESC;'''

best_in_category_query = '''SELECT CategoryName as Kategori, StoreName, CategorySalesSum as "Sammanlagd Försäljningsumma" FROM(
SELECT Products.CategoryName, Stores.StoreName, SUM(PriceAtPurchase) as CategorySalesSum
FROM TransactionDetails
JOIN Products on TransactionDetails.ProductID = Products.ProductID
JOIN Transactions on TransactionDetails.TransactionID = Transactions.TransactionID
JOIN Stores on Transactions.StoreID = Stores.StoreID
GROUP BY Products.CategoryName, Stores.StoreName
ORDER BY CategorySalesSum DESC)
GROUP BY CategoryName'''

store_sales_query = '''SELECT Products.CategoryName as Kategori, Stores.StoreName as Butik, SUM(PriceAtPurchase) as "Sammanlagd Försäljningsumma"
FROM TransactionDetails
JOIN Products on TransactionDetails.ProductID = Products.ProductID
JOIN Transactions on TransactionDetails.TransactionID = Transactions.TransactionID
JOIN Stores on Transactions.StoreID = Stores.StoreID
GROUP BY Kategori, Butik
ORDER BY "Sammanlagd Försäljningsumma" DESC'''

sales_total_df = pd.read_sql(sales_total_query, connection)
best_in_category_df = pd.read_sql(best_in_category_query, connection)
store_sales_df = pd.read_sql(store_sales_query, connection)

st.title("Köksglädje")
st.header("Analys av försäljning av köksprylar och föremål")
st.subheader("Total försäjning per kategori")
st.dataframe(sales_total_df)

st.bar_chart(sales_total_df,x="Kategori", y="Sammanlagd Försäljningsumma")

st.subheader("Högst säljande butik i varje kategori")
st.dataframe(best_in_category_df)

st.bar_chart(best_in_category_df,x="Kategori", y="Sammanlagd Försäljningsumma")

st.subheader("Butiksprestande per kategori")

st.bar_chart(store_sales_df, x="Kategori", y="Sammanlagd Försäljningsumma", stack=False)

st_category_select = store_sales_df.drop_duplicates(subset=['Kategori'])
st_category = st.selectbox(label='Välj kategori',options=st_category_select['Kategori'])

stores_in_category_df = store_sales_df[store_sales_df['Kategori'] == st_category]

figsic, axsic = plt.subplots()
axsic.pie(stores_in_category_df['Sammanlagd Försäljningsumma'],
          labels=stores_in_category_df['Butik'],
          autopct='%1.1f%%',
          startangle=90)
axsic.axis('equal')

st.pyplot(figsic)

st.subheader("Kategoriprestanda per butik")

st_store_select = store_sales_df.drop_duplicates(subset=['Butik'])
st_store = st.selectbox(label='Välj butik',
                        options=st_store_select['Butik'])

category_in_stores_df = store_sales_df[store_sales_df['Butik'] == st_store]

figcis, axcis = plt.subplots()
axcis.pie(category_in_stores_df['Sammanlagd Försäljningsumma'],
          labels=category_in_stores_df['Kategori'],
          autopct='%1.1f%%',
          startangle=90)
axcis.axis('equal')

st.pyplot(figcis)