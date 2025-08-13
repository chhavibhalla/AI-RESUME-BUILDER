import streamlit as st
from database import get_user_profile, update_user_profile, get_user_resumes_from_db
from resume import create_resume_pdf

def show():
    """Renders the user's profile page with a modern, interactive UI."""
    st.title("👤 My Profile")
    st.markdown("---")

    if 'uid' not in st.session_state:
        st.error("Could not identify user. Please sign in again.")
        return

    uid = st.session_state['uid']
    profile_data = get_user_profile(uid)

    if not profile_data:
        st.warning("Could not load profile data. Please try again.")
        return

    # --- Main Layout: Two Columns ---
    col1, col2 = st.columns([1, 2], gap="large")

    # --- Column 1: User Details & Edit Form ---
    with col1:
        st.subheader("Your Details")
        with st.container(border=True):
            st.write(f"**📧 Email:** {profile_data.get('email', 'N/A')}")
            st.write(f"**👤Name:** {profile_data.get('displayName', 'N/A')}")

        with st.expander("✏️ Change Your Name"):
            with st.form("update_name_form"):
                new_name = st.text_input("New Display Name", value=profile_data.get('displayName', ''))
                submitted = st.form_submit_button("Save Name")
                if submitted and new_name:
                    update_user_profile(uid, {'displayName': new_name})
                    st.rerun()

    # --- Column 2: Resume History ---
    with col2:
        st.subheader("📄 Your Resume History")
        st.caption("Click on a resume from the list below to view its details and download it.")
        
        user_resumes = get_user_resumes_from_db(uid)

        if not user_resumes:
            st.info("You haven't generated any resumes yet. Go to the 'Resume Maker' to create one!")
        else:
            # Initialize session state to store the selected resume's data
            if 'selected_resume_details' not in st.session_state:
                st.session_state.selected_resume_details = None

            # Create a list of resume names for the selectbox
            resume_options = []
            for resume in user_resumes:
                date_str = resume.get('created_at').strftime('%b %d, %Y') if resume.get('created_at') else "N/A"
                option_label = f"{resume.get('name', 'Untitled')} ({date_str})"
                resume_options.append(option_label)
            
            # Use a selectbox for a clean, dropdown-style list
            selected_option = st.selectbox(
                "Select a resume to view",
                options=resume_options,
                index=None, # No default selection
                placeholder="Choose a resume..."
            )

            # Find the full resume data that corresponds to the selected option
            if selected_option:
                selected_index = resume_options.index(selected_option)
                selected_resume_data = user_resumes[selected_index]
                
                # Display the details in a styled container
                with st.container(border=True):
                    st.markdown(f"#### Details for '{selected_resume_data.get('name')}'")
                    st.text("Summary:")
                    st.info(f"*{selected_resume_data.get('summary', 'No summary available.')}*")

                    pdf_buffer = create_resume_pdf(selected_resume_data['resume_data'])
                    st.download_button(
                        label="⬇️ Download This Resume as PDF",
                        data=pdf_buffer,
                        file_name=f"resume_{selected_resume_data.get('name', 'resume').replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
