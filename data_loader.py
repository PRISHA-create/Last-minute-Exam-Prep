from pathlib import Path

import pandas as pd


DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"


def load_csv(file_name):
    file_path = DATA_FOLDER / file_name
    return pd.read_csv(file_path)


def load_all_data():
    subjects = load_csv("subjects.csv")
    topics = load_csv("topics.csv")
    past_papers = load_csv("past_papers.csv")
    student_marks = load_csv("student_marks.csv")

    return subjects, topics, past_papers, student_marks