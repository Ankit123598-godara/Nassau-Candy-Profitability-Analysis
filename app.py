
import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    page_icon='🍬',
    layout='wide')

@st.cache_data
def load_data():
    df=pd.read_csv("Nassau Candy Distributor.csv")
    df['Order Date']=pd.to_datetime(df['Order Date'],format='mixed',
    dayfirst=True,errors='coerce')
    return df

df=load_data()

st.title("🍬 Nassau Candy Distributor")
st.subheader("Product Line Profitability and Margin Performance Analysis")

st.sidebar.header("Dashboard Filters")

divisions=['All']+sorted(df['Division'].dropna().unique().tolist())
selected_division=st.sidebar.selectbox('Select Division',divisions)

products=['All']+sorted(df['Product Name'].dropna().unique().tolist())
selected_product=st.sidebar.selectbox('Select Product',products)

data=df.copy()

if selected_division!='All':
    data=data[data['Division']==selected_division]

if selected_product!='All':
    data=data[data['Product Name']==selected_product]

total_sales=data['Sales'].sum()
total_cost=data['Cost'].sum()
total_profit=data['Gross Profit'].sum()

margin=(total_profit/total_sales*100) if total_sales else 0

c1,c2,c3,c4=st.columns(4)

c1.metric("Total Sales",f"${total_sales:,.2f}")
c2.metric("Total Cost",f"${total_cost:,.2f}")
c3.metric("Gross Profit",f"${total_profit:,.2f}")
c4.metric("Gross Margin",f"{margin:.2f}%")

st.divider()

st.header("Product Profitability")
product_data=(
    data.groupby('Product Name',as_index=False).agg(
        Sales=('Sales','sum'),
        Cost=('Cost','sum'),
        Gross_Profit=('Gross Profit','sum')))

product_data['Margin(%)']=(product_data['Gross_Profit']/product_data['Sales'].replace(0,pd.NA)*100).fillna(0)

fig1=px.bar(
    product_data.sort_values('Gross_Profit',ascending=False),
    x='Product Name',
    y='Gross_Profit',
    title='Gross Profit by Product',
    color='Gross_Profit')
st.plotly_chart(fig1,use_container_width=True)

st.header('Division Performance')
division_data=(
    data.groupby('Division',as_index=False).agg(
        Sales=('Sales','sum'),
        Gross_Profit=('Gross Profit','sum')))

fig2=px.bar(
    division_data,
    x='Division',
    y='Gross_Profit',
    title='Gross Profit by Division',
    color='Division')
st.plotly_chart(fig2,
                use_container_width=True)

st.header('Monthly Sales Trend')

monthly_data= data.dropna(subset=['Order Date']).copy()
monthly_data['Month']=(
    monthly_data['Order Date'].dt.to_period("M").astype(str))

monthly_sales=(
    monthly_data.groupby('Month',as_index=False)['Sales'].sum())

fig3=px.line(
    monthly_sales,
    x='Month',
    y='Sales',
    markers=True,
    title='Monthly Sales')
st.plotly_chart(fig3,
                use_container_width=True)

st.header('Product Summary')
st.dataframe(
    product_data.sort_values('Gross_Profit',ascending=False),
    use_container_width=True)

st.download_button(
    label="Download Product Report",
    data=product_data.to_csv(index=False).encode("utf-8"),
    file_name='product_profitability_report.csv',mime='text/csv')
                             
