import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import sqlite3


connection = sqlite3.connect("Köksglädje.db")
palette_color = sns.color_palette("bright")#declares the palette colour for the piecharts using seaborn

sales_total_query = '''SELECT Products.CategoryName as Kategori, SUM(PriceAtPurchase) as "Sammanlagd Försäljningsumma"
FROM TransactionDetails
JOIN Products on TransactionDetails.ProductID = Products.ProductID
GROUP BY Kategori
ORDER BY "Sammanlagd Försäljningsumma" DESC;'''

best_in_category_query = '''SELECT CategoryName as Kategori, StoreName as Butik, CategorySalesSum as "Sammanlagd Försäljningsumma" FROM(
SELECT Products.CategoryName, Stores.StoreName, SUM(PriceAtPurchase) as CategorySalesSum
FROM TransactionDetails
JOIN Products on TransactionDetails.ProductID = Products.ProductID
JOIN Transactions on TransactionDetails.TransactionID = Transactions.TransactionID
JOIN Stores on Transactions.StoreID = Stores.StoreID
GROUP BY Products.CategoryName, Stores.StoreName
ORDER BY CategorySalesSum DESC)
GROUP BY CategoryName'''

store_sales_query = '''SELECT Products.CategoryName as Kategori, Stores.StoreName as Butik, SUM(PriceAtPurchase) as "Sammanlagd Försäljningsumma", Transactions.TransactionDate as Datum
FROM TransactionDetails
JOIN Products on TransactionDetails.ProductID = Products.ProductID
JOIN Transactions on TransactionDetails.TransactionID = Transactions.TransactionID
JOIN Stores on Transactions.StoreID = Stores.StoreID
GROUP BY Kategori, Butik
ORDER BY "Sammanlagd Försäljningsumma" DESC'''

sales_total_df = pd.read_sql(sales_total_query, connection)
best_in_category_df = pd.read_sql(best_in_category_query, connection)
store_sales_df = pd.read_sql(store_sales_query, connection)
print(store_sales_df)
#store_sales_df['Datum'] = pd.to_datetime(store_sales_df['Datum'])


st.title("Köksglädje")
st.header("Analys av försäljning av köksprylar och föremål")
st.subheader("Total försäjning per kategori")
st.dataframe(sales_total_df)

figbarts, axbarts = plt.subplots()
sns.barplot(sales_total_df.reset_index(),
            x="Kategori", y="Sammanlagd Försäljningsumma",
            ax=axbarts, errorbar=None,
            palette="bright")
plt.xticks(rotation=45)
axbarts.grid(axis="y")
st.pyplot(figbarts)

#--------------------best in each category--------------------
st.subheader("Högst säljande butik i varje kategori")
st.dataframe(best_in_category_df, column_order=["Butik", "Sammanlagd Försäljningsumma"])

figbarbc, axbarbc = plt.subplots()
sns.barplot(best_in_category_df.reset_index(),
            x="Kategori", y="Sammanlagd Försäljningsumma",
            ax=axbarbc, errorbar=None,
            palette="bright")
plt.xticks(rotation=45)
axbarbc.grid(axis="y")
st.pyplot(figbarbc)


#--------------------stores per categori--------------------
st.subheader("Butiksprestande per kategori")

figbarsic, axbarsic = plt.subplots(figsize=(12, 8))
sns.barplot(store_sales_df.reset_index(),
            x="Kategori", y="Sammanlagd Försäljningsumma",
            hue="Butik", ax=axbarsic)
axbarsic.grid(axis="y")
st.pyplot(figbarsic)

#--------------------selector for barchart--------------------
st_category_select = store_sales_df.drop_duplicates(subset=['Kategori'])
st_category_select.sort_values('Kategori', inplace=True)
st_category = st.selectbox(label='Välj kategori',options=st_category_select['Kategori'])

stores_in_category_df = store_sales_df[store_sales_df['Kategori'] == st_category]
stores_in_category_df.sort_values('Butik', inplace=True)
stores_in_category_df['Procent'] = (stores_in_category_df['Sammanlagd Försäljningsumma'] / sum(stores_in_category_df['Sammanlagd Försäljningsumma'])) * 100

#--------------------barchart--------------------
figsic, axsic = plt.subplots()
sns.barplot(stores_in_category_df.reset_index(),
            x="Procent",
            y="Butik",
            ax=axsic,
            errorbar=None,
            palette="bright")
axsic.set_xticklabels([f'{x:.0f}%' for x in axsic.get_xticks()]) 
axsic.grid(axis="x")

st.pyplot(figsic)

#--------------------categori per store--------------------

st.subheader("Kategoriprestanda per butik")

store_sales_df['Procent'] = (store_sales_df['Sammanlagd Försäljningsumma'] / sum(store_sales_df['Sammanlagd Försäljningsumma'])) * 100

figbarcis, axbarcis = plt.subplots(figsize=(12, 8))
sns.barplot(store_sales_df.reset_index(),
            x="Kategori", y="Procent",
            hue="Butik", ax=axbarcis)
axbarcis.set_yticklabels([f'{x:.0f}%' for x in axbarcis.get_yticks()]) 
axbarcis.grid(axis="y")
st.pyplot(figbarcis)

#--------------------selector for barchart--------------------
st_store_select = store_sales_df.drop_duplicates(subset=['Butik'])
st_store_select.sort_values('Butik', inplace=True)
st_store = st.selectbox(label='Välj butik',
                        options=st_store_select['Butik'])

category_in_stores_df = store_sales_df[store_sales_df['Butik'] == st_store]
category_in_stores_df.sort_values('Kategori', inplace=True)
category_in_stores_df['Procent'] = (category_in_stores_df['Sammanlagd Försäljningsumma'] / sum(category_in_stores_df['Sammanlagd Försäljningsumma'])) * 100


#--------------------barchart--------------------

figcis, axcis = plt.subplots()
sns.barplot(category_in_stores_df.reset_index(),
            x="Kategori",
            y="Procent",
            ax=axcis,
            errorbar=None,
            palette="bright")
plt.xticks(rotation=45)
axcis.set_yticklabels([f'{x:.0f}%' for x in axcis.get_yticks()]) 
axcis.grid(axis="y")
st.pyplot(figcis)