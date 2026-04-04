import pandas as pd
import re
import numpy as np
import os

def parse_salary(salary_str):
    """
    Standardizes salary strings like '50K - 100K' into numeric min/max values.
    Returns: (min_salary, max_salary)
    """
    if pd.isna(salary_str) or 'N/A' in str(salary_str):
        return np.nan, np.nan
    
    # Find all digits followed by 'K'
    matches = re.findall(r'(\d+)K', str(salary_str))
    if len(matches) == 2:
        return int(matches[0]) * 1000, int(matches[1]) * 1000
    elif len(matches) == 1:
        return int(matches[0]) * 1000, int(matches[0]) * 1000
    return np.nan, np.nan

def parse_experience(exp_str):
    """
    Extracts numeric years from strings like '1 Year' or 'Fresh'.
    """
    if pd.isna(exp_str) or 'N/A' in str(exp_str):
        return np.nan
    if 'fresh' in str(exp_str).lower():
        return 0.0
    match = re.search(r'(\d+)', str(exp_str))
    return float(match.group(1)) if match else np.nan

def clean_data(input_file='data/jobs_raw.csv', output_file='data/jobs_clean.csv'):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run scraper.py first.")
        return

    # Load raw dataset
    df = pd.read_csv(input_file)
    print(f"Raw data loaded: {len(df)} rows.")

    # 1. Feature Engineering: Title & Company
    df['title'] = df['title'].str.strip().str.title()
    df['company'] = df['company'].str.strip()

    # 2. Location Normalization & Remote Tagging
    # Converts 'Lahore, Pakistan' -> 'Lahore'
    df['city'] = df['location'].str.split(',').str[0].str.strip()
    df['is_remote'] = df['location'].str.contains('remote', case=False, na=False).astype(int)

    # 3. Numerical Transformation: Salary & Experience
    salary_data = df['salary'].apply(lambda x: pd.Series(parse_salary(x)))
    df['salary_min'] = salary_data[0]
    df['salary_max'] = salary_data[1]
    df['exp_years'] = df['experience'].apply(parse_experience)

    # 4. Skill Tokenization
    # Standardizes skills to lowercase list for frequency analysis
    df['skills'] = df['skills'].str.lower().str.split(',').apply(
        lambda x: [s.strip() for s in x] if isinstance(x, list) else []
    )

    # 5. Temporal Alignment
    df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')

    # 6. Deduplication
    # Removing duplicate listings based on title, company, and city
    initial_count = len(df)
    df.drop_duplicates(subset=['title', 'company', 'city'], inplace=True)
    print(f"Deduplication complete: Removed {initial_count - len(df)} duplicate entries.")

    # Save processed data
    os.makedirs('data', exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✅ Cleaned data saved to {output_file}. Ready for analysis.")

if __name__ == "__main__":
    clean_data()