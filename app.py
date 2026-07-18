import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="FIFA Intelligence Analytics", layout="wide")

st.markdown(
    """
    <style>
    :root{
      --bg0:#05060a;
      --bg1:#070a12;
      --card:rgba(255,255,255,0.06);
      --card2:rgba(255,255,255,0.09);
      --stroke:rgba(255,255,255,0.14);
      --text:rgba(255,255,255,0.92);
      --muted:rgba(255,255,255,0.70);
      --accent:#35d0ff;
      --accent2:#7c4dff;
      --good:#22c55e;
      --warn:#f59e0b;
      --bad:#ef4444;
      --shadow: 0 16px 60px rgba(0,0,0,0.55);
      --shadow2: 0 10px 35px rgba(0,0,0,0.40);
      --radius:18px;
    }

    html, body {
      background:
        radial-gradient(1200px 600px at 20% 10%, rgba(53,208,255,0.10), transparent 55%),
        radial-gradient(1000px 520px at 80% 0%, rgba(124,77,255,0.10), transparent 50%),
        linear-gradient(180deg, var(--bg0), var(--bg1));
      color: var(--text);
    }

    .main .block-container{ padding-top: 26px; }

    /* Glass */
    .glass{
      background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.04));
      border: 1px solid rgba(255,255,255,0.14);
      box-shadow: var(--shadow2);
      border-radius: var(--radius);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }

    /* 3D KPI */
    .kpi{
      position: relative;
      overflow:hidden;
      padding: 18px 16px;
      transform-style: preserve-3d;
      transition: transform 250ms ease, box-shadow 250ms ease;
    }
    .kpi::before{
      content:"";
      position:absolute;
      inset:-60px;
      background:
        radial-gradient(circle at 30% 20%, rgba(53,208,255,0.28), transparent 45%),
        radial-gradient(circle at 80% 0%, rgba(124,77,255,0.25), transparent 48%);
      transform: translateZ(-1px);
      pointer-events:none;
    }
    .kpi:hover{
      transform: translateY(-3px) rotateX(1deg);
      box-shadow: 0 28px 85px rgba(0,0,0,0.60);
    }

    .kpi .label{
      font-size: 12px;
      color: var(--muted);
      letter-spacing: 0.6px;
      text-transform: uppercase;
    }
    .kpi .value{
      font-size: 28px;
      font-weight: 900;
      line-height: 1.1;
      margin-top: 10px;
    }
    .kpi .sub{
      font-size: 12px;
      color: var(--muted);
      margin-top: 8px;
    }

    /* Hero */
    .hero{
      padding: 22px 22px;
      border-radius: calc(var(--radius) + 6px);
      box-shadow: var(--shadow);
      border: 1px solid rgba(255,255,255,0.16);
      background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.03));
      position: relative;
      overflow: hidden;
    }

    .hero::after{
      content:"";
      position:absolute;
      inset:-2px;
      background: linear-gradient(90deg, rgba(53,208,255,0.18), rgba(124,77,255,0.18));
      opacity: 0.35;
      transform: translateX(-30%);
      transition: transform 900ms ease;
      pointer-events:none;
    }

    .hero:hover::after{ transform: translateX(0%); }

    .hero h1{ margin: 0; font-size: 34px; font-weight: 950; letter-spacing: 0.2px; }
    .hero p{ margin: 10px 0 0 0; color: var(--muted); max-width: 900px; }

    .stSidebar section{ padding: 16px 14px !important; }
    .plotly-container{ background: transparent !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def kpi_card(label: str, value, sub: str = "") -> str:
    return (
        f"""
        <div class="glass kpi">
          <div class="label">{label}</div>
          <div class="value">{value}</div>
          <div class="sub">{sub}</div>
        </div>
        """
    )


def section_title(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="glass" style="padding:14px 16px; margin-bottom: 14px; border-radius: 16px;">
          <div style="font-weight:900; letter-spacing:0.4px; font-size:16px;">{title}</div>
          {f"<div style='color:rgba(255,255,255,0.70); font-size:12px; margin-top:6px'>{subtitle}</div>" if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


# Load Data (no dataset/logic changes)
df = pd.read_csv("fifa_cleaned.csv")
required_cols = {"year", "stage", "home_team", "away_team", "home_goals", "away_goals"}
missing = sorted(list(required_cols - set(df.columns)))
if missing:
    st.error(f"Missing required columns in fifa_cleaned.csv: {missing}")
    st.stop()

with st.container():
    st.markdown(
        """
        <div class="hero">
          <h1>FIFA Intelligence Analytics</h1>
          <p>
            Premium dark glassmorphism dashboard. Use filters to explore World Cup match
            insights — KPIs and charts update instantly.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.markdown(
    """
    <div class="glass" style="padding:14px 14px; border-radius: 16px;">
      <div style="font-weight:950; letter-spacing:0.5px;">🎛️ Premium Filters</div>
      <div style="color:rgba(255,255,255,0.70); font-size:12px; margin-top:6px">
        Year & Stage selections drive all visuals automatically.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# Sidebar Filters
year = st.sidebar.multiselect(
    "🗓️ Select Year",
    df["year"].unique(),
    default=df["year"].unique(),
)
stage = st.sidebar.multiselect(
    "🏷️ Select Stage",
    df["stage"].unique(),
    default=df["stage"].unique(),
)

filtered_df = df[(df["year"].isin(year)) & (df["stage"].isin(stage))].copy()

if filtered_df.empty:
    st.info("No matches found for selected Year/Stage filters.")
    st.stop()

# Overview section
section_title("Overview", "KPIs update automatically based on your filters")
col1, col2, col3 = st.columns(3)
col1.markdown(kpi_card("Total Matches", int(filtered_df.shape[0]), "Matches in selection"), unsafe_allow_html=True)
col2.markdown(
    kpi_card(
        "Avg Home Goals",
        round(float(filtered_df["home_goals"].mean()), 2),
        "Mean goals scored as home team",
    ),
    unsafe_allow_html=True,
)
col3.markdown(
    kpi_card(
        "Avg Away Goals",
        round(float(filtered_df["away_goals"].mean()), 2),
        "Mean goals scored as away team",
    ),
    unsafe_allow_html=True,
)

# Team performance
section_title("Team Performance", "Top teams and head-to-head goal profiles")

# Top Teams by goals (same aggregation)
top_teams = (
    filtered_df.groupby("home_team")["home_goals"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig_top = px.bar(
    top_teams.reset_index().rename(columns={"home_team": "Team", "home_goals": "Avg Home Goals"}),
    x="Avg Home Goals",
    y="Team",
    orientation="h",
    color="Avg Home Goals",
    color_continuous_scale=["#35d0ff", "#7c4dff"],
)
fig_top.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="rgba(255,255,255,0.92)"),
    margin=dict(l=10, r=10, t=10, b=10),
    height=420,
    showlegend=False,
)
fig_top.update_traces(marker_line_width=0)
st.plotly_chart(fig_top, width="stretch")

# Team Comparison
team_list = sorted(df["home_team"].unique())
team1 = st.selectbox("Select Team 1 🏟️", team_list, index=0, key="team1")
team2 = st.selectbox("Select Team 2 🏟️", team_list, index=1 if len(team_list) > 1 else 0, key="team2")

team1_stats = filtered_df[filtered_df["home_team"] == team1]["home_goals"].mean()
team2_stats = filtered_df[filtered_df["home_team"] == team2]["home_goals"].mean()

comparison_df = pd.DataFrame({"Team": [team1, team2], "Avg Goals": [team1_stats, team2_stats]})

fig_cmp = go.Figure(
    data=[
        go.Bar(
            x=comparison_df["Team"],
            y=comparison_df["Avg Goals"],
            marker=dict(color=["#35d0ff", "#7c4dff"]),
        )
    ]
)
fig_cmp.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="rgba(255,255,255,0.92)"),
    margin=dict(l=10, r=10, t=10, b=10),
    height=360,
    showlegend=False,
)
fig_cmp.update_yaxes(zerolinecolor="rgba(255,255,255,0.2)")
st.plotly_chart(fig_cmp, width="stretch")

# Match insights
section_title("Match Insights", "Result distribution derived from home/away goals")

filtered_df["result"] = filtered_df.apply(
    lambda x: "Home Win" if x["home_goals"] > x["away_goals"]
    else ("Away Win" if x["home_goals"] < x["away_goals"] else "Draw"),
    axis=1,
)

result_counts = filtered_df["result"].value_counts()

labels = list(result_counts.index)
values = list(result_counts.values)

fig_pie = go.Figure(
    data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.42,
            sort=False,
            marker=dict(colors=["#35d0ff", "#7c4dff", "#22c55e", "#f59e0b"]),
            textinfo="label+percent",
        )
    ]
)
fig_pie.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="rgba(255,255,255,0.92)"),
    margin=dict(l=10, r=10, t=10, b=10),
    height=420,
    showlegend=False,
)
st.plotly_chart(fig_pie, width="stretch")

# Raw Data (optional)
show_raw = st.sidebar.checkbox("📄 Show raw data", value=False)
if show_raw:
    st.subheader("📄 Raw Data")
    st.dataframe(filtered_df)

