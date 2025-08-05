import streamlit as st
import pandas as pd
from logics.customer_query_handler import process_user_message
from helper_functions.utility import check_password 

# Streamlit app config
st.set_page_config(
    page_title="CDP Courses Chatbot",
    layout="wide",
)

if not check_password():
    st.stop()

st.title("Courses for Finance Professionals")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant for course recommendations."}
    ]

if "course_details" not in st.session_state:
    st.session_state.course_details = []

# 1. Input form (at the bottom)
with st.form(key="course_form", clear_on_submit=True):
    user_input = st.text_area("Ask something about our available courses:", height=150)
    submitted = st.form_submit_button("Send")

# 2. Process user input BEFORE showing chat history
if submitted and user_input:
    reply, course_details = process_user_message(st.session_state.chat_history, user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.session_state.course_details = course_details
    st.toast("Response generated.")

# 3. Display chat history (above the input form)
st.markdown("---")
st.subheader("Your guide to CDP courses for Finance Professionals")
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='background:#DCF8C6;padding:8px;border-radius:8px;margin:5px 0;'>"
            f"<b>You:</b> {msg['content']}</div>",
            unsafe_allow_html=True
        )
    elif msg["role"] == "assistant":
        st.markdown(
            f"<div style='background:#ECECEC;padding:8px;border-radius:8px;margin:5px 0;'>"
            f"<b>Bot:</b> {msg['content']}</div>",
            unsafe_allow_html=True
        )

# 4. Show matched course details
st.markdown("---")
st.subheader("Matched Course Details")

course_details = st.session_state.get("course_details", [])

if course_details:
    df = pd.DataFrame(course_details)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No course details to display.")

