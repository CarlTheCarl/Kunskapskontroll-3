import sqlite3
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns


connection = sqlite3.connect("Köksglädje.db")
palette_color = sns.color_palette('bright')#declares the palette colour for the piecharts using seaborn

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

figbarts, axbarts = plt.subplots()
sns.barplot(sales_total_df.reset_index(),
            x="Kategori", y="Sammanlagd Försäljningsumma",
            ax=axbarts, errorbar=None)
plt.xticks(rotation=45)
st.pyplot(figbarts)

#best in each category
st.subheader("Högst säljande butik i varje kategori")
st.dataframe(best_in_category_df)

figbarbc, axbarbc = plt.subplots()
sns.barplot(best_in_category_df.reset_index(),
            x="Kategori", y="Sammanlagd Försäljningsumma",
            ax=axbarbc, errorbar=None)
plt.xticks(rotation=45)
st.pyplot(figbarbc)

#stores per categori
st.subheader("Butiksprestande per kategori")

figbarsic, axbarsic = plt.subplots(figsize=(12, 8))
sns.barplot(store_sales_df.reset_index(),
            x="Kategori", y="Sammanlagd Försäljningsumma",
            hue="Butik", ax=axbarsic)
st.pyplot(figbarsic)

#selector for piechart
st_category_select = store_sales_df.drop_duplicates(subset=['Kategori'])
st_category = st.selectbox(label='Välj kategori',options=st_category_select['Kategori'])

stores_in_category_df = store_sales_df[store_sales_df['Kategori'] == st_category]

#piechart
figsic, axsic = plt.subplots()
axsic.pie(stores_in_category_df['Sammanlagd Försäljningsumma'],
          labels=stores_in_category_df['Butik'],
          colors=palette_color,
          autopct='%1.1f%%',
          startangle=90)
axsic.axis('equal')

plt.show()  

st.pyplot(figsic)

st.subheader("Kategoriprestanda per butik")

#selector for piechart
st_store_select = store_sales_df.drop_duplicates(subset=['Butik'])
st_store = st.selectbox(label='Välj butik',
                        options=st_store_select['Butik'])

category_in_stores_df = store_sales_df[store_sales_df['Butik'] == st_store]

#piechart
figcis, axcis = plt.subplots()
axcis.pie(category_in_stores_df['Sammanlagd Försäljningsumma'],
          labels=category_in_stores_df['Kategori'],
          colors=palette_color,
          autopct='%1.1f%%',
          startangle=90)
axcis.axis('equal')

st.pyplot(figcis)