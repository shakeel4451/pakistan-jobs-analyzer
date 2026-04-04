import asyncio
import csv
import random
from playwright.async_api import async_playwright

async def scrape_rozee_paginated(target_count=1000):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        all_jobs = []
        # Each page has ~20 jobs, so for 1000 jobs, we need ~50 pages
        pages_to_scrape = (target_count // 20) + 1 

        for pg in range(1, pages_to_scrape + 1):
            print(f"Injesting Page {pg}...")
            
            # Rozee pagination pattern: /q/all/pg/1, /q/all/pg/2, etc.
            url = f"https://www.rozee.pk/job/jsearch/q/all/pg/{pg}"
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                # Wait for at least one job card to appear
                await page.wait_for_selector(".job.Pjbs", timeout=10000)
                
                job_cards = await page.query_selector_all(".job.Pjbs")
                
                for card in job_cards:
                    title_elem = await card.query_selector("h3.s-18 bdi")
                    company_elem = await card.query_selector(".cname a:nth-of-type(1)")
                    location_elem = await card.query_selector(".cname a:nth-of-type(2)")
                    exp_elem = await card.query_selector(".func-area-drn")
                    salary_elem = await card.query_selector(".rz-salary + span")
                    date_elem = await card.query_selector(".rz-calendar + span")
                    skill_nodes = await card.query_selector_all(".label.label-default")
                    skills_list = [await s.inner_text() for s in skill_nodes]

                    all_jobs.append({
                        "title": await title_elem.inner_text() if title_elem else "N/A",
                        "company": (await company_elem.inner_text()).strip(",") if company_elem else "N/A",
                        "location": await location_elem.inner_text() if location_elem else "N/A",
                        "experience": await exp_elem.inner_text() if exp_elem else "N/A",
                        "salary": await salary_elem.inner_text() if salary_elem else "N/A",
                        "date_posted": await date_elem.inner_text() if date_elem else "N/A",
                        "skills": ", ".join(skills_list)
                    })

                print(f"Cumulative total: {len(all_jobs)} jobs extracted.")
                
                # Exit early if target reached
                if len(all_jobs) >= target_count:
                    break

                # Polite Delay: Random sleep to avoid rate-limiting/403 Forbidden
                await asyncio.sleep(random.uniform(1.5, 3.0))

            except Exception as e:
                print(f"Error on page {pg}: {e}")
                continue

        await browser.close()
        
        # Save Final Dataset
        if all_jobs:
            import os
            os.makedirs('data', exist_ok=True)
            with open('data/jobs_raw.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=all_jobs[0].keys())
                writer.writeheader()
                writer.writerows(all_jobs)
            print(f"✅ Mission Accomplished: {len(all_jobs)} records saved to data/jobs_raw.csv")

if __name__ == "__main__":
    # Change target_count to 2000 if needed
    asyncio.run(scrape_rozee_paginated(target_count=1000))