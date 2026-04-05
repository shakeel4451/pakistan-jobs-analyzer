import pandas as pd
import os

def run_market_audit():
    file_path = 'data/jobs_clean.csv'
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found. Please run cleaner.py first.")
        return

    df = pd.read_csv(file_path)
    
    print("\n" + "="*40)
    print("🇵🇰 DATAHARVEST PK: MARKET INTELLIGENCE")
    print("="*40)
    
    # 1. Tech Distribution
    if 'is_tech' in df.columns:
        tech_count = df['is_tech'].sum()
        tech_pct = (tech_count / len(df)) * 100
        print(f"🔹 Tech-Specific Roles: {tech_count} ({tech_pct:.1f}%)")
    
    # 2. Remote Work Index (Safe check)
    if 'is_remote' in df.columns:
        remote_rate = df['is_remote'].mean() * 100
        print(f"🔹 Remote Opportunity Rate: {remote_rate:.1f}%")
    else:
        print("⚠️ Warning: 'is_remote' column missing. Re-run cleaner.py.")

    # 3. City Breakdown
    print("\n📍 Top Hiring Hubs:")
    print(df['location'].value_counts().head(4))

    # 4. Skill Demand Frequency
    if 'skills' in df.columns:
        skills = df['skills'].str.split(',').explode().str.strip()
        top_skills = skills[~skills.isin(['not specified', ''])].value_counts().head(10)
        print("\n🔥 Top 10 In-Demand Skills:")
        for skill, count in top_skills.items():
            print(f" - {skill.title()}: {count} listings")

    print("="*40)

if __name__ == "__main__":
    run_market_audit()