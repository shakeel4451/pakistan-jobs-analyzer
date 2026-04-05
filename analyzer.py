import pandas as pd

def run_market_audit():
    df = pd.read_csv('data/jobs_clean.csv')
    
    print("\n" + "="*30)
    print("🇵🇰 DATAHARVEST PK: MARKET REPORT")
    print("="*30)
    
    # KPI 1: Tech vs General Market
    tech_count = df['is_tech'].sum()
    print(f"Tech-Specific Roles: {tech_count} ({ (tech_count/len(df))*100 :.1f}%)")

    # KPI 2: Remote Work Saturation
    remote_rate = df['is_remote'].mean() * 100
    print(f"Remote Work Saturation: {remote_rate:.1f}%")

    # KPI 3: Skill Dominance (Top 10)
    skills = df['skills'].fillna('').str.lower().str.split(',').explode().str.strip()
    top_skills = skills[skills != ''].value_counts().head(10)
    print("\n🔥 Top 10 High-Demand Skills:")
    print(top_skills)

if __name__ == "__main__":
    run_market_audit()