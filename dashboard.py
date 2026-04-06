import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Pakistan Jobs Market 2026",
    page_icon="🇵🇰",
    layout="wide"
)

# ── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/jobs_clean.csv")
    return df

df = load_data()
tech_df = df[df["is_tech"] == 1]

# ── Header ────────────────────────────────────────────────────
st.markdown("## 🇵🇰 Pakistan Jobs Market Analyzer — 2026")
st.markdown("*Scraped live from Rozee.pk · 1,020 job listings across Lahore, Karachi, Islamabad & Rawalpindi*")
st.divider()

# ── KPI Row ───────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Jobs Analyzed", f"{len(df):,}")
k2.metric("Tech Sector Jobs", f"{len(tech_df):,}", f"{len(tech_df)/len(df)*100:.1f}% of market")
k3.metric("Remote Opportunities", f"{df['is_remote'].sum():,}", f"{df['is_remote'].mean()*100:.1f}% remote")
k4.metric("Unique Companies", f"{df['company'].nunique():,}")

st.divider()

# ── Row 1: City Distribution + Remote Split ───────────────────
col1, col2 = st.columns([3, 2])

with col1:
    city_counts = df["location"].value_counts().head(6).reset_index()
    city_counts.columns = ["City", "Jobs"]
    fig_city = px.bar(
        city_counts, x="City", y="Jobs", color="Jobs",
        color_continuous_scale="Blues",
        title="📍 Top Hiring Cities in Pakistan",
        text="Jobs"
    )
    fig_city.update_traces(textposition="outside")
    fig_city.update_layout(showlegend=False, coloraxis_showscale=False,
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_city, use_container_width=True)

with col2:
    remote_data = pd.DataFrame({
        "Type": ["On-Site", "Remote"],
        "Count": [len(df) - df["is_remote"].sum(), df["is_remote"].sum()]
    })
    fig_remote = px.pie(
        remote_data, values="Count", names="Type",
        title="🏠 Remote vs On-Site",
        color_discrete_sequence=["#1f77b4", "#17becf"],
        hole=0.45
    )
    fig_remote.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_remote, use_container_width=True)

# ── Row 2: Top Skills ─────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    all_skills = (
        df["skills"].str.split(",").explode().str.strip().str.title()
    )
    all_skills = all_skills[~all_skills.isin(["Not Specified", "Crm"])]
    top_skills = all_skills.value_counts().head(12).reset_index()
    top_skills.columns = ["Skill", "Count"]

    fig_skills = px.bar(
        top_skills, x="Count", y="Skill", orientation="h",
        title="🔥 Top 12 In-Demand Skills (All Sectors)",
        color="Count", color_continuous_scale="Oranges"
    )
    fig_skills.update_layout(yaxis=dict(autorange="reversed"),
                             showlegend=False, coloraxis_showscale=False,
                             plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_skills, use_container_width=True)

with col4:
    tech_skills = (
        tech_df["skills"].str.split(",").explode().str.strip().str.upper()
    )
    tech_skills = tech_skills[tech_skills != "NOT SPECIFIED"]
    top_tech = tech_skills.value_counts().head(12).reset_index()
    top_tech.columns = ["Skill", "Count"]

    fig_tech = px.bar(
        top_tech, x="Count", y="Skill", orientation="h",
        title="💻 Top 12 Tech Skills",
        color="Count", color_continuous_scale="Greens"
    )
    fig_tech.update_layout(yaxis=dict(autorange="reversed"),
                           showlegend=False, coloraxis_showscale=False,
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_tech, use_container_width=True)

# ── Row 3: Tech vs Non-Tech by City + Experience Dist ─────────
col5, col6 = st.columns(2)

with col5:
    city_tech = df.groupby(["location", "is_tech"]).size().reset_index(name="count")
    city_tech["is_tech"] = city_tech["is_tech"].map({1: "Tech", 0: "Non-Tech"})
    city_tech = city_tech[city_tech["location"].isin(["Lahore", "Karachi", "Islamabad", "Rawalpindi"])]

    fig_stack = px.bar(
        city_tech, x="location", y="count", color="is_tech",
        title="🏙️ Tech vs Non-Tech Jobs by City",
        barmode="stack",
        color_discrete_map={"Tech": "#1f77b4", "Non-Tech": "#aec7e8"},
        labels={"location": "City", "count": "Jobs", "is_tech": "Type"}
    )
    fig_stack.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_stack, use_container_width=True)

with col6:
    exp_counts = df["experience"].value_counts().head(8).reset_index()
    exp_counts.columns = ["Experience", "Count"]
    exp_counts = exp_counts[exp_counts["Experience"] != "N/A"]

    fig_exp = px.bar(
        exp_counts, x="Experience", y="Count",
        title="📅 Experience Level Distribution",
        color="Count", color_continuous_scale="Purples",
        text="Count"
    )
    fig_exp.update_traces(textposition="outside")
    fig_exp.update_layout(showlegend=False, coloraxis_showscale=False,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_exp, use_container_width=True)

# ── Row 4: Top Hiring Companies ───────────────────────────────
st.subheader("🏢 Top 15 Hiring Companies")
top_cos = df["company"].value_counts().head(15).reset_index()
top_cos.columns = ["Company", "Openings"]
fig_cos = px.bar(
    top_cos, x="Openings", y="Company", orientation="h",
    color="Openings", color_continuous_scale="Teal", text="Openings"
)
fig_cos.update_traces(textposition="outside")
fig_cos.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False,
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      height=450)
st.plotly_chart(fig_cos, use_container_width=True)

# ── Row 5: Raw Data Table ─────────────────────────────────────
st.divider()
st.subheader("🔍 Explore Raw Data")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    city_filter = st.selectbox("Filter by City", ["All"] + sorted(df["location"].unique().tolist()))
with col_f2:
    sector_filter = st.selectbox("Filter by Sector", ["All", "Tech", "Non-Tech"])
with col_f3:
    search = st.text_input("Search job title or skill", placeholder="e.g. Python, React...")

filtered = df.copy()
if city_filter != "All":
    filtered = filtered[filtered["location"] == city_filter]
if sector_filter == "Tech":
    filtered = filtered[filtered["is_tech"] == 1]
elif sector_filter == "Non-Tech":
    filtered = filtered[filtered["is_tech"] == 0]
if search:
    mask = (
        filtered["title"].str.contains(search, case=False, na=False) |
        filtered["skills"].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]

st.dataframe(
    filtered[["title", "company", "location", "experience", "skills"]].reset_index(drop=True),
    use_container_width=True, height=350
)
st.caption(f"Showing {len(filtered):,} of {len(df):,} jobs")

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center><small>Built with Playwright · Pandas · Plotly · Streamlit &nbsp;|&nbsp; "
    "Data: Rozee.pk 2026 &nbsp;|&nbsp; "
    "GitHub: <a href='https://github.com/shakeel4451/pakistan-jobs-analyzer'>shakeel4451</a></small></center>",
    unsafe_allow_html=True
)