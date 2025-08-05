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

# --- Custom CSS for course title ---
st.markdown("""
    <style>
        .course-title {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 8px;
            font-size: 1.2rem;
            font-weight: bold;
            line-height: 1.4;
            height: 4.2em;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            margin-bottom: 0.8rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Load CSV Safely ---
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "..", "data", "courses.csv")

try:
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    # Rename columns for easier access
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

    # --- Display Cards (4 per row) ---
    cards_per_row = 4
    rows = [df.iloc[i:i + cards_per_row] for i in range(0, len(df), cards_per_row)]

    for row in rows:
        cols = st.columns(cards_per_row)
        for idx, (_, course) in enumerate(row.iterrows()):
            with cols[idx]:
                # Title with fixed height and style
                st.markdown(f"<div class='course-title'>{course['title']}</div>", unsafe_allow_html=True)

                # Content
                st.write(f"💡 **Competency:** {course.get('Competency', 'N/A')}")
                st.write(f"🎯 **Proficiency Level:** {course.get('Proficiency Level', 'N/A')}")
                st.write(f"🏫 **Provider:** {course.get('provider', 'N/A')}")
                st.write(f"🖥️ **Mode:** {course.get('mode', 'N/A')}")

                training_period = course.get("Training Period")
                if pd.isna(training_period) or str(training_period).strip().lower() == "nan":
                    st.write("🗓️ **Training Period:** N/A")
                else:
                    st.write(f"🗓️ **Training Period:** {training_period}")

                url = course.get("URL", "")
                if pd.notna(url) and str(url).strip().lower() not in ["", "nan"]:
                    st.markdown(f"🔗 [Course Link]({url})")

                st.markdown("&nbsp;", unsafe_allow_html=True)

        # Horizontal line after each row
        st.markdown("----")

except FileNotFoundError:
    st.error("❌ Could not find `courses.csv`. Make sure it's in the `/data` folder.")
except Exception as e:
    st.error("❌ An error occurred while loading the course data.")
    st.exception(e)




# import streamlit as st
# import pandas as pd
# import json

# st.set_page_config(page_title="View All Courses", page_icon="📚")
# st.title("📚 View All Courses")
 
# # 🔍 Search bar
# search_query = st.text_input("Search for a course by name, competency, proficiency, category, training mode or keyword:")

# # # Load the JSON file
# # filepath = './data/courses-full.json'
# # with open(filepath, 'r') as file:
# #     json_string = file.read()
# #     dict_of_courses = json.loads(json_string)
# #     print(dict_of_courses)

# # import pandas as pd

# filepath = './data/CDP2025_CATALOG (extract for AI).csv'

# # Load the CSV file into a DataFrame
# df = pd.read_csv(filepath)

# # Convert to a list of dictionaries (one per row)
# list_of_dicts = df.to_dict(orient='records')

# # Print the list of dictionaries
# print(list_of_dicts)

# # # Extract the value of the `dict_of_courses` dictionary
# # # If you are not sure what the dictionary looks like, you can print it out
# # list_of_dict = []
# # for course_name, details_dict in dict_of_courses.items():
# #     list_of_dict.append(details_dict)

# # # display the `dict_of_course` as a Pandas DataFrame
# # df = pd.DataFrame(list_of_dict)
# # df