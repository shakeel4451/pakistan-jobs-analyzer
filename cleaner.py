import pandas as pd
import numpy as np
import os

def run_cleaning_pipeline():
    raw_path = 'data/jobs_raw.csv'
    clean_path = 'data/jobs_clean.csv'
    
    if not os.path.exists(raw_path):
        print(f"❌ Error: {raw_path} not found.")
        return

    df = pd.read_csv(raw_path)
    print(f"📡 Sanitizing {len(df)} records...")

    # Stage 1: String Normalization
    df['title'] = df['title'].str.strip().str.title()
    df['company'] = df['company'].str.strip().str.rstrip(',')

    # Stage 2: Geographic & Remote Standardization (FIXED)
    df['location'] = df['location'].str.replace(', Pakistan', '', case=False).str.strip()
    df['location'] = df['location'].replace(['', ',', 'nan'], 'Unknown').fillna('Unknown')
    # Restoring the missing remote flag logic
    df['is_remote'] = df['location'].str.contains('remote', case=False, na=False).astype(int)

    # Stage 3: Skill Normalization
    df['skills'] = df['skills'].fillna('Not Specified')
    df['skills'] = df['skills'].apply(lambda s: ', '.join([x.strip().lower() for x in s.split(',')]) if s != 'Not Specified' else s)

    # Stage 4: Tech Classification
    tech_stack = ['software', 'developer', 'data', 'analyst', 'it', 'web', 'python', 'java', 'sql', 'engineer', 'react', 'node', 'flutter', 'sqa', 'devops']
    df['is_tech'] = df['title'].str.contains('|'.join(tech_stack), case=False, na=False).astype(int)

    # Stage 5: Experience Extraction
    df['exp_years'] = df['experience'].str.extract(r'(\d+)').astype(float).fillna(0)

    # Stage 6: Deduplication
    df.drop_duplicates(subset=['title', 'company', 'location'], inplace=True)

    os.makedirs('data', exist_ok=True)
    df.to_csv(clean_path, index=False)
    print(f"✅ Success: {len(df)} unique jobs saved to {clean_path}")

if __name__ == "__main__":
    run_cleaning_pipeline()