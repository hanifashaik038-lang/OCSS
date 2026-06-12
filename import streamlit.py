import streamlit as st
import os
from pathlib import Path
from datetime import date

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="OCSS - One Click Semester Setup",
    page_icon="📚",
    layout="wide"
)

BASE_DIR = Path("ocss_data")
BASE_DIR.mkdir(exist_ok=True)

# -----------------------------
# Session State
# -----------------------------
if "subjects" not in st.session_state:
    st.session_state.subjects = []

if "notes" not in st.session_state:
    st.session_state.notes = {}

if "study_hours" not in st.session_state:
    st.session_state.study_hours = 0

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📚 OCSS")
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Semester Setup",
        "Subject Organizer",
        "Notes",
        "Planner",
        "Mock Test Generator",
        "Progress"
    ]
)

# ======================================================
# DASHBOARD
# ======================================================

if page == "Dashboard":

    st.title("🎓 OCSS - One Click Semester Setup")

    c1, c2, c3 = st.columns(3)

    c1.metric("Subjects", len(st.session_state.subjects))
    c2.metric("Study Hours", st.session_state.study_hours)
    c3.metric("Notes", len(st.session_state.notes))

    st.divider()

    st.subheader("Today's Goals")

    st.checkbox("Complete revision")
    st.checkbox("Read lecture notes")
    st.checkbox("Attempt mock test")
    st.checkbox("Upload new study material")

    st.divider()

    st.subheader("Recent Subjects")

    if st.session_state.subjects:
        for s in st.session_state.subjects:
            st.write("✅", s)
    else:
        st.info("No subjects added yet.")

# ======================================================
# SEMESTER SETUP
# ======================================================

elif page == "Semester Setup":

    st.title("⚡ One Click Semester Setup")

    semester = st.text_input("Semester Name")

    subject_input = st.text_area(
        "Enter Subjects (one per line)"
    )

    exam_date = st.date_input(
        "Exam Date",
        value=date.today()
    )

    if st.button("Create Semester"):

        subjects = [
            s.strip()
            for s in subject_input.splitlines()
            if s.strip()
        ]

        st.session_state.subjects = subjects

        semester_path = BASE_DIR / semester

        semester_path.mkdir(parents=True, exist_ok=True)

        for sub in subjects:

            (semester_path / sub).mkdir(
                parents=True,
                exist_ok=True
            )

        st.success("Semester created successfully!")

        st.write("Exam Date:", exam_date)

# ======================================================
# SUBJECT ORGANIZER
# ======================================================

elif page == "Subject Organizer":

    st.title("📂 Subject Organizer")

    if not st.session_state.subjects:
        st.warning("Create a semester first.")
    else:

        subject = st.selectbox(
            "Choose Subject",
            st.session_state.subjects
        )

        uploaded = st.file_uploader(
            "Upload Files",
            accept_multiple_files=True
        )

        if uploaded:

            folder = BASE_DIR / "Uploads" / subject
            folder.mkdir(parents=True, exist_ok=True)

            for file in uploaded:

                with open(folder / file.name, "wb") as f:
                    f.write(file.read())

            st.success("Files uploaded successfully.")

        folder = BASE_DIR / "Uploads" / subject

        if folder.exists():

            st.subheader("Uploaded Files")

            for file in os.listdir(folder):
                st.write("📄", file)

# ======================================================
# NOTES
# ======================================================

elif page == "Notes":

    st.title("📝 Smart Notes")

    if not st.session_state.subjects:
        st.warning("Add subjects first.")

    else:

        subject = st.selectbox(
            "Subject",
            st.session_state.subjects
        )

        note = st.text_area("Write Notes")

        if st.button("Save Note"):

            st.session_state.notes[subject] = note

            st.success("Saved!")

        if subject in st.session_state.notes:

            st.subheader("Current Note")

            st.write(
                st.session_state.notes[subject]
            )

# ======================================================
# PLANNER
# ======================================================

elif page == "Planner":

    st.title("📅 Study Planner")

    task = st.text_input("Today's Task")

    deadline = st.date_input("Deadline")

    if st.button("Add Task"):

        st.success(
            f"Task '{task}' added with deadline {deadline}"
        )

    st.divider()

    hours = st.slider(
        "Hours Studied Today",
        0,
        15,
        0
    )

    if st.button("Save Study Hours"):

        st.session_state.study_hours += hours

        st.success("Hours saved!")

# ======================================================
# MOCK TEST
# ======================================================

elif page == "Mock Test Generator":

    st.title("🧪 AI Mock Test Generator")

    marks = st.selectbox(
        "Total Marks",
        [20, 50, 75, 100]
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    mode = st.selectbox(
        "Paper Type",
        [
            "MCQs",
            "Short Answers",
            "Long Answers",
            "Mixed"
        ]
    )

    questions = st.slider(
        "Number of Questions",
        5,
        100,
        20
    )

    if st.button("Generate Mock Test"):

        st.success(
            "In the full version, AI will generate the paper from uploaded documents."
        )

        st.write("Marks:", marks)
        st.write("Difficulty:", difficulty)
        st.write("Format:", mode)
        st.write("Questions:", questions)

# ======================================================
# PROGRESS
# ======================================================

elif page == "Progress":

    st.title("📊 Progress Dashboard")

    st.metric(
        "Total Study Hours",
        st.session_state.study_hours
    )

    st.metric(
        "Subjects",
        len(st.session_state.subjects)
    )

    st.metric(
        "Notes Saved",
        len(st.session_state.notes)
    )

    st.progress(
        min(
            st.session_state.study_hours / 100,
            1.0
        )
    )

    st.write(
        "Keep going! Build on your progress every day."
    )
    