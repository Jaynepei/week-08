import streamlit as st
import pandas as pd
import os
 
# --- Page Config ---
st.set_page_config(
    page_title="View All Courses",
    page_icon="📚",
    layout="wide"
)
 
st.title("📚 View All Courses")
 
# --- Custom CSS ---
st.markdown("""
    <style>
        .course-title {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 8px;
            font-size: 0.9rem; /* 10% smaller */
            font-weight: bold;
            line-height: 1.4;
            height: 80px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: left;
            text-align: left;
            margin-bottom: 0.8rem;
        }
        .course-detail {
            font-size: 0.875rem; /* slightly smaller detail text */
            line-height: 1.5;
            margin-bottom: 4px;
        }
        .course-link {
            font-size: 0.875rem;
        }
    </style>
""", unsafe_allow_html=True)
 
# --- Load CSV ---
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "..", "data", "courses.csv")
 
try:
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
 
    # Rename columns
    df.rename(columns={
        "Course Title": "title",
        "Course Provider": "provider",
        "Training Mode": "mode",
        " Cost ": "cost"
    }, inplace=True)
 
    # --- Filters ---
    search_query = st.text_input("🔍 Search for a course by title, category, or keyword:")
 
    competency_options = df["Competency"].dropna().unique().tolist()
    competency_options.sort()
    selected_competency = st.selectbox("💡 Filter by Competency:", ["All"] + competency_options)
 
    proficiency_options = df["Proficiency Level"].dropna().unique().tolist()
    proficiency_options.sort()
    selected_level = st.selectbox("🎯 Filter by Proficiency Level:", ["All"] + proficiency_options)
 
    # --- Apply Filters ---
    if search_query:
        query = search_query.lower()
        df = df[df.apply(lambda row: query in str(row).lower(), axis=1)]
 
    if selected_competency != "All":
        df = df[df["Competency"] == selected_competency]
 
    if selected_level != "All":
        df = df[df["Proficiency Level"] == selected_level]
 
    # --- Results Count ---
    st.markdown(f"### Showing {len(df)} course(s)")
 
    # --- Display Cards ---
    cards_per_row = 4
    rows = [df.iloc[i:i + cards_per_row] for i in range(0, len(df), cards_per_row)]
 
    for row in rows:
        cols = st.columns(cards_per_row)
        for idx, (_, course) in enumerate(row.iterrows()):
            with cols[idx]:
                # Title box
                st.markdown(f"<div class='course-title'>{course['title']}</div>", unsafe_allow_html=True)
 
                # Details with smaller font
                st.markdown(f"<div class='course-detail'>💡 <strong>Competency:</strong> {course.get('Competency', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='course-detail'>🎯 <strong>Proficiency Level:</strong> {course.get('Proficiency Level', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='course-detail'>🏫 <strong>Provider:</strong> {course.get('provider', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='course-detail'>🖥️ <strong>Mode:</strong> {course.get('mode', 'N/A')}</div>", unsafe_allow_html=True)
 
                training_period = course.get("Training Period")
                training_text = "N/A" if pd.isna(training_period) or str(training_period).strip().lower() == "nan" else training_period
                st.markdown(f"<div class='course-detail'>🗓️ <strong>Training Period:</strong> {training_text}</div>", unsafe_allow_html=True)
 
                url = course.get("URL", "")
                if pd.notna(url) and str(url).strip().lower() not in ["", "nan"]:
                    st.markdown(f"<div class='course-link'>🔗 <a href='{url}' target='_blank'>Course Link</a></div>", unsafe_allow_html=True)
 
                st.markdown("&nbsp;", unsafe_allow_html=True)
 
        st.markdown("----")
 
except FileNotFoundError:
    st.error("❌ Could not find `courses.csv`. Make sure it's in the `/data` folder.")
except Exception as e:
    st.error("❌ An error occurred while loading the course data.")
    st.exception(e)
 