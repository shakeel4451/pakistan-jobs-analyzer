import pandas as pd

def run_market_audit():
    df = pd.read_csv('data/jobs_clean.csv')
    
    print("\n" + "═"*45)
    print("🇵🇰 DATAHARVEST PK: 2026 MARKET AUDIT")
    print("═"*45)
    
    # KPIs
    tech_df = df[df['is_tech'] == 1]
    print(f"🔹 Total Jobs Analyzed: {len(df)}")
    print(f"🔹 Tech-Sector Depth:  {len(tech_df)} ({ (len(tech_df)/len(df))*100 :.1f}%)")
    print(f"🔹 Remote Index:       {df['is_remote'].mean()*100 :.1f}%")

    # City Hubs
    print("\n📍 TOP HIRING HUBS")
    print(df['location'].value_counts().head(4))

    # General Market Skills
    print("\n🔥 TOP 10 MARKET-WIDE SKILLS")
    all_skills = df['skills'].str.split(',').explode().str.strip()
    top_gen = all_skills[all_skills != 'not specified'].value_counts().head(10)
    for skill, count in top_gen.items():
        print(f" - {skill.title()}: {count}")

    # TECH SPECIFIC SKILLS (The Value-Add)
    print("\n💻 TOP 10 TECH-SPECIFIC SKILLS")
    tech_skills = tech_df['skills'].str.split(',').explode().str.strip()
    top_tech = tech_skills[tech_skills != 'not specified'].value_counts().head(10)
    for skill, count in top_tech.items():
        print(f" - {skill.upper()}: {count}")

    print("═"*45)

if __name__ == "__main__":
    run_market_audit()