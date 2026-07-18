
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="FIFA Dashboard", layout="wide")

# Load Data
df = pd.read_csv("fifa_cleaned.csv")

st.title("⚽ FIFA World Cup Analytics Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

year = st.sidebar.multiselect("Select Year", df['year'].unique(), default=df['year'].unique())
stage = st.sidebar.multiselect("Select Stage", df['stage'].unique(), default=df['stage'].unique())

filtered_df = df[(df['year'].isin(year)) & (df['stage'].isin(stage))].copy()

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", filtered_df.shape[0])
col2.metric("Avg Home Goals", round(filtered_df['home_goals'].mean(), 2))
col3.metric("Avg Away Goals", round(filtered_df['away_goals'].mean(), 2))

# Top Teams
st.subheader("📊 Top Teams by Goals")

top_teams = (
    filtered_df.groupby('home_team')['home_goals']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_teams)

# Result Distribution
st.subheader("🥧 Match Result Distribution")

filtered_df['result'] = filtered_df.apply(
    lambda x: 'Home Win' if x['home_goals'] > x['away_goals']
    else ('Away Win' if x['home_goals'] < x['away_goals'] else 'Draw'),
    axis=1
)

result_counts = filtered_df['result'].value_counts()

fig, ax = plt.subplots()
ax.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%')
st.pyplot(fig)

# Team Comparison
st.subheader("⚔️ Team Comparison")

teams = sorted(df['home_team'].unique())

team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", teams)

team1_stats = filtered_df[filtered_df['home_team'] == team1]['home_goals'].mean()
team2_stats = filtered_df[filtered_df['home_team'] == team2]['home_goals'].mean()

comparison_df = pd.DataFrame({
    'Team': [team1, team2],
    'Avg Goals': [team1_stats, team2_stats]
})

st.bar_chart(comparison_df.set_index('Team'))

# Raw Data
st.subheader("📄 Raw Data")
st.dataframe(filtered_df)