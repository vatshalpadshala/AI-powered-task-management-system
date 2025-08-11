import streamlit as st
import pandas as pd
import plotly.express as px

# Page title
st.set_page_config(page_title="AI Task Dashboard", layout="wide")
st.title("📊 AI-Powered Task Management Dashboard")

# Load your dataset
@st.cache_data
def load_data():
    return pd.read_csv("jira_dataset.csv")  # Make sure the CSV file is in the same folder as app.py

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Tasks")
priorities = st.sidebar.multiselect("Select Priority", df["priority"].unique(), default=df["priority"].unique())
filtered_df = df[df["priority"].isin(priorities)]

# Show data table
st.subheader("Filtered Tasks")
st.dataframe(filtered_df)

# Plot 1: Task by Issue Type
fig1 = px.pie(filtered_df, names='issue_type', title='Task Distribution by Issue Type')
st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Priority Count
priority_count = filtered_df['priority'].value_counts().reset_index()
priority_count.columns = ['priority', 'count']
fig2 = px.bar(priority_count, x='priority', y='count', title='Task Count by Priority')
st.plotly_chart(fig2, use_container_width=True)

# Plot 3: Word Count Histogram
if 'word_count' in filtered_df.columns:
    fig3 = px.histogram(filtered_df, x='word_count', nbins=20, title='Word Count Distribution')
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No 'word_count' column found.")

# Plot 4: Top 10 Assignees
top_assignees = filtered_df['task_assignee'].value_counts().nlargest(10).reset_index()
top_assignees.columns = ['Assignee', 'Task Count']
fig4 = px.bar(top_assignees, x='Assignee', y='Task Count', title='Top 10 Task Assignees')
st.plotly_chart(fig4, use_container_width=True)
