# filename: utility.py
import streamlit as st  
import random  
import hmac  
  
# """  
# This file contains the common components used in the Streamlit App.  
# This includes the sidebar, the title, the footer, and the password check.  
# """

def check_password():
    """Login form using Streamlit session state and on_change (no rerun)."""
    USERS = st.secrets["users"]

    # Validate login on password submit
    def password_entered():
        username = st.session_state["username"]
        password = st.session_state["password"]

        if username == USERS["admin_username"] and password == USERS["admin_password"]:
            st.session_state["logged_in"] = True
            st.session_state["role"] = "Admin"
            del st.session_state["password"]  # Don’t store password
        elif username == USERS["user_username"] and password == USERS["user_password"]:
            st.session_state["logged_in"] = True
            st.session_state["role"] = "User"
            del st.session_state["password"]
        else:
            st.session_state["logged_in"] = False

    # Already logged in
    if st.session_state.get("logged_in"):
        return True

    st.title("🔐 Login Required")

    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password", on_change=password_entered)

    # Feedback
    if "logged_in" in st.session_state and not st.session_state["logged_in"]:
        st.error("Invalid username or password")

    return False


#old_check_password = check_password  # Keep the old function for reference
# def check_password():  
#     """Returns `True` if the user had the correct password."""  
#     def password_entered():  
#         """Checks whether a password entered by the user is correct."""  
#         if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):  
#             st.session_state["password_correct"] = True  
#             del st.session_state["password"]  # Don't store the password.  
#         else:  
#             st.session_state["password_correct"] = False  
#     # Return True if the passward is validated.  
#     if st.session_state.get("password_correct", False):  
#         return True  
#     # Show input for password.  
#     st.text_input(  
#         "Password", type="password", on_change=password_entered, key="password"  
#     )  
#     if "password_correct" in st.session_state:  
#         st.error("😕 Password incorrect")  
#     return False

