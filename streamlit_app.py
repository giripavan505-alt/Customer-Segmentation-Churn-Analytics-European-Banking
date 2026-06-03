import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Customer Segmentation & Churn Pattern Analytics",
    layout="wide"
)
st.title("Customer Segmentation & Churn Pattern Analytics in European Banking")
# Load Dataset
df = pd.read_csv("European_Bank.csv")
# -----------------------------
# Data Preparation
# -----------------------------
# Age Segments
df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[0, 30, 45, 60, 100],
    labels=["<30", "30-45", "46-60", "60+"]
)
# Credit Score Segments
df["CreditBand"] = pd.cut(
    df["CreditScore"],
    bins=[0, 600, 750, 1000],
    labels=["Low", "Medium", "High"]
)
# Tenure Segments
df["TenureGroup"] = pd.cut(
    df["Tenure"],
    bins=[-1, 3, 7, 10],
    labels=["New", "Mid-Term", "Long-Term"]
)
# Balance Segments
median_balance = df["Balance"].median()
def balance_segment(x):
    if x == 0:
        return "Zero Balance"
    elif x <= median_balance:
        return "Low Balance"
    else:
        return "High Balance"
df["BalanceSegment"] = df["Balance"].apply(balance_segment)
# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")
country = st.sidebar.multiselect(
    "Select Geography",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
)
filtered_df = df[df["Geography"].isin(country)]
# -----------------------------
# KPI Section
# -----------------------------
st.subheader("Key Performance Indicators")
total_customers = len(filtered_df)
churn_rate = round(filtered_df["Exited"].mean() * 100, 2)
high_value = filtered_df[
    filtered_df["Balance"] > filtered_df["Balance"].quantile(0.75)
]
high_value_churn = round(
    high_value["Exited"].mean() * 100, 2
)
active_rate = round(
    filtered_df["IsActiveMember"].mean() * 100, 2
)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", total_customers)
col2.metric("Overall Churn Rate", f"{churn_rate}%")
col3.metric("High-Value Churn Ratio", f"{high_value_churn}%")
col4.metric("Active Customers", f"{active_rate}%")
st.divider()
# -----------------------------
# Geography-wise Churn
# -----------------------------
st.subheader("Geography-wise Churn Analysis")
geo_churn = (
    filtered_df.groupby("Geography")["Exited"]
    .mean()
    .reset_index()
)
fig_geo = px.bar(
    geo_churn,
    x="Geography",
    y="Exited",
    color="Geography",
    title="Churn Rate by Geography"
)
st.plotly_chart(fig_geo, use_container_width=True)
# -----------------------------
# Age Segment Analysis
# -----------------------------
st.subheader("Age Group Churn Analysis")
age_churn = (
    filtered_df.groupby("AgeGroup")["Exited"]
    .mean()
    .reset_index()
)
fig_age = px.bar(
    age_churn,
    x="AgeGroup",
    y="Exited",
    title="Churn Rate by Age Group"
)
st.plotly_chart(fig_age, use_container_width=True)
# -----------------------------
# Tenure Analysis
# -----------------------------
st.subheader("Tenure Group Churn Analysis")
tenure_churn = (
    filtered_df.groupby("TenureGroup")["Exited"]
    .mean()
    .reset_index()
)
fig_tenure = px.bar(
    tenure_churn,
    x="TenureGroup",
    y="Exited",
    title="Churn Rate by Tenure Group"
)
st.plotly_chart(fig_tenure, use_container_width=True)
# -----------------------------
# Credit Score Analysis
# -----------------------------
st.subheader("Credit Score Band Analysis")
credit_churn = (
    filtered_df.groupby("CreditBand")["Exited"]
    .mean()
    .reset_index()
)
fig_credit = px.bar(
    credit_churn,
    x="CreditBand",
    y="Exited",
    title="Churn Rate by Credit Score Band"
)
st.plotly_chart(fig_credit, use_container_width=True)
# -----------------------------
# Balance Segment Analysis
# -----------------------------
st.subheader("Balance Segment Churn Analysis")
balance_churn = (
    filtered_df.groupby("BalanceSegment")["Exited"]
    .mean()
    .reset_index()
)
fig_balance = px.bar(
    balance_churn,
    x="BalanceSegment",
    y="Exited",
    title="Churn Rate by Balance Segment"
)
st.plotly_chart(fig_balance, use_container_width=True)
# -----------------------------
# High Value Customer Explorer
# -----------------------------
st.subheader("High-Value Customer Churn Explorer")
threshold = st.slider(
    "Balance Threshold",
    int(df["Balance"].min()),
    int(df["Balance"].max()),
    100000
)
premium_customers = filtered_df[
    filtered_df["Balance"] >= threshold
]
st.write(
    f"Premium Customers Found: {len(premium_customers)}"
)
st.dataframe(
    premium_customers[
        [
            "CustomerId",
            "Geography",
            "Age",
            "Balance",
            "EstimatedSalary",
            "Exited"
        ]
    ]
)
# -----------------------------
# Gender Analysis
# -----------------------------
st.subheader("Gender-wise Churn")
gender_churn = (
    filtered_df.groupby("Gender")["Exited"]
    .mean()
    .reset_index()
)
fig_gender = px.pie(
    gender_churn,
    names="Gender",
    values="Exited",
    title="Gender Churn Distribution"
)
st.plotly_chart(fig_gender, use_container_width=True)
st.success("Dashboard Loaded Successfully")
