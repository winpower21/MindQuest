from celery import shared_task
from jinja2 import Template
from sqlalchemy import select
from .models import User, Subject, Chapter, Quiz, Question, Attempt, Response, db
from .mail import send_email
import csv
from flask import current_app
from datetime import datetime, timezone, timedelta
import requests


# Task 1 - User Triggered Async Job - Export as CSV
@shared_task(ignore_results=False, name="download_user_csv_report")
def generate_user_report(user_id):
    attempts = db.session.query(
        Subject.name.label('subject_name'),
        Chapter.name.label('chapter_name'),
        Quiz.id.label('quiz_id'),
        Quiz.name.label('quiz_name'),
        Quiz.total_marks,
        Attempt.attempt_number,
        Attempt.score,
        Attempt.submitted_at,
    ).join(Chapter, Chapter.subject_id == Subject.id)\
        .join(Quiz, Quiz.chapter_id == Chapter.id)\
        .join(Attempt, Attempt.quiz_id == Quiz.id)\
        .filter(Attempt.user_id == user_id)\
        .order_by(Attempt.submitted_at.desc())\
        .all()
    filename = f'user_report_{user_id}_{datetime.now()}.csv'
    with open(f'static/{filename}', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["Sr No.", "Subject Name", "Chapter Name", "Quiz Id", "Quiz Name",
                        "Total Marks", "User Score", "Attempt Number", "Submission Date"])
        sr_no = 0
        for attempt in attempts:
            writer.writerow([
                sr_no + 1,
                attempt.subject_name,
                attempt.chapter_name,
                attempt.quiz_id,
                attempt.quiz_name,
                attempt.total_marks,
                attempt.score,
                attempt.attempt_number,
                attempt.submitted_at.strftime('%d-%m-%Y - %H:%M:%S')
            ])
    return filename

@shared_task(ignore_results=False, name="download_user_attempt_csv_report")
def generate_user_attempt_report(subject_id, user_id, user_role):
    if user_role == "user":
        attempts = db.session.query(
            Attempt.attempt_number,
            Attempt.score,
            Attempt.submitted_at,
            Quiz.id.label('quiz_id'),
            Quiz.name.label('quiz_name'),
            Quiz.total_marks,
            Chapter.name.label('chapter_name'),
            Subject.name.label('subject_name'),
        ).join(Quiz, Attempt.quiz_id == Quiz.id) \
         .join(Chapter, Quiz.chapter_id == Chapter.id) \
         .join(Subject, Chapter.subject_id == Subject.id) \
         .filter(Attempt.user_id == user_id, Subject.id == subject_id) \
         .order_by(Attempt.submitted_at.desc()) \
         .all()
    
        filename = f'user_report_{user_id}_{datetime.now()}.csv'
        with open(f'static/{filename}', mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["Sr No.", "Subject Name", "Chapter Name", "Quiz Id", "Quiz Name",
                            "Total Marks", "User Score", "Attempt Number", "Submission Date"])
            sr_no = 0
            for attempt in attempts:
                writer.writerow([
                    sr_no + 1,
                    attempt.subject_name,
                    attempt.chapter_name,
                    attempt.quiz_id,
                    attempt.quiz_name,
                    attempt.total_marks,
                    attempt.score,
                    attempt.attempt_number,
                    attempt.submitted_at.strftime('%d-%m-%Y - %H:%M:%S')
                ])
        return filename
    elif user_role == "admin" :
        attempts = db.session.query(
        Attempt.id.label('attempt_id'),
        Attempt.attempt_number,
        Attempt.score,
        Attempt.submitted_at,
        User.id.label('user_id'),
        User.name.label('user_name'),
        Quiz.id.label('quiz_id'),
        Quiz.name.label('quiz_name'),
        Quiz.total_marks,
        Chapter.name.label('chapter_name'),
        Subject.name.label('subject_name'),
    ).join(User, Attempt.user_id == User.id) \
     .join(Quiz, Attempt.quiz_id == Quiz.id) \
     .join(Chapter, Quiz.chapter_id == Chapter.id) \
     .join(Subject, Chapter.subject_id == Subject.id) \
     .filter(Subject.id == subject_id) \
     .order_by(Attempt.submitted_at.desc()) \
     .all()
     
        filename_admin = f'subject_attempt_report_{subject_id}_{datetime.now()}.csv'
        with open(f'static/{filename_admin}', mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["Sr No.", "User ID","User Name" , "Subject Name", "Chapter Name", "Quiz Id", "Quiz Name",
                            "Total Marks", "User Score", "Attempt Number", "Submission Date"])
            sr_no = 0
            for attempt in attempts:
                writer.writerow([
                    sr_no + 1,
                    attempt.user_id,
                    attempt.user_name,
                    attempt.subject_name,
                    attempt.chapter_name,
                    attempt.quiz_id,
                    attempt.quiz_name,
                    attempt.total_marks,
                    attempt.score,
                    attempt.attempt_number,
                    attempt.submitted_at.strftime('%d-%m-%Y - %H:%M:%S')
                ])
        return filename_admin


# Task 2 - Scheduled Job - Monthly Activity Report
@shared_task(ignored_results=False, name="monthly_report")
def monthly_report():
    users = User.query.all()
    now = datetime.now(timezone.utc)
    start_of_month = now.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1)
    for user in users[1:]:
        user_data = {}
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_attempts = db.session.query(
            Subject.name.label("subject_name"),
            Chapter.name.label("chapter_name"),
            Quiz.name.label("quiz_name"),
            Quiz.total_marks.label("total_marks"),
            Attempt.attempt_number.label("attempt_number"),
            Attempt.score.label("score"),
            Attempt.submitted_at.label("submitted_at"))\
            .join(Quiz, Attempt.quiz_id == Quiz.id)\
            .join(Chapter, Quiz.chapter_id == Chapter.id)\
            .join(Subject, Chapter.subject_id == Subject.id)\
            .filter(Attempt.user_id == user.id, Attempt.submitted_at >= start_of_month, Attempt.submitted_at < end_of_month)\
            .order_by(Attempt.submitted_at.asc()).all()

        user_attempt_details = []
        for attempt in user_attempts:
            details = {}
            details["subjectName"] = attempt.subject_name
            details["chapterName"] = attempt.chapter_name
            details["quizName"] = attempt.quiz_name
            details["totalMarks"] = attempt.total_marks
            details["score"] = attempt.score
            details["attemptNumber"] = attempt.attempt_number
            details["submissionDate"] = attempt.submitted_at.strftime(
                '%d-%m-%Y - %H:%M:%S')
            user_attempt_details.append(details)
        attempted_quiz_ids = db.session.query(
            Attempt.quiz_id).filter_by(user_id=user.id).subquery()
        user_missed_quizzes = Quiz.query.filter(
            Quiz.deadline >= start_of_month,
            Quiz.deadline < end_of_month,
            ~Quiz.id.in_(select(attempted_quiz_ids.c.quiz_id))
        ).all()
        user_missed_quiz_details = []
        for missed_quiz in user_missed_quizzes:
            details = {}
            details["quizName"] = missed_quiz.name
            details["startDate"] = missed_quiz.start_date.strftime('%d-%m-%Y')
            details["deadline"] = missed_quiz.deadline.strftime('%d-%m-%Y')
            user_missed_quiz_details.append(details)
        user_data['user_attempt_details'] = user_attempt_details
        user_data['user_missed_quiz_details'] = user_missed_quiz_details
        mail_template = """
        <h3>Dear {{ user_data.name }}, </h3>
        <p>Please find your monthly report below.</p>
        <p>Visit the MindQuest app at http://127.0.0.1:5173 for more details.</p>
        <h4>Your quiz scores: </h4>
        {% if user_data.user_attempt_details|length > 0 %}
        <table>
            <tr>
                <th>Subject Name</th>
                <th>Chapter Name</th>
                <th>Quiz Name</th>
                <th>Total Marks</th>
                <th>Your Score</th>
                <th>Attempt Number</th>
                <th>Submission Date</th>
            </tr>
            {% for attempt in user_data.user_attempt_details %}
            <tr>
                <td>{{ attempt.subjectName }}</td>
                <td>{{ attempt.chapterName }}</td>
                <td>{{ attempt.quizName }}</td>
                <td>{{ attempt.totalMarks }}</td>
                <td>{{ attempt.score }}</td>
                <td>{{ attempt.attemptNumber }}</td>
                <td>{{ attempt.submissionDate }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>You have not attempted any quizzes this month !!</p>
        {% endif %}
        <h4>Your missed quizzes: </h4>
        {% if user_data.user_missed_quiz_details|length > 0 %}
        <table>
            <tr>
                <th>Quiz Name</th>
                <th>Quiz Start Date</th>
                <th>Quiz Deadline</th>
            </tr>
            {% for missed_quiz in user_data.user_missed_quiz_details %}
            <tr>
                <td>{{ missed_quiz.quizName }}</td>
                <td>{{ missed_quiz.startDate }}</td>
                <td>{{ atmissed_quiztempt.deadline }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>You have not missed any quizzes this month !!</p>
        {% endif %}
        """

        message = Template(mail_template).render(user_data=user_data)
        send_email(
            user.email, subject="Monthly Performance Report - MindQuest", message=message)
    return "Monthly reports sent"


# Task 3 -  Daily reminders - The application should send daily reminders to users on g-chat using Google Chat Webhooks or SMS or mail
@shared_task(ignore_results=False, name="generate_msg")
def generate_msg(chapterName, quizName):
    text = f"Hi, new quiz has been added under {chapterName}:{quizName}. Please check the app at http://127.0.0.1:5173 to view more details."
    response = requests.post(
        "https://chat.googleapis.com/v1/spaces/AAQAN_E2GeM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Tdm6WauWeZtY1MQEwbMP-GelgXnROQqn96LlO5KrCUE", json={"text": text})
    print(response.status_code)
    return "Message sent"
