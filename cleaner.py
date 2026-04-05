import pandas as pd
import os

def run_advanced_cleaning():
    df = pd.read_csv('data/jobs_raw.csv')
    
    # 1. Title & Company Sanitization
    df['title'] = df['title'].str.strip().str.title()
    df['company'] = df['company'].str.strip().str.rstrip(',')

    # 2. Smart Remote Detection
    # Checks both the location AND the title for the word 'Remote'
    df['is_remote'] = (
        df['location'].str.contains('remote', case=False, na=False) | 
        df['title'].str.contains('remote', case=False, na=False)
    ).astype(int)

    # 3. Location Normalization
    df['location'] = df['location'].str.replace(', Pakistan', '', case=False).str.strip()
    # If it was 'Remote, Lahore', keep 'Lahore' as the city but is_remote is already 1
    df['location'] = df['location'].apply(lambda x: x.split(',')[-1].strip().title() if ',' in str(x) else x.title())

    # 4. Skill Synonym Mapping (Deduplication)
    def clean_skills(s):
        if pd.isna(s) or s == '': return 'Not Specified'
        tokens = [t.strip().lower() for t in str(s).split(',')]
        cleaned = []
        for t in tokens:
            # Merge common synonyms
            if 'communication' in t: t = 'communication skills'
            if 'microsoft excel' in t or t == 'excel': t = 'ms excel'
            if 'crm' in t: t = 'crm'
            cleaned.append(t)
        return ', '.join(list(set(cleaned))) # set() removes duplicates in the same row

    df['skills'] = df['skills'].apply(clean_skills)

    # 5. Tech Tagging
    tech_stack = ['software', 'developer', 'data', 'analyst', 'it', 'web', 'python', 'java', 'sql', 'engineer', 'react', 'node', 'flutter']
    df['is_tech'] = df['title'].str.contains('|'.join(tech_stack), case=False, na=False).astype(int)

    # 6. Final Deduplication
    df.drop_duplicates(subset=['title', 'company', 'location'], inplace=True)
    df.to_csv('data/jobs_clean.csv', index=False)
    print(f"✅ Advanced Cleaning Complete. {len(df)} records ready.")

if __name__ == "__main__":
    run_advanced_cleaning()