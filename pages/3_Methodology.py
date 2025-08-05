import streamlit as st
from PIL import Image

# Page config
st.set_page_config(page_title="Methodology", layout="wide")

st.title("📚 Methodology")

st.markdown("""
This project uses modern AI techniques and web technologies to create a smart chatbot for course recommendations. Below are the core components of our methodology:
""")

# Methodology sections
with st.expander("🔍 Natural Language Understanding (LLM)", expanded=False):
    st.markdown("""
    We use a **Large Language Model (LLM)** to interpret user queries. It extracts relevant course names, keywords, and competencies from natural language input.
    """)

with st.expander("💬 Conversational Interface (Chatbot)", expanded=False):
    st.markdown("""
    Streamlit powers the chat interface. Session state is used to manage conversation history and course recommendations interactively.
    """)

with st.expander("🔐 User Authentication", expanded=False):
    st.markdown("""
    Basic authentication is implemented using password input, controlled via `st.session_state` and checked against credentials stored securely in `.streamlit/secrets.toml`.
    """)

with st.expander("📊 Course Data Processing & Web Scraping", expanded=False):
    st.markdown("""
    Course data is stored in a **CSV file**. Upon user input, the chatbot retrieves and matches course details using keyword extraction and semantic similarity.  
    Additionally, an **admin-only web scraping tool** periodically crawls course URLs to validate and update course information by fetching page titles and snippets.  
    This automation helps identify broken or outdated links efficiently without manual checks.
    """)

with st.expander("🗂️ Conversation History Tracking", expanded=False):
    st.markdown("""
    The chatbot maintains a record of the entire dialogue using `st.session_state`. Each user input and the corresponding assistant response is appended to a list, 
    allowing the model to generate context-aware replies. This ensures the conversation remains coherent and personalized over multiple exchanges.
    """)

# Flowchart image
st.markdown("---")
st.subheader("📈 Flowchart illustrating the process flow for the chatbot use case")

try:
    image = Image.open("images/chatbot_flow.png")
    col1, col2, col3 = st.columns([1, 2, 1])  # Center the image
    with col2:
        st.image(image, caption="System Flowchart", use_container_width=True)
except FileNotFoundError:
    st.warning("⚠️ 'chatbot_flow.png' not found in the 'images/' folder. Please add it to display the diagram.")