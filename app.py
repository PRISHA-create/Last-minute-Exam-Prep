import streamlit as st
import pandas as pd

from utils.data_loader import load_all_data
from utils.recommender import get_topic_recommendations
from utils.study_plan import create_study_plan

st.set_page_config(
    page_title="Last-Minute Revision Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Last-Minute Exam Revision Assistant")
st.write(
    "This app helps college students focus on important topics instead of "
    "wasting time on less important material."
)

subjects, topics, past_papers, student_marks = load_all_data()

student_name = st.text_input(
    "Enter your name",
    value="Riya"
)

subject_options = subjects["subject_name"].tolist()

selected_subject_name = st.selectbox(
    "Select subject",
    subject_options
)

selected_subject = subjects[
    subjects["subject_name"] == selected_subject_name
].iloc[0]

subject_id = selected_subject["subject_id"]
exam_date = pd.to_datetime(selected_subject["exam_date"])
days_left = max((exam_date - pd.Timestamp.today()).days, 0)

st.info(f"Exam date: {exam_date.date()} | Days left: {days_left}")

available_hours = st.slider(
    "How many hours can you study today?",
    min_value=1,
    max_value=8,
    value=2
)

recommendations = get_topic_recommendations(
    subject_id=subject_id,
    student_name=student_name,
    subjects=subjects,
    topics=topics,
    past_papers=past_papers,
    student_marks=student_marks
)

if recommendations.empty:
    st.warning("No topics found for this subject.")
    st.stop()

st.subheader("🎯 What should you study first?")

priority_filter = st.selectbox(
    "Filter by priority",
    ["All", "Study First", "Study Soon", "Revise Later"]
)

if priority_filter == "All":
    filtered_recommendations = recommendations
else:
    filtered_recommendations = recommendations[
        recommendations["priority"] == priority_filter
    ]

st.dataframe(
    filtered_recommendations[
        [
            "topic_name",
            "unit",
            "priority",
            "priority_score",
            "paper_count",
            "marks",
            "reason"
        ]
    ],
    use_container_width=True
)

st.subheader("📌 Important Notes")

selected_topic_name = st.selectbox(
    "Select a topic to revise",
    filtered_recommendations["topic_name"].tolist()
)

selected_topic = filtered_recommendations[
    filtered_recommendations["topic_name"] == selected_topic_name
].iloc[0]

st.success(f"Priority: {selected_topic['priority']}")

st.write("**Why this topic is important:**")
st.write(selected_topic["reason"])

st.write("**Quick revision notes:**")
st.write(selected_topic["important_notes"])

related_questions = past_papers[
    (past_papers["subject_id"] == subject_id)
    & (past_papers["topic_id"] == selected_topic["topic_id"])
]

if not related_questions.empty:
    st.write("**Past paper questions:**")

    for _, question in related_questions.iterrows():
        st.write(f"- {question['question_text']} ({question['year']}, {question['marks']} marks)")

else:
    st.write("No past-paper questions available for this topic.")

st.subheader("🗓️ Today's Study Plan")

study_plan = create_study_plan(
    recommendations=recommendations,
    available_hours=available_hours
)

if study_plan.empty:
    st.write("No study plan available.")
else:
    st.dataframe(study_plan, use_container_width=True)

st.subheader("📊 Your Revision Progress")

total_topics = len(recommendations)
weak_topics = len(
    recommendations[
        recommendations["priority"] == "Study First"
    ]
)

st.metric("Total Topics", total_topics)
st.metric("High-Priority Topics", weak_topics)
st.metric("Days Left", days_left)

st.success(
    "Start with the topic marked **Study First**. "
    "Do not try to revise every topic equally."
)