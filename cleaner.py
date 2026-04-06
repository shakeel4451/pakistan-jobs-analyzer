import pandas as pd
import os

def run_production_cleaning():
    raw_path = 'data/jobs_raw.csv'
    clean_path = 'data/jobs_clean.csv'
    
    if not os.path.exists(raw_path):
        print(f"❌ Error: {raw_path} not found.")
        return

    df = pd.read_csv(raw_path)
    print(f"📡 Processing {len(df)} records for visualization...")

    # 1. Title & Company Normalization
    df['title'] = df['title'].str.strip().str.title()
    df['company'] = df['company'].str.strip().str.rstrip(',')

    # 2. Remote Detection (Detects 'Remote' in Title or Location)
    df['is_remote'] = (
        df['location'].str.contains('remote', case=False, na=False) | 
        df['title'].str.contains('remote', case=False, na=False)
    ).astype(int)

    # 3. Location Normalization (Isolates City Name)
    df['location'] = df['location'].str.replace(', Pakistan', '', case=False).str.strip()
    df['location'] = df['location'].apply(lambda x: str(x).split(',')[-1].strip().title() if ',' in str(x) else str(x).title())
    df['location'] = df['location'].replace(['', 'Nan', 'None'], 'Unknown')

    # 4. Experience Extraction (CRITICAL FOR VISUALIZER)
    # Extracts the first number found (e.g., "2 Years" -> 2.0)
    df['exp_years'] = df['experience'].str.extract(r'(\d+)').astype(float).fillna(0)

    # 5. Skill Synonym Mapping
    def clean_skills(s):
        if pd.isna(s) or s == '' or s == 'nan': return 'Not Specified'
        tokens = [t.strip().lower() for t in str(s).split(',')]
        cleaned = []
        for t in tokens:
            if 'communication' in t: t = 'communication skills'
            if 'excel' in t: t = 'ms excel'
            if 'crm' in t: t = 'crm'
            cleaned.append(t)
        return ', '.join(list(set(cleaned)))

    df['skills'] = df['skills'].apply(clean_skills)

    # 6. Technical Role Classification
    tech_stack = ['software', 'developer', 'data', 'analyst', 'it', 'web', 'python', 'java', 'sql', 'engineer', 'react', 'node', 'flutter', 'sqa', 'devops']
    df['is_tech'] = df['title'].str.contains('|'.join(tech_stack), case=False, na=False).astype(int)

    # 7. Global Deduplication
    df.drop_duplicates(subset=['title', 'company', 'location'], inplace=True)
    
    # Save Final Dataset
    os.makedirs('data', exist_ok=True)
    df.to_csv(clean_path, index=False)
    print(f"✅ Sanitization Complete: {len(df)} unique records saved with all required metrics.")

if __name__ == "__main__":
    run_production_cleaning()