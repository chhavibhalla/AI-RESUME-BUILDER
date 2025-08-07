import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import re  

# --- Firebase Initialization ---
# This should only run once
if not firebase_admin._apps:
    # Use Streamlit secrets to securely store Firebase credentials
    cred = credentials.Certificate(dict(st.secrets["firebase_credentials"]))
    firebase_admin.initialize_app(cred)

# --- Email Format Validator ---
def is_valid_email(email):
    # Enforce at least 2 characters before the @ and a valid domain
    pattern = r'^(?!.*[.]{2})[a-zA-Z0-9](\.?[a-zA-Z0-9_-])*@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$'
    return re.match(pattern, email) is not None

# --- Authentication Functions ---

def sign_up(email, password):
    """Creates a new user with email and password."""
    try:
        user = auth.create_user(email=email, password=password)
        st.success(f"Account created successfully for {user.email}! Please proceed to the Sign In tab.")
        return True
    except Exception as e:
        st.error(f"Error creating account: {e}")
        return False

def sign_in(email, password):
    """Signs in a user with email and password."""
    try:
        user = auth.get_user_by_email(email)
        st.session_state['user_email'] = user.email
        return True
    except Exception as e:
        st.error(f"Error signing in: Invalid email or password.")
        return False

def sign_out():
    """Signs out the current user."""
    if 'user_email' in st.session_state:
        del st.session_state['user_email']
    st.success("You have been signed out.")

def show_auth_page():
    """Renders a unified Sign In / Sign Up page using tabs."""
    st.title("Welcome to Resumely")
    st.write("Please sign in or create an account to continue.")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        signin_tab, signup_tab = st.tabs(["**Sign In**", "**Sign Up**"])

        with signin_tab:
            with st.form("signin_form", clear_on_submit=True):
                email = st.text_input("Email", key="signin_email")
                password = st.text_input("Password", type="password", key="signin_password")
                signin_submitted = st.form_submit_button("Sign In", use_container_width=True)

            if signin_submitted:
                if email and password:
                    if sign_in(email, password):
                        st.rerun()
                else:
                    st.warning("Please enter both email and password.")

        with signup_tab:
            with st.form("signup_form", clear_on_submit=True):
                new_email = st.text_input("Email", key="signup_email")
                new_password = st.text_input("Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
                signup_submitted = st.form_submit_button("Create Account", use_container_width=True)

            if signup_submitted:
                if new_email and new_password and confirm_password:
                    if not is_valid_email(new_email):
                        st.error("Invalid email format. Please enter a valid email address.")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        sign_up(new_email, new_password)
                else:
                    st.warning("Please fill out all fields.")
