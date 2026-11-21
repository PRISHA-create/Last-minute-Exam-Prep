# Last-Minute Exam Revision Assistant

A Python and Streamlit web application that helps college students identify
the most important topics to revise before exams.

## Features

- Subject and topic management using CSV data
- Exam countdown
- Topic priority recommendation
- Past-paper frequency analysis
- Marks-based weakness detection
- Personalized study plan
- Quick revision notes
- Past-paper question display

## How to Run

1. Install Python 3.10 or above.
2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate it:

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

4. Install packages:

```bash
pip install -r requirements.txt
```

5. Run the app:

```bash
streamlit run app.py
```

## Deployment

This app can be deployed using Streamlit Community Cloud by pushing the
project to GitHub and selecting `app.py` as the entrypoint.