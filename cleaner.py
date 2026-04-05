import pandas as pd
import numpy as np
import os

def run_cleaning_pipeline():
    raw_path = 'data/jobs_raw.csv'
    clean_path = 'data/jobs_clean.csv'
    
    if not os.path.exists(raw_path):
        print(f"❌ Error: {raw_path} not found. Execute scraper.py first.")
        return

    # Load Raw Dataset
    df = pd.read_csv(raw_path)
    print(f"📡 Ingested {len(df)} records. Starting Sanitization...")

    # --- Stage 1: String Normalization ---
    # Title Case for consistency and stripping artifacts
    df['title'] = df['title'].str.strip().str.title()
    # Remove trailing commas often found in company names from breadcrumbs
    df['company'] = df['company'].str.strip().str.rstrip(',')

    # --- Stage 2: Geographic Standardization ---
    # Remove country suffix and handle empty location clusters
    df['location'] = df['location'].str.replace(', Pakistan', '', case=False).str.strip()
    df['location'] = df['location'].replace(['', ',', 'nan'], 'Unknown')
    df['location'] = df['location'].fillna('Unknown')

    # --- Stage 3: Skill Taxonomy Tokenization ---
    # Handle NaNs and normalize for frequency distribution
    df['skills'] = df['skills'].fillna('Not Specified')
    
    def normalize_skills(s):
        if s == 'Not Specified': return s
        # Lowercase, strip each token, and join back for CSV readability
        return ', '.join([skill.strip().lower() for skill in s.split(',')])
    
    df['skills'] = df['skills'].apply(normalize_skills)

    # --- Stage 4: Heuristic Classification ---
    # Expanded tech_stack to capture DevOps, SQA, and Cloud roles
    tech_stack = [
        'software', 'developer', 'data', 'analyst', 'it', 'web', 'python', 'java', 
        'sql', 'engineer', 'react', 'node', 'flutter', 'technical', 'devops', 
        'fullstack', 'frontend', 'backend', 'cloud', 'database', 'aws', 'mobile', 
        'android', 'ios', 'cyber', 'sqa', 'automation', 'testing', 'bioinformatic'
    ]
    pattern = '|'.join(tech_stack)
    df['is_tech'] = df['title'].str.contains(pattern, case=False, na=False).astype(int)

    # --- Stage 5: Experience Coefficient Extraction ---
    # Extract numerical value for quantitative analysis
    df['exp_years'] = df['experience'].str.extract(r'(\d+)').astype(float).fillna(0)

    # --- Stage 6: Global Deduplication ---
    # Verify uniqueness across Title-Company-Location triads
    before_count = len(df)
    df.drop_duplicates(subset=['title', 'company', 'location'], inplace=True)
    after_count = len(df)

    # Export Processed Data
    os.makedirs('data', exist_ok=True)
    df.to_csv(clean_path, index=False)
    
    print("-" * 30)
    print(f"✅ CLEANING COMPLETE")
    print(f"📊 Unique Records: {after_count}")
    print(f"📉 Redundant Rows Dropped: {before_count - after_count}")
    print(f"💻 Tech vs General Split: {df['is_tech'].sum()} Tech Roles identified.")
    print("-" * 30)

if __name__ == "__main__":
    run_cleaning_pipeline()