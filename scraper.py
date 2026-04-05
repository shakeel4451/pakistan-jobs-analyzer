import asyncio
import csv
import random
import os
from playwright.async_api import async_playwright

async def scrape_rozee_mega(target_count=1000):
    # Expanded keyword list based on your successful 600+ run
    queries = [
        'python', 'data', 'developer', 'software', 'engineer', 'analyst', 'sql', 'react', 
        'node', 'flutter', 'android', 'ios', 'java', 'javascript', 'sqa', 'devops', 
        'cloud', 'aws', 'marketing', 'sales', 'hr', 'finance', 'accounting', 'manager', 
        'intern', 'graphic', 'ui', 'ux', 'seo', 'content', 'social media', 'laravel', 
        'wordpress', 'shopify', 'asp.net', 'c#', 'c++', 'unity', 'sap', 'power bi'
    ]
    
    # Verified 2026 City Codes
    cities = {'Lahore': '1185', 'Karachi': '1184', 'Islamabad': '1180', 'Rawalpindi': '1190'}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) 
        context = await browser.new_context()
        page = await context.new_page()
        
        all_jobs = []
        seen_fingerprints = set()

        for q in queries:
            for city_name, city_code in cities.items():
                if len(all_jobs) >= target_count: break
                
                # Check Page 1 (fpn 0) and Page 2 (fpn 20) for every keyword/city combo
                for offset in [0, 20]:
                    url = f"https://www.rozee.pk/job/jsearch/q/{q}/fc/{city_code}/fpn/{offset}"
                    print(f"📡 {q.upper()} | {city_name} | Offset {offset}")
                    
                    try:
                        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                        await page.mouse.wheel(0, 2000) # Trigger lazy-load
                        await asyncio.sleep(1.5)

                        job_cards = await page.query_selector_all(".job")
                        if not job_cards: break

                        new_added = 0
                        for card in job_cards:
                            title_node = await card.query_selector("h3.s-18 bdi")
                            comp_node = await card.query_selector(".cname bdi a:nth-of-type(1)")
                            
                            if title_node and comp_node:
                                title = (await title_node.inner_text()).strip()
                                company = (await comp_node.inner_text()).strip(",")
                                fingerprint = f"{title}-{company}".lower()
                                
                                if fingerprint not in seen_fingerprints:
                                    seen_fingerprints.add(fingerprint)
                                    loc_node = await card.query_selector(".cname bdi a:nth-of-type(2)")
                                    exp_node = await card.query_selector(".func-area-drn")
                                    skill_nodes = await card.query_selector_all(".label.label-default")
                                    
                                    all_jobs.append({
                                        "title": title, "company": company,
                                        "location": await loc_node.inner_text() if loc_node else city_name,
                                        "experience": await exp_node.inner_text() if exp_node else "N/A",
                                        "skills": ", ".join([await s.inner_text() for s in skill_nodes])
                                    })
                                    new_added += 1

                        if new_added == 0 and offset > 0: break
                        await asyncio.sleep(random.uniform(1, 2))

                    except: break

        await browser.close()
        
        if all_jobs:
            os.makedirs('data', exist_ok=True)
            with open('data/jobs_raw.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=all_jobs[0].keys())
                writer.writeheader(); writer.writerows(all_jobs)
            print(f"🏆 Total Unique Jobs: {len(all_jobs)}")

if __name__ == "__main__":
    asyncio.run(scrape_rozee_mega())