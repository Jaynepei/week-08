import streamlit as st
import os
from PIL import Image

# --- Page Config (must be at the very top) ---
st.set_page_config(page_title="Course Image Gallery", layout="wide")

# --- Page Title ---
st.title("🧭 About this Page")

# --- Introduction ---
st.write(
    "Welcome! This page provides an overview of the 14 **Competency Descriptors** "
    "to help you better understand the skills and knowledge required across different domains."
)

# --- Add subtle shadow styling ---
st.markdown("""
    <style>
    .stImage > img {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Expander for Explore Competencies ---
with st.expander("🗃️ Explore Competencies – Click to view all 14 competencies", expanded=False):
    st.write("Scroll through the images below to view each of the 14 competencies.")

    # --- Image Folder ---
    image_folder = os.path.join(os.path.dirname(__file__), "..", "images")

    # --- Image Filenames ---
    image_names = [
        f"C{str(i).zfill(2)}.jpg" if i <= 8 else f"C{str(i).zfill(2)}.png"
        for i in range(1, 15)
    ]

    # --- Layout: 2 images per row ---
    images_per_row = 2
    rows = [image_names[i:i + images_per_row] for i in range(0, len(image_names), images_per_row)]

    # --- Display Images ---
    for row in rows:
        cols = st.columns(len(row))
        for idx, img_name in enumerate(row):
            img_path = os.path.join(image_folder, img_name)
            if os.path.exists(img_path):
                with cols[idx]:
                    img = Image.open(img_path)
                    st.image(img, use_container_width=True)
            else:
                with cols[idx]:
                    st.warning(f"Missing: {img_name}")

# --- How to Use Section ---
st.markdown("### 🚀 How to Navigate")
st.write("1. Go to **Main** – You can ask the availabilty of the courses offered under CDP.")
st.write("2. Click **Send** – The app will generate a response based on your input.")
st.write("3. **View All Courses** – You can use the filters to explore learning opportunities by Competency and Proficiency Level.")



# import streamlit as st

# # region <--------- Streamlit App Configuration --------->
# st.set_page_config(
#     layout="centered",
#     page_title="My Streamlit App"
# )
# # endregion <--------- Streamlit App Configuration --------->

# st.title("About this App")

# st.write("This is a Streamlit App that demonstrates how to use the OpenAI API to generate text completions.")

# with st.expander("How to use this App"):
#     st.write("1. Enter your prompt in the text area.")
#     st.write("2. Click the 'Submit' button.")
#     st.write("3. The app will generate a text completion based on your prompt.")
