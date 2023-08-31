import pandas as pd 
import plotly.express as px
import streamlit as st 

st.set_page_config(page_title="Supermarket Sales",page_icon=":bar_chart",layout="wide")


df=pd.read_csv("saledata.csv")
#df.columns=df.columns.str.replace(" ","")

st.sidebar.header("Please choose the criteria")
city=st.sidebar.multiselect("Select City",
                         options=df["City"].unique(),
                         default=df["City"].unique()[:2])
                        

product=st.sidebar.multiselect("Select product line",
                         options=df["Product_line"].unique(),
                         default=df["Product_line"].unique()[:2])

customer=st.sidebar.multiselect("Select Customer_type",
                         options=df["Customer_type"].unique(),
                         default=df["Customer_type"].unique()[:2])

branch=st.sidebar.multiselect("Select Branch",
                         options=df["Branch"].unique(),
                         default=df["Branch"].unique()[:3])

                        
st.title(":bar_chart:2019 Sales Dashboard") 

totaloverall=df["Total"].sum()


item=df["Product_line"].nunique()

a,b=st.columns(2)

with a:
    st.subheader("Total Overall:")
    st.subheader(f"US $ {totaloverall}")
    
    
    
with b:
    st.subheader("Total number of product line:")
    st.subheader(f" {item}")
    
var=[city,customer,product,branch]
for x in var:
    if x==city and len(city)==0:
       city=df["City"]
    if x==product and len(product)==0:
       product=df["Product_line"]
    if x==customer and len(customer)==0:
       customer=df["Customer_type"]
    if x==branch and len(branch)==0:
       branch=df["Branch"]
      
    
df_selection=df.query("Product_line==@product and City==@city and Customer_type==@customer and Branch==@branch")

sales_by_product=df_selection.groupby("Product_line")["Total"].sum().sort_values(ascending=False)

barchart=px.bar(
sales_by_product, x=["Total"],y=sales_by_product.index,orientation="h",title="<b>Sales Bar Chart by Product line</b>",template="plotly_white",
)  
barchart.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

sales_by_city=df_selection.groupby("City")["Total"].sum().sort_values(ascending=False)

barchart_city=px.bar(
sales_by_city, y=["Total"],x=sales_by_city.index,title="<b>Sales Bar Chart by City</b>",template="plotly_white",
)  


sales_by_customer_type=df_selection.groupby("Customer_type")["Total"].sum().sort_values(ascending=False)

piechart_customer_type=px.pie(
sales_by_customer_type,values=sales_by_customer_type.values,names=sales_by_customer_type.index,title="<b>Sales Pie Chart by Customer_type</b>",template="plotly_white",
)  
barchart.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

sales_by_branch=df_selection.groupby("Branch")["Total"].sum().sort_values(ascending=False)

piechart_branch=px.pie(
sales_by_branch,values=sales_by_branch.values,names=sales_by_branch.index,title="<b>Sales Pie Chart by branch</b>",template="plotly_white",
)  
barchart.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


chart_col1,chart_col2,chart_col3,chart_col4=st.columns(4)
chart_col1.plotly_chart(barchart,use_container_width=True)
chart_col2.plotly_chart(piechart_customer_type,use_container_width=True)
chart_col3.plotly_chart(barchart_city,use_container_width=True)
chart_col4.plotly_chart(piechart_branch,use_container_width=True)

col1,col2=st.columns(2)

value=df_selection.groupby("City")["Total"].sum()
linechart_city=px.line(
value, y=value.values,x=value.index,title="<b>Sales Line Chart by City</b>",template="plotly_white",
)
col1.plotly_chart(linechart_city,use_container_width=True) 

scatterchart_city=px.scatter(df_selection, y="Quantity",x="Total",title="<b>Sales  Scatter Chart by Quantity</b>",template="plotly_white",
)

col2.plotly_chart(scatterchart_city,use_container_width=True)
