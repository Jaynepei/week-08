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


#A detailed page outlining the project scope, objectives, data sources, and features.

# Project Overview
st.header("Project Overview")
st.write("""
Welcome to the *Courses for Finance Professionals Chatbot**! This project is designed to 
streamline the process of discovering relevant training courses tailored to the competencies 
and proficiency levels required of finance professionals. By providing an interactive chatbot interface, 
users can quickly receive personalised guidance and explore detailed information about available courses.
Whether you're a new joiner or an experienced officer, the chatbot supports your learning journey by helping you 
identify the right courses to build and strengthen your skills at every stage.""")

# Project Scope
st.header("Project Scope")
st.write("""
This project consists of two primary components:

**Conversational Assistant**
An intelligent chatbot that leverages conversation history to provide personalised guidance. It uses a large language model (LLM) to understand user inputs and recommend relevant courses tailored to the user’s competencies, interests, and career development needs.
**Courses Display Interface**
A dynamic, user-friendly interface that presents course information through:
1. LLM-Powered Course Table: A searchable and filterable table that displays course details based on user queries, allowing for easy comparison and exploration.
2. Course Tiles View: A visually engaging, tile-based layout that showcases courses by category or keyword. This makes it easy for users to browse and quickly identify relevant training opportunities.
The goal of this project is to empower finance professionals with the tools and information they need to make informed training decisions, supporting continuous learning and professional growth throughout their career journey.
""")

# Objectives
st.header("Project Objectives")
st.write("""
1. **User Empowerment**: Equip finance professionals with timely, relevant course information to support their upskilling and career development decisions.

2. **Personalised Recommendations**: Leverage conversational AI and LLM capabilities to provide tailored course suggestions based on each user’s competencies and needs.

3. **Information Accessibility**: Present course data in a clear and intuitive format—through searchable tables and visual tiles—ensuring ease of use for all users, regardless of technical background.
""")

# Data Sources
st.header("Data Sources")
st.write("""
This application draws from multiple structured and dynamic sources to ensure relevant, accurate, and contextual course recommendations:

Course Dataset: A comprehensive list of internal training courses, each tagged to specific competencies and mapped to the relevant proficiency levels. This dataset enables targeted course suggestions that align with the user’s developmental stage.

Competency-Proficiency Framework: A structured reference that outlines key competencies required by finance professionals, each accompanied by detailed descriptions for proficiency levels ranging from Level 1 (Foundational) to Level 5 (Master). This framework helps the chatbot explain what each level entails and recommend suitable courses that support progression across the levels.

User Input: The chatbot uses a large language model (LLM) to interpret and respond to user queries. By understanding natural language inputs, it can identify the relevant competency or course of interest, and over time, refine its responses based on repeated interactions and patterns.
""")

# Features
st.header("Features")

st.subheader("Courses for Finance Professionals Chatbot")
st.write("""
- **Natural Language Understanding**: The chatbot uses a large language model (LLM) to interpret user queries related to training needs, such as competencies, course titles, or proficiency levels.

- **Interactive Interface**: Users can engage in a seamless, chat-based interaction to explore relevant courses, making the discovery process intuitive and user-friendly.

- **Conversation History**: The chatbot retains context from previous interactions within the same session, allowing for more coherent and continuous guidance across multiple queries.

- **Personalised Guidance**: Based on user input and mapped competencies, the chatbot recommends suitable courses aligned with the user’s current proficiency level and learning objectives.

- **Built-in Moderation for Safe Interactions**: Ensures conversations are safe and appropriate by filtering harmful or inappropriate inputs and outputs in real time.

""")

st.subheader("Course Tiles Dashboard")
st.write("""
- **Visual Overview**: Courses are displayed in a clean, tile-based layout for easy browsing.

- **Filter Functionality**: Users can filter courses by competency, proficiency level, or course name to quickly narrow down their options.

- **Interactive Exploration**: Each tile provides key information about the course, helping users make quick comparisons and informed decisions at a glance.

- **Direct Links & Resources**: Access course brochures, registration pages, or contact info directly from each tile.
         
 """)