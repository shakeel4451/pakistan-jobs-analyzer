# 🇵🇰 Pakistan Jobs Market Analyzer — 2026

> A complete end-to-end data pipeline that scrapes, cleans, analyzes, and visualizes the Pakistani tech job market in real time.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-scraping-green?logo=playwright)
![Pandas](https://img.shields.io/badge/Pandas-data--cleaning-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-visualization-purple?logo=plotly)
![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-red?logo=streamlit)

---

## 📌 What This Project Does

Automatically collects **1,000+ job listings** from [Rozee.pk](https://www.rozee.pk) across Pakistan's top cities, cleans the data using Pandas, extracts market insights, and serves everything as an interactive Streamlit dashboard.

**Key questions it answers:**

- What are the most in-demand skills in Pakistan's job market right now?
- Which cities have the most tech opportunities?
- What's the ratio of remote to on-site roles?
- Which companies are hiring the most?

---

## 📊 Key Findings (April 2026)

| Metric               | Value                |
| -------------------- | -------------------- |
| Total jobs analyzed  | 1,020                |
| Tech sector share    | 37.6%                |
| Remote opportunities | 0.2%                 |
| Top hiring city      | Lahore (394 jobs)    |
| #1 tech skill        | Python               |
| #1 market-wide skill | Communication Skills |

---

## 🗂️ Project Structure

```
pakistan-jobs-analyzer/
├── scraper.py        # Playwright scraper — Rozee.pk multi-keyword/city
├── cleaner.py        # Pandas pipeline — normalization, dedup, tagging
├── analyzer.py       # Terminal market audit report
├── dashboard.py      # Streamlit interactive dashboard
├── data/
│   ├── jobs_raw.csv  # Raw scraped output
│   └── jobs_clean.csv# Cleaned, tagged, analysis-ready
└── README.md
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install playwright pandas plotly streamlit
playwright install chromium
```

### 2. Scrape fresh data

```bash
python scraper.py
```

Targets 40 keywords × 4 cities (Lahore, Karachi, Islamabad, Rawalpindi) with pagination. Saves to `data/jobs_raw.csv`.

### 3. Clean the data

```bash
python cleaner.py
```

- Strips and normalizes job titles and company names
- Detects remote roles from both title and location fields
- Maps skill synonyms (e.g. `Microsoft Excel` → `ms excel`)
- Tags tech roles using keyword matching
- Deduplicates on `title + company + location`
- Saves to `data/jobs_clean.csv`

### 4. Run the terminal audit

```bash
python analyzer.py
```

Prints a formatted market report with KPIs, top cities, and skill frequency tables.

### 5. Launch the dashboard

```bash
streamlit run dashboard.py
```

Opens an interactive dashboard with filters, charts, and a searchable data table.

---

## 🛠️ Tech Stack

| Layer         | Tool                                                |
| ------------- | --------------------------------------------------- |
| Scraping      | Playwright (async, headless Chromium)               |
| Data cleaning | Pandas                                              |
| Visualization | Plotly Express                                      |
| Dashboard     | Streamlit                                           |
| Bot bypass    | `wait_for_load_state`, `mouse.wheel`, random delays |
| Deduplication | Fingerprint hashing (`title-company` pair)          |

---

## 💡 What Makes This Different

Most data science portfolios use Kaggle datasets. This project sources **fresh, real-world data** directly from Pakistan's largest job platform — giving insights that are actually current and locally relevant.

The scraper is also production-grade: it handles pagination, lazy loading, random delays to avoid bot detection, and deduplicates across keyword/city combinations.

---

## 📈 Dashboard Features

- **KPI cards** — total jobs, tech share, remote rate, unique companies
- **City distribution** bar chart
- **Remote vs On-site** donut chart
- **Top 12 in-demand skills** (all sectors)
- **Top 12 tech-specific skills**
- **Tech vs Non-Tech by city** stacked bar
- **Experience level distribution**
- **Top 15 hiring companies**
- **Filterable data table** — search by title, skill, city, or sector

---

## 🔗 Author

**Muhammad Shakeel** — CS Graduate | Python Developer | Aspiring AI Engineer  
[GitHub](https://github.com/shakeel4451) · [LinkedIn](https://.linkedin.com/in/muhammad-shakeel-48367236a)

---

_Data collected April 2026 from Rozee.pk. For educational and portfolio purposes._
