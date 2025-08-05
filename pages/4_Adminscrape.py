import asyncio
import streamlit as st
import pandas as pd
import os
from helper_functions.scraper import scrape_url_data
from helper_functions.utility import check_password 

# Enable full-width layout
st.set_page_config(layout="wide")

# ✅ Require login
if not check_password():
    st.stop()

# ✅ Allow only admin
if st.session_state.get("role") != "Admin":
    st.error("🚫 Access denied: This page is for admin users only.")
    st.stop()

# ✅ Optional: show who is logged in
st.sidebar.markdown(f"👤 Logged in as: `{st.session_state.get('role', 'Unknown')}`")

# ----------------------
# Function to scrape CSV
# ----------------------
def scrape_from_csv(csv_path, progress_callback=None):
    df = pd.read_csv(csv_path)
    urls = df['URL'].dropna().tolist()
    scraped_data = asyncio.run(scrape_url_data(urls, progress_callback=progress_callback))
    return pd.DataFrame(scraped_data)


# ---------------------
# Main Admin Scrape UI
# ---------------------
def main():
    st.title("Admin: Scrape Course URLs")

    st.markdown("""
    **Purpose:**  
    This page allows admin to bulk-check all course URLs by scraping their page titles and snippets.  
    It helps identify broken or invalid links without having to click each one manually,  
    so that broken links can be easily updated in the system.
    """)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    original_csv = os.path.join(base_dir, 'courses.csv')
    scraped_csv = os.path.join(base_dir, 'courses_with_scraped_info.csv')

    if st.button("Scrape"):
        progress_bar = st.progress(0)
        status_text = st.empty()  # Placeholder to show live progress text

        def update_progress(p):
            progress_bar.progress(p)
            status_text.text(f"🏃‍♂️ Progress: {int(p * 100)}%")

        with st.spinner("🏃‍♂️ Scraping all course URLs, please wait..."):
            scraped_df = scrape_from_csv(original_csv, progress_callback=update_progress)
            scraped_df.to_csv(scraped_csv, index=False)

        st.success("✅ Scraping completed!")

        # Show the scraped data in a wide table
        st.dataframe(scraped_df, use_container_width=True, height=600)
    else:
        st.info("Click the 'Scrape' button to start scraping all course URLs from courses.csv.")


if __name__ == "__main__":
    main()