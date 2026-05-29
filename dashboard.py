import pandas as pd
import streamlit as st
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Clinical Trial Dashboard",
    layout="wide"
)

# Title
st.title("Clinical Trial Safety Dashboard")

# Load Data
df = pd.read_csv("clinical_data.csv")

# Sidebar Filters
st.sidebar.header("Filter Data")

treatment_filter = st.sidebar.multiselect(
    "Select Treatment Group",
    options=df["Treatment"].unique(),
    default=df["Treatment"].unique()
)

severity_filter = st.sidebar.multiselect(
    "Select Severity",
    options=df["Severity"].unique(),
    default=df["Severity"].unique()
)

# Apply Filters
filtered_df = df[
    (df["Treatment"].isin(treatment_filter)) &
    (df["Severity"].isin(severity_filter))
]

# KPI Cards
total_patients = filtered_df["Patient_ID"].nunique()
average_age = round(filtered_df["Age"].mean(), 1)
severe_cases = filtered_df[
    filtered_df["Severity"] == "Severe"
].shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("Total Patients", total_patients)
col2.metric("Average Age", average_age)
col3.metric("Severe Cases", severe_cases)

st.divider()

# Gender Distribution
gender_chart = px.pie(
    filtered_df,
    names="Gender",
    title="Gender Distribution"
)

# Adverse Event Distribution
ae_chart = px.bar(
    filtered_df["Adverse_Event"].value_counts().reset_index(),
    x="Adverse_Event",
    y="count",
    title="Adverse Event Distribution"
)

# Severity Distribution
severity_chart = px.histogram(
    filtered_df,
    x="Severity",
    color="Severity",
    title="Severity Distribution"
)

# Charts Layout
chart1, chart2 = st.columns(2)

with chart1:
    st.plotly_chart(gender_chart, use_container_width=True)

with chart2:
    st.plotly_chart(ae_chart, use_container_width=True)

st.plotly_chart(severity_chart, use_container_width=True)

st.divider()

# Display Dataset
st.subheader("Clinical Dataset")
st.dataframe(filtered_df)