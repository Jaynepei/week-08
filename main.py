# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
# from helper_functions import llm
from logics.customer_query_handler import process_user_message
### Import the utility function to check password
from helper_functions.utility import check_password 

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    page_title="CDP Courses Chatbot",
    layout="wide",
)
# endregion <--------- Streamlit App Configuration --------->

 # Check if the password is correct.  
if not check_password():  
     st.stop()

### end

st.title("Courses for Finance Professionals")

# Initialize conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant for course recommendations."}
    ]

if "course_details" not in st.session_state:
    st.session_state.course_details = []

# Display full chat history
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

# Input form
with st.form(key="course_form"):
    user_input = st.text_area("Ask something about our available courses:", height=150)
    submitted = st.form_submit_button("Send")


if submitted and user_input:
    # Call your logic function (single-turn, but we still track chat)
    reply, course_details = process_user_message(st.session_state.chat_history, user_input)
    st.session_state.course_details = course_details
    # Update chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    st.session_state.course_details = course_details

    st.toast("Response generated.")
    st.rerun()


# Display the matched course details nicely
# Important: `course_details` variable is only defined if user submitted input,
# so check carefully or you might get a NameError when loading page initially.
st.markdown("---")
st.subheader("Matched Course Details")

course_details = st.session_state.get("course_details", [])

if course_details and len(course_details) > 0:
    df = pd.DataFrame(course_details)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No course details to display.")
