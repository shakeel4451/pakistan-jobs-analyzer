import pandas as pd
import re
import numpy as np
import os

def parse_salary(val):
    """Resilient salary parser for '50K - 100K' or '70K' formats."""
    if pd.isna(val) or str(val).lower() in ['n/a', 'not disclosed', 'unknown']:
        return np.nan, np.nan
    matches = re.findall(r'(\d+)K', str(val))
    if len(matches) >= 2:
        return int(matches[0]) * 1000, int(matches[1]) * 1000
    if len(matches) == 1:
        return int(matches[0]) * 1000, int(matches[0]) * 1000
    return np.nan, np.nan

def clean_data(input_path='data/jobs_raw.csv', output_path='data/jobs_clean.csv'):
    if not os.path.exists(input_path):
        print(f"❌ Source file {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    print(f"--- Ingested {len(df)} raw records ---")

    # 1. Handle Critical Missing Data
    # We fill 'skills' with 'Not Specified' so we don't lose the rows
    df['skills'] = df['skills'].fillna('Not Specified')
    df['experience'] = df['experience'].fillna('Not Specified')
    df['salary'] = df['salary'].fillna('Not Disclosed')

    # 2. Text Normalization
    df['title'] = df['title'].str.strip().str.title()
    df['company'] = df['company'].str.strip()
    
    # 3. Location & Remote Logic
    # Splits "Lahore, Pakistan" -> "Lahore"
    df['city'] = df['location'].apply(lambda x: str(x).split(',')[0].strip())
    df['is_remote'] = df['location'].str.contains('remote', case=False, na=False).astype(int)

    # 4. Numerical Extraction (without dropping rows)
    salary_cols = df['salary'].apply(lambda x: pd.Series(parse_salary(x)))
    df['salary_min'] = salary_cols[0]
    df['salary_max'] = salary_cols[1]
    
    # Extract years (e.g., '1 Year' -> 1.0)
    df['exp_years'] = df['experience'].str.extract(r'(\d+)').astype(float)

    # 5. Smart Deduplication
    # We only drop if Title, Company, and City are identical.
    before_dedup = len(df)
    df.drop_duplicates(subset=['title', 'company', 'city'], inplace=True)
    print(f"📉 Deduplication: Removed {before_dedup - len(df)} duplicate listings.")

    # 6. Tech Categorization (Crucial for your LinkedIn project)
    tech_keywords = ['software', 'developer', 'engineer', 'data', 'analyst', 'it', 'web', 'python', 'java', 'graphic']
    df['is_tech'] = df['title'].str.contains('|'.join(tech_keywords), case=False, na=False).astype(int)

    # Final Audit
    print(f"✅ Clean complete. Final count: {len(df)} rows.")
    print(f"💻 Tech Jobs identified: {df['is_tech'].sum()}")
    
    os.makedirs('data', exist_ok=True)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    clean_data()