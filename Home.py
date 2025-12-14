import streamlit as st
import json
import os

st.set_page_config(page_title="Login", layout="centered")

USERS_FILE = "users.json"

# --- LOGOUT HANDLER FUNCTION ---
def logout():
    """Clears the session state to log the user out."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    # Updated to the current, recommended function
    st.rerun()
# --------------------------------

# LOAD USERS FROM FILE
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}

# SAVE USERS TO FILE
def save_users(users_dict):
    with open(USERS_FILE, "w") as file:
        json.dump(users_dict, file, indent=4)

# Load persistent users
persistent_users = load_users()

# SESSION INITIALIZATION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# --- CONDITIONAL LOGOUT SECTION ---
if st.session_state.logged_in:
    # Display message and logout button if the user is logged in
    st.info(f"Welcome back, **{st.session_state.username}**! You are already signed in.")
    
    # Place the logout button here
    if st.button("Log Out"):
        logout()
    
    # Stop the login/registration forms from showing if the user is already logged in
    st.stop()
# -----------------------------------

# Tabs for login and registration
login_tab, register_tab = st.tabs(["Login", "Register"])

# LOGIN SECTION
with login_tab:
    st.subheader("Sign In")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if username in persistent_users and persistent_users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("You are now logged in!")
            # Updated to the current, recommended function
            st.rerun() 
        else:
            st.error("Incorrect username or password.")

# REGISTRATION SECTION
with register_tab:
    st.subheader("Create an Account")

    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")
    confirm = st.text_input("Re-enter Password", type="password")

    if st.button("Register"):
        if not new_user or not new_pass:
            st.warning("Please fill in all fields.")
        elif new_pass != confirm:
            st.error("Passwords do not match.")
        elif new_user in persistent_users:
            st.error("That username already exists.")
        else:
            # Save new user permanently
            persistent_users[new_user] = new_pass
            save_users(persistent_users)

            st.success("Account created successfully! Switch to Login tab to sign in.") 