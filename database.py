import streamlit as st
import firebase_admin
from firebase_admin import firestore, auth

def get_db():
    """Returns the Firestore client."""
    if not firebase_admin._apps:
        cred = firebase_admin.credentials.Certificate(dict(st.secrets["firebase_credentials"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

def create_user_profile_if_not_exists(uid, email):
    """Creates a user profile document if it doesn't already exist."""
    db = get_db()
    user_ref = db.collection('users').document(uid)
    if not user_ref.get().exists:
        # Set a default displayName based on the email prefix
        default_name = email.split('@')[0]
        user_ref.set({
            'email': email,
            'displayName': default_name, # Add a default display name
            'created_at': firestore.SERVER_TIMESTAMP
        })

def get_user_profile(uid):
    """Fetches a user's profile data from Firestore."""
    db = get_db()
    user_ref = db.collection('users').document(uid)
    return user_ref.get().to_dict()

def update_user_profile(uid, new_data):
    """Updates a user's profile data in Firestore."""
    try:
        db = get_db()
        user_ref = db.collection('users').document(uid)
        user_ref.update(new_data)
        st.toast("✅ Profile updated successfully!")
        return True
    except Exception as e:
        st.error(f"Failed to update profile: {e}")
        return False

def save_resume_to_db(uid, resume_data):
    """Saves a generated resume's data for the user."""
    try:
        db = get_db()
        resume_ref = db.collection('users').document(uid).collection('resumes').document()
        resume_ref.set({
            'name': resume_data.get('name', 'N/A'),
            'summary': resume_data.get('summary', ''),
            'created_at': firestore.SERVER_TIMESTAMP,
            'resume_data': resume_data
        })
        st.toast("✅ Resume saved to your profile!")
    except Exception as e:
        st.error(f"Failed to save resume: {e}")

def get_user_resumes_from_db(uid):
    """Fetches all resumes for a given user from Firestore."""
    try:
        db = get_db()
        resumes_ref = db.collection('users').document(uid).collection('resumes').order_by(
            'created_at', direction=firestore.Query.DESCENDING
        ).stream()
        return [resume.to_dict() for resume in resumes_ref]
    except Exception as e:
        st.error(f"Could not fetch resumes: {e}")
        return []
