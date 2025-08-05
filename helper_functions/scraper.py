import nest_asyncio
import asyncio
import pandas as pd
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

nest_asyncio.apply()  # allows nested event loops, useful if needed

async def scrape_url_data(urls, progress_callback=None):
    results = []
    total = len(urls)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for i, url in enumerate(urls):
            try:
                await page.goto(url, timeout=30000)
                title = await page.title()
                body = await page.text_content("body")
                snippet = (body or "").strip().replace('\n', ' ')[:300]
                results.append({
                    "URL": url,
                    "title": title,
                    "snippet": snippet
                })
            except Exception as e:
                results.append({
                    "URL": url,
                    "title": "Error",
                    "snippet": str(e)
                })

            if progress_callback:
                progress_callback((i + 1) / total)  # update progress

        await browser.close()
    return results

def scrape_from_csv(file_path, progress_callback=None):
    # Read URLs from csv
    df = pd.read_csv(file_path)
    urls = df['URL'].dropna().tolist()  # get url column, remove empty
    # Run async scraping
    scraped_data = asyncio.run(scrape_url_data(urls, progress_callback=progress_callback))
    # Return scraped data as DataFrame for easier use later
    return pd.DataFrame(scraped_data)