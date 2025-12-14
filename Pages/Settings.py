import streamlit as st

st.set_page_config(page_title="Settings", layout="wide")

if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("Access denied. Please log in first.")
    if st.button("Return to Login Page"):
        st.switch_page("Home.py")
    st.stop()

st.title("Application Settings")

st.write(f"Current user: *{st.session_state.username}*")

# 2️-   PROFILE PICTURE UPLOAD
st.subheader("Profile Picture")

# initialize storage
if "pfp" not in st.session_state:
    st.session_state.pfp = None

# Show current picture
if st.session_state.pfp is not None:
    st.image(st.session_state.pfp, width=150, caption="Your Profile Picture")
else:
    st.info("No profile picture uploaded yet.")

uploaded_pfp = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])

if uploaded_pfp:
    st.session_state.pfp = uploaded_pfp.read()
    st.success("Profile picture updated!")
    st.rerun()


if st.button("Remove Profile Picture"):
    st.session_state.pfp = None
    st.success("Profile picture removed.")
    st.rerun()




# 3️-  CHANGE PROFILE NAME
st.subheader("Profile Settings")

new_name = st.text_input("Update Display Name", st.session_state.username)

if st.button("Save Name"):
    if new_name.strip():
        st.session_state.username = new_name.strip()
        st.success("Display name updated successfully!")
    else:
        st.warning("Name cannot be empty.")

# RESET SESSION
st.subheader("System")

if st.button("Reset Session"):
    st.session_state.clear()
    st.success("Session has been reset. Please restart the application.")
