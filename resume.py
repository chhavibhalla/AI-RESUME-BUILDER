# import streamlit as st
# from api import generate_resume_summary
# from fpdf import FPDF
# import io

# FONT_PATH = "DejaVuSans.ttf"


# class ResumePDF(FPDF):
#     def header(self):
#         self.set_font("DejaVu", 'B', 18)
#         self.cell(0, 10, self.resume_data['name'], ln=True, align='C')

        
#         self.set_font("DejaVu", '', 12)
#         self.set_text_color(0, 0, 255)
#         contact = f"{self.resume_data['email']} | {self.resume_data['phone']} | {self.resume_data['linkedin']} | {self.resume_data['github']}"
#         self.multi_cell(0, 10, contact, align='C')
#         self.set_text_color(0, 0, 0)

#         self.ln(4)
#         self.line(10, self.get_y(), 200, self.get_y())
#         self.ln(5)

#     def section_title(self, title):
#         self.set_font("DejaVu", 'B', 14)
#         self.set_text_color(0, 0, 128)
#         self.cell(0, 10, title, ln=True)
#         self.set_text_color(0, 0, 0)

#     def section_body(self, content):
#         self.set_font("DejaVu", '', 12)
#         self.multi_cell(0, 8, content)
#         self.ln(2)

#     def generate(self, data):
#         self.resume_data = data
#         self.add_page()
#         self.set_auto_page_break(auto=True, margin=15)

#         self.section_title("Summary")
#         self.section_body(data["summary"])

#         self.section_title("Skills")
#         self.section_body(", ".join(data["skills"]))

#         self.section_title("Experience")
#         self.section_body(data["experience"])

#         self.section_title("Projects")
#         self.section_body(data["projects"])

#         self.section_title("Education")
#         self.section_body(data["education"])

#         pdf_bytes = self.output(dest='S').encode('latin1')
#         return io.BytesIO(pdf_bytes)

# def create_resume_pdf(resume_data):
#     pdf = ResumePDF()
#     pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
#     pdf.add_font("DejaVu", "B", FONT_PATH, uni=True)
#     return pdf.generate(resume_data)


# def show():
#     st.title(" AI Resume Builder")
#     st.caption("💡 Fill out the form and download your resume instantly!")

#     name = st.text_input("Full Name")
#     email = st.text_input("Email")
#     phone = st.text_input("Phone Number")
#     linkedin = st.text_input("LinkedIn (full URL)")
#     github = st.text_input("GitHub (full URL)")
#     skills = st.text_area("Skills (comma separated)")
#     experience = st.text_area("Work Experience")
#     projects = st.text_area("Projects")
#     education = st.text_area("Education")

#     summary = ""
#     pdf_buffer = None

#     if st.button(" Generate Resume Summary"):
#         if all([
#             name.strip(), email.strip(), phone.strip(), skills.strip(),
#             experience.strip(), linkedin.strip(), github.strip(),
#             projects.strip(), education.strip()
#         ]):
#             with st.spinner("Generating summary..."):
#                 try:
#                     summary = generate_resume_summary(
#                         name, email, phone, skills, experience,
#                         linkedin, github, projects, education
#                     )
#                     st.success(" Summary generated!")
#                     st.markdown(summary)
#                 except Exception as e:
#                     st.error(f" Gemini API Error: {e}")
#         else:
#             st.warning(" Please fill all fields.")

    
#     if summary:
#         resume_data = {
#             "name": name,
#             "email": email,
#             "phone": phone,
#             "linkedin": linkedin,
#             "github": github,
#             "summary": summary,
#             "skills": [s.strip() for s in skills.split(',')],
#             "experience": experience,
#             "projects": projects,
#             "education": education
#         }
#         pdf_buffer = create_resume_pdf(resume_data)

#     # Test mode / manual resume (for submission without form)
#     if not summary:
#         resume_data = {
#             "name": "Chhavi Bhalla",
#             "email": "bhallachhavi007@gmail.com",
#             "phone": "8708300000",
#             "linkedin": "https://linkedin.com/in/chhaviibhalla",
#             "github": "https://github.com/chhavibhalla",
#             "summary": "Motivated B.Tech student with experience in HTML/CSS and a passion for technology.",
#             "skills": ["HTML", "CSS", "Python", "C++", "Git"],
#             "experience": "Intern - Web Development, IGDTUW (2024)",
#             "projects": "She Sync - menstrual tracker app using HTML/CSS. Created responsive UI and logic.",
#             "education": "IGDTUW - B.Tech CSE (2024 2028), SDVM - CBSE (2024, 96%)"
#         }
#         pdf_buffer = create_resume_pdf(resume_data)

#     if pdf_buffer:
#         st.download_button(
#             label="⬇️ Download Resume PDF",
#             data=pdf_buffer,
#             file_name="resume_chha.pdf",
#             mime="application/pdf"
#         )
#         st.success(" Resume ready! Click to download.")


import streamlit as st
from api import generate_resume_summary
from fpdf import FPDF
import io
from database import save_resume_to_db # Import the database function

FONT_PATH = "DejaVuSans.ttf"

class ResumePDF(FPDF):
    """A class to handle the creation of the resume PDF."""
    def header(self):
        self.set_font("DejaVu", 'B', 18)
        self.cell(0, 10, self.resume_data['name'], ln=True, align='C')

        self.set_font("DejaVu", '', 12)
        self.set_text_color(0, 0, 255)
        contact = f"{self.resume_data['email']} | {self.resume_data['phone']} | {self.resume_data['linkedin']} | {self.resume_data['github']}"
        self.multi_cell(0, 10, contact, align='C')
        self.set_text_color(0, 0, 0)

        self.ln(4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def section_title(self, title):
        self.set_font("DejaVu", 'B', 14)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)

    def section_body(self, content):
        self.set_font("DejaVu", '', 12)
        self.multi_cell(0, 8, content)
        self.ln(2)

    def generate(self, data):
        self.resume_data = data
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)

        self.section_title("Summary")
        self.section_body(data.get("summary", " ")) # Use .get for safety

        self.section_title("Skills")
        self.section_body(", ".join(data.get("skills", [])))

        self.section_title("Experience")
        self.section_body(data.get("experience", " "))

        self.section_title("Projects")
        self.section_body(data.get("projects", " "))

        self.section_title("Education")
        self.section_body(data.get("education", " "))

        output = self.output(dest="S")
        pdf_bytes = output.encode("latin1") if isinstance(output, str) else output
        return io.BytesIO(pdf_bytes)


def create_resume_pdf(resume_data):
    """Creates a PDF object and generates the resume."""
    pdf = ResumePDF()
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "B", FONT_PATH, uni=True)
    return pdf.generate(resume_data)


def show():
    """Renders the Resume Maker page."""
    st.title("🎯 AI Resume Builder")
    st.caption("💡 Fill out the form, generate an AI summary (optional), and download your resume.")

    # --- Input Form ---
    with st.form("resume_form"):
        st.subheader("1. Your Details")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone Number*")
        with col2:
            linkedin = st.text_input("LinkedIn URL*")
            github = st.text_input("GitHub URL*")

        skills = st.text_area("Skills (comma separated)*")
        experience = st.text_area("Work Experience*")
        projects = st.text_area("Projects*")
        education = st.text_area("Education*")

        st.markdown("---")
        st.subheader("2. AI Summary (Optional)")
        generate_clicked = st.form_submit_button("⚡ Generate AI Summary")

    # --- Session State for Summary ---
    if 'generated_summary' not in st.session_state:
        st.session_state.generated_summary = ""

    is_form_complete = all([name, email, phone, skills, experience, linkedin, github, projects, education])

    if generate_clicked:
        if is_form_complete:
            with st.spinner("Generating summary..."):
                try:
                    st.session_state.generated_summary = generate_resume_summary(
                        name, email, phone, skills, experience,
                        linkedin, github, projects, education
                    )
                    st.success("✅ AI summary generated below!")
                except Exception as e:
                    st.error(f"Gemini API Error: {e}")
        else:
            st.warning("Please fill out all required fields marked with * before generating a summary.")

    # --- Display Final Resume and Download Button ---
    if is_form_complete:
        st.markdown("---")
        st.subheader("3. Download Your Resume")

        # Use the generated summary if available, otherwise use an empty string.
        final_summary = st.session_state.get('generated_summary', "")
        if final_summary:
             st.markdown("**Generated Summary:**")
             st.info(final_summary)

        resume_data = {
            "name": name, "email": email, "phone": phone, "linkedin": linkedin,
            "github": github, "summary": final_summary,
            "skills": [s.strip() for s in skills.split(',')],
            "experience": experience, "projects": projects, "education": education
        }

        pdf_buffer = create_resume_pdf(resume_data)

        # The on_click callback saves the data to the database before the download starts.
        st.download_button(
            label="⬇️ Download & Save to Profile",
            data=pdf_buffer,
            file_name=f"resume_{name.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            on_click=save_resume_to_db,
            args=(st.session_state.get('uid'), resume_data),
            disabled=('uid' not in st.session_state)
        )

        if 'uid' not in st.session_state:
            st.error("You must be logged in to save and download a resume.")
    else:
        st.info("Fill out all fields marked with * to create and download your resume.")
