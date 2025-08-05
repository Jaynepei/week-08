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
# --- Project Overview ---
st.header("Project Overview")
st.markdown("""
<div style="max-width: 1100px; line-height:1.6; font-size:16px;">
Welcome to the <em>Courses for Finance Professionals Chatbot</em>! This project is designed to 
streamline the process of discovering relevant training courses tailored to the competencies 
and proficiency levels required of finance professionals. By providing an interactive chatbot interface, 
users can quickly receive personalised guidance and explore detailed information about available courses.  
Whether you're a new joiner or an experienced officer, the chatbot supports your learning journey by helping you 
identify the right courses to build and strengthen your skills at every stage.

---

In addition to the chatbot for end users, the system includes a secure admin-only dashboard with 
a built-in <strong>web scraping tool</strong>. This tool enables administrators to:

- Automatically check the validity of course URLs listed in the database  
- Fetch and display page titles and content snippets for easy review  
- Identify broken or outdated links without needing to click each URL manually  
- View progress updates via a progress bar with live status and visual feedback  
- Export the latest scraped results to a CSV file for future reference  

This functionality helps maintain high data quality and ensures users always have access to accurate course links.
</div>
""", unsafe_allow_html=True)

# --- Project Scope ---
st.header("Project Scope")
st.markdown("""
<div style="max-width: 1100px; line-height:1.6; font-size:16px;">
This project consists of two primary components, designed to serve both regular users and administrators:
<br><br>
<strong>Conversational Assistant (for Users & Admins)</strong><br>
An intelligent chatbot that leverages conversation history to provide personalised guidance.  
It uses a large language model (LLM) to understand user inputs and recommend relevant courses tailored to the user’s competencies, interests, and career development needs.
<br><br>
<strong>Courses Display Interface (for Users & Admins)</strong><br>
A dynamic, user-friendly interface that presents course information through:
<ol>
<li><strong>LLM-Powered Course Table</strong> – A searchable and filterable table that displays course details based on user queries, allowing for easy comparison and exploration.</li>
<li><strong>Course Tiles View</strong> – A visually engaging, tile-based layout that showcases courses by category or keyword, making it easy for users to browse and identify relevant training opportunities.</li>
</ol>
<br>
<strong>Admin-Only Web Scraping Dashboard</strong><br>
A secure section accessible only to admins that includes:
<ul>
<li>A scraping tool that automatically extracts course page titles and summaries from URLs listed in the dataset</li>
<li>Real-time progress updates with a visual progress bar and animated status indicator</li>
<li>CSV export functionality for scraped data, helping admins identify broken links or outdated content</li>
<li>A built-in login system to restrict access to scraping features and ensure data integrity</li>
</ul>
<br>
The goal of this project is to empower finance professionals with the tools and information they need to make informed training decisions, while also equipping administrators with backend tools to maintain course data accuracy and quality.
</div>
""", unsafe_allow_html=True)

# --- Project Objectives ---
st.header("Project Objectives")
st.markdown("""
<div style="max-width: 1100px; line-height:1.6; font-size:16px;">
1. <strong>User Empowerment</strong>: Equip finance professionals with timely, relevant course information to support their upskilling and career development decisions.<br><br>
2. <strong>Personalised Recommendations</strong>: Leverage conversational AI and LLM capabilities to provide tailored course suggestions based on each user’s competencies and needs.<br><br>
3. <strong>Information Accessibility</strong>: Present course data in a clear and intuitive format—through searchable tables and visual tiles—ensuring ease of use for all users, regardless of technical background.<br><br>
4. <strong>Data Accuracy & Maintenance (Admin Only)</strong>: Provide administrators with a secure web scraping tool to automatically verify course URLs, detect broken or outdated links, and maintain the integrity of the course database.
</div>
""", unsafe_allow_html=True)

# --- Data Sources ---
st.header("Data Sources")
st.markdown("""
<div style="max-width: 1100px; line-height:1.6; font-size:16px;">
This application draws from multiple structured and dynamic sources to ensure relevant, accurate, and contextual course recommendations:

<ul>
<li><strong>Course Dataset</strong>: A comprehensive list of internal training courses, each tagged to specific competencies and mapped to the relevant proficiency levels. This dataset enables targeted course suggestions that align with the user’s developmental stage.</li>

<li><strong>Competency-Proficiency Framework</strong>: A structured reference that outlines key competencies required by finance professionals, each accompanied by detailed descriptions for proficiency levels ranging from Level 1 (Foundational) to Level 5 (Master). This framework helps the chatbot explain what each level entails and recommend suitable courses that support progression across the levels.</li>

<li><strong>User Input</strong>: The chatbot uses a large language model (LLM) to interpret and respond to user queries. By understanding natural language inputs, it can identify the relevant competency or course of interest, and over time, refine its responses based on repeated interactions and patterns.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# --- Features ---
st.header("Features")

st.subheader("Courses for Finance Professionals Chatbot (User & Admin)")
st.markdown("""
<div style="max-width: 1100px; line-height:1.6; font-size:16px;">
<ul>
<li><strong>Natural Language Understanding</strong>: The chatbot uses a large language model (LLM) to interpret user queries related to training needs, such as competencies, course titles, or proficiency levels.</li>

<li><strong>Interactive Interface</strong>: Users can engage in a seamless, chat-based interaction to explore relevant courses, making the discovery process intuitive and user-friendly.</li>

<li><strong>Conversation History</strong>: The chatbot retains context from previous interactions within the same session, allowing for more coherent and continuous guidance across multiple queries.</li>

<li><strong>Personalised Guidance</strong>: Based on user input and mapped competencies, the chatbot recommends suitable courses aligned with the user’s current proficiency level and learning objectives.</li>

<li><strong>Built-in Moderation for Safe Interactions</strong>: Ensures conversations are safe and appropriate by filtering harmful or inappropriate inputs and outputs in real time.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.subheader("Course Tiles Dashboard")
st.markdown("""
<div style="max-width: 1100px; line-height:1.6; font-size:16px;">
<ul>
<li><strong>Visual Overview</strong>: Courses are displayed in a clean, tile-based layout for easy browsing.</li>

<li><strong>Filter Functionality</strong>: Users can filter courses by competency, proficiency level, or course name to quickly narrow down their options.</li>

<li><strong>Interactive Exploration</strong>: Each tile provides key information about the course, helping users make quick comparisons and informed decisions at a glance.</li>

<li><strong>Direct Links & Resources</strong>: Access course brochures, registration pages, or contact info directly from each tile.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.subheader("Admin Web Scraping Tool (Admin Only)")
st.markdown("""
<div style="max-width: 1100px; line-height:1.6; font-size:16px;">
<ul>
<li><strong>Automated URL Verification</strong>: Bulk-scrape course URLs to retrieve page titles and snippets, helping identify broken or outdated links without manual checking.</li>

<li><strong>Progress Tracking</strong>: Visual progress bar and status updates during scraping to monitor the process efficiently.</li>

<li><strong>Data Maintenance</strong>: Export scraped results to CSV for easy review and updating of course links in the system.</li>

<li><strong>Secure Access</strong>: Restricted to admin users with login credentials to ensure data security and operational control.</li>
</ul>
</div>
""", unsafe_allow_html=True)
