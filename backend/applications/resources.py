from flask_restful import Api, Resource, fields, marshal_with, abort, marshal
from flask import request
from sqlalchemy.sql import func
from .models import Subject, Chapter, Quiz, Question, User, Attempt, Response, Role, db
from flask_security.decorators import roles_required, roles_accepted
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime, date, timedelta, timezone
from .extensions import whooshee
from celery.result import AsyncResult
from .tasks import generate_msg

api = Api(prefix="/api")

# ====================================================================================================================
# --- Define field structures ---
label_value_fields = {
    'label': fields.String,
    'value': fields.Float
}

date_value_fields = {
    'date': fields.String,
    'users': fields.Integer
}

hour_count_fields = {
    'hour': fields.Integer,
    'count': fields.Integer
}

date_count_fields = {
    'date': fields.String,
    'count': fields.Integer
}

totals_fields = {
    'users': fields.Integer,
    'quizzes': fields.Integer,
    'attempts': fields.Integer
}

admin_stats_fields = {
    'avg_score_per_quiz': fields.List(fields.Nested(label_value_fields)),
    'top_users': fields.List(fields.Nested(label_value_fields)),
    'low_performing_quizzes': fields.List(fields.Nested(label_value_fields)),
    'subject_performance': fields.List(fields.Nested(label_value_fields)),
    'daily_active': fields.List(fields.Nested(date_value_fields)),
    'most_active_users': fields.List(fields.Nested(label_value_fields)),
    'attempt_heatmap': fields.List(fields.Nested(hour_count_fields)),
    'most_attempted_quizzes': fields.List(fields.Nested(label_value_fields)),
    'avg_attempts_per_quiz': fields.List(fields.Nested(label_value_fields)),
    'completion_rate': fields.List(fields.Nested(label_value_fields)),
    'totals': fields.Nested(totals_fields),
    'user_growth': fields.List(fields.Nested(date_count_fields))
}

# ====================================================================================================================


class RawJsonField(fields.Raw):
    def format(self, value):
        return value


attempt_output_fields = {
    "subject_name": fields.String,
    "subject_id": fields.Integer,
    "subject_image_url": fields.String,
    "chapter_name": fields.String,
    "chapter_id": fields.Integer,
    "quiz_name": fields.String,
    "quiz_id": fields.Integer,
    "total_marks": fields.Integer,
    "attempt_no": fields.Integer,
    "attempt_id": fields.Integer,
    "score": fields.Float,
    "submitted_at": fields.DateTime(dt_format='iso8601'),
    "user_name": fields.String,
    "user_id": fields.Integer,
    "avatar_seed": fields.String,
    "avatar_style": fields.String
}

responses_fields = {
    "id": fields.Integer,
    "question_id": fields.Integer,
    "attempt_id": fields.Integer,
    "answer": RawJsonField(),
    "isCorrect": fields.Boolean
}

attempts_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "quiz_id": fields.Integer,
    "attempt_number": fields.Integer,
    "responses": fields.List(fields.Nested(responses_fields)),
    "score": fields.Integer,
    "submitted_at": fields.DateTime(dt_format='iso8601')
}

role_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String
}

user_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "avatar_seed": fields.String,
    "avatar_style": fields.String,
    "active": fields.Boolean,
    "roles": fields.List(fields.Nested(role_fields)),
    "email": fields.String,
    "attempts": fields.List(fields.Nested(attempts_fields))
}

question_view_fields = {
    "id": fields.Integer,
    "question_no": fields.Integer,
    "question_statement": fields.String,
    "ans_type": fields.String,
    "options": fields.List(fields.String),
    "correct_options": fields.List(fields.String),
    "correct_min": fields.Float,
    "correct_max": fields.Float,
    "marks": fields.Integer,
    "question_no": fields.Integer,
    "attempts": fields.List(fields.Nested(attempts_fields))
}

quiz_view_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "time_limit": fields.Integer,
    "start_date": fields.DateTime(dt_format='iso8601'),
    "deadline": fields.DateTime(dt_format='iso8601'),
    "questions": fields.List(fields.Nested(question_view_fields)),
    "attempts": fields.List(fields.Nested(attempts_fields)),
    "total_marks": fields.Integer
}


question_attempt_fields = {
    "id": fields.Integer,
    "question_statement": fields.String,
    "ans_type": fields.String,
    "options": fields.List(fields.String),
    "marks": fields.Integer,
    "question_no": fields.Integer
}

quiz_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "chapter_id": fields.Integer,
    "subject_id": fields.Integer,
    "time_limit": fields.Integer,
    "start_date": fields.DateTime(dt_format='iso8601'),
    "deadline": fields.DateTime(dt_format='iso8601'),
    "questions": fields.List(fields.Nested(question_attempt_fields)),
    "total_marks": fields.Integer
}

chapter_fields = {
    "id": fields.Integer,
    "subject_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "quizzes": fields.List(fields.Nested(quiz_fields))
}

subject_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "image_url": fields.String,
    "chapters": fields.List(fields.Nested(chapter_fields))
}


class SubjectAPI(Resource):
    # Get all subjects
    @marshal_with(subject_fields)
    @jwt_required()
    @roles_accepted('user', 'admin')
    def get(self):
        subjects = Subject.query.all()
        if not subjects:
            abort(404, message="No subjects found")
        return subjects

    # Create new subject
    @jwt_required()
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        try:
            name = data["name"]
            description = data["description"]
        except KeyError as e:
            abort(400, message=f"Missing required field: {str(e)}")
        image_url = data.get("image_url")
        existing_subject = Subject.query.filter_by(name=name).first()
        if existing_subject:
            abort(
                409, message=f"Subject with name: {existing_subject.name}, already exists.")
        try:
            if image_url:
                subject = Subject(
                    name=name, description=description, image_url=image_url)
            else:
                subject = Subject(name=name, description=description)
            db.session.add(subject)
            db.session.commit()
            return {"message": "Subject added successfully"}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error creating subject: {e}")


class SubjectIdAPI(Resource):
    # Get subject by subject id.
    @marshal_with(subject_fields)
    @jwt_required()
    @roles_accepted('user', 'admin')
    def get(self, id):
        subject = Subject.query.get(id)
        if not subject:
            abort(404, message="Subject not found")
        return subject

    # Modify specific subject
    @jwt_required()
    @roles_required('admin')
    def put(self, id):
        data = request.get_json()
        id = id
        name = data.get("name")
        description = data.get("description")
        image_url = data.get("image_url")
        if not name and not description and not image_url:
            abort(400, message="Provide data to update")
        subject = Subject.query.get(id)
        if not subject:
            abort(409, message="This subject does not exist.")
        try:
            if name:
                subject.name = name
            if description:
                subject.description = description
            if image_url:
                subject.image_url = image_url

            db.session.commit()
            return {"message": "Subject modified successfully"}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error modifying subject: {e}")

    # Delete a subject.
    @jwt_required()
    @roles_required('admin')
    def delete(self, id):
        subject = Subject.query.get(id)
        if not subject:
            abort(409, message="This subject does not exist.")
        try:
            db.session.delete(subject)
            db.session.commit()
            return {"message": "Subject deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error deleting subject: {e}")


class ChapterAPI(Resource):
    # Get all chapters for a subject
    @marshal_with(chapter_fields)
    @jwt_required()
    @roles_accepted('admin', 'user')
    def get(self, subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            abort(404, message="Subject does not exist")
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        if not chapters:
            abort(404, message="No chapters for this subject.")
        return chapters

    # Create new chapter
    @jwt_required()
    @roles_required('admin')
    def post(self, subject_id):
        data = request.get_json()
        try:
            name = data["name"]
            description = data["description"]
        except KeyError as e:
            abort(400, message=f"Missing required field: {str(e)}")
        subject = Subject.query.get(subject_id)
        if not subject:
            abort(400, message="Subject does not exist")
        chapter = Chapter.query.filter_by(
            name=name, subject_id=subject_id).first()
        if chapter:
            abort(
                409, message=f"Chapter with name: {chapter.name}, already exists in this subject.")
        try:
            chapter = Chapter(
                name=name, description=description, subject_id=subject_id)
            db.session.add(chapter)
            db.session.commit()
            return {"message": f"Subject {name} created successfully."}
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Could not add subject: {e}")


class ChpaterIdAPI(Resource):
    # Get a chapter by chapter id
    @jwt_required()
    @roles_accepted('admin', 'user')
    @marshal_with(chapter_fields)
    def get(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            abort(404, message="Chapter does not exist")
        return chapter

    # Modify a chapter
    @jwt_required()
    @roles_required('admin')
    def put(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            abort(404, message="This chapter does not exist.")
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        if not name and not description:
            abort(400, message="Provide data to modify")
        try:
            if name:
                chapter.name = name
            if description:
                chapter.description = description
            db.session.commit()
            return {"message": "Chapter successfully modified"}
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error modifiying chapter: {e}")

    # Delete a chapter
    @jwt_required()
    @roles_required('admin')
    def delete(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            abort(404, message="Chapter does not exist")
        try:
            db.session.delete(chapter)
            db.session.commit()
            return {"message": "Chapter deleted successfully."}
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error deleting chapter: {e}")


class QuizAPI(Resource):

    @marshal_with(quiz_fields)
    @jwt_required()
    @roles_accepted('admin', 'user')
    def get(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            abort(404, message="Chapter does not exist")
        quizzes = chapter.quizzes
        return quizzes

    @jwt_required()
    @roles_required('admin')
    def post(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            abort(404, message="Chapter does not exist")
        data = request.get_json()
        try:
            name = data["name"]
            description = data["description"]
            time_limit = data["time_limit"]
            questions = data["questions"]
            total_marks = data["total_marks"]
            start_date = datetime.fromisoformat(
                data["start_date"]) if data["start_date"] else None
            deadline = datetime.fromisoformat(
                data["deadline"]) if data["deadline"] else None
            if Quiz.query.filter_by(name=name).first():
                abort(500, message=f"Quiz with name: {name} already exists. Use a different name.")
        except KeyError as e:
            abort(400, message=f"Missing required field: {str(e)}")
        try:
            with db.session.begin_nested():
                if start_date:
                    quiz = Quiz(name=name, description=description, time_limit=time_limit,
                                chapter_id=chapter_id, total_marks=total_marks, start_date=start_date, deadline=deadline)
                else:
                    quiz = Quiz(name=name, description=description, time_limit=time_limit,
                                chapter_id=chapter_id, total_marks=total_marks, deadline=deadline)
                db.session.add(quiz)
                db.session.flush()  # Ensure quiz.id is available for questions
                for question in questions:
                    new_question = Question(
                        question_statement=question["question_statement"],
                        ans_type=question["ans_type"],
                        options=question.get("options", []),
                        correct_options=question.get("correct_options", []),
                        correct_min=question.get("correct_min"),
                        correct_max=question.get("correct_max"),
                        marks=question.get("marks", 0),
                        quiz_id=quiz.id,
                        question_no=questions.index(question)+1
                    )
                    db.session.add(new_question)
                db.session.commit()
            generate_msg.delay(chapter.name, name)
            return {"message": "Quiz created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error creating quiz: {e}")


class QuizIdViewAPI(Resource):
    @marshal_with(quiz_view_fields)
    @jwt_required()
    @roles_accepted('admin', 'user')
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            abort(404, message="Quiz does not exist")
        return quiz


class QuizIdAPI(Resource):
    @marshal_with(quiz_fields)
    @jwt_required()
    @roles_accepted('admin', 'user')
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            abort(404, message="Quiz does not exist")
        return quiz

    @jwt_required()
    @roles_required('admin')
    def put(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)

        # if quiz.start_date < today < quiz.deadline:
        if not quiz:
            abort(404, message="Quiz does not exist")

        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        time_limit = data.get("time_limit")
        total_marks = data.get("total_marks")
        questions = data.get("questions", [])
        start_date = datetime.fromisoformat(data["start_date"])
        deadline = datetime.fromisoformat(data["deadline"])

        if not any([name, description, time_limit, questions]):
            abort(400, message="Provide data to modify")
        response = db.session.query(Response).join(
            Attempt, Attempt.quiz_id == quiz_id).distinct().all()
        # Response.query.filter_by(quiz_id=quiz_id).first()
        if response:
            abort(400, message="This quiz already has responses. Cannot be modified.")
        try:
            # Update metadata
            if name:
                quiz.name = name
            if description:
                quiz.description = description
            if time_limit is not None:
                quiz.time_limit = time_limit
            if total_marks is not None:
                quiz.total_marks = total_marks
            if start_date is not None:
                quiz.start_date = start_date
            if deadline is not None:
                quiz.deadline = deadline

            # Remove existing questions
            Question.query.filter_by(quiz_id=quiz.id).delete()

            # Add new questions
            for q in questions:
                new_q = Question(
                    quiz_id=quiz.id,
                    question_statement=q["question_statement"],
                    ans_type=q["ans_type"],
                    options=q.get("options", []),
                    correct_options=q.get("correct_options", []),
                    correct_min=q.get("correct_min"),
                    correct_max=q.get("correct_max"),
                    marks=q.get("marks",0),
                    question_no=questions.index(q)+1
                )
                db.session.add(new_q)

            db.session.commit()
            return {"message": "Quiz and questions successfully modified"}

        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error modifying quiz: {e}")
        # else:
            # if today > quiz.deadline:
            # abort(400, message="Deadline for this quiz has passed.")
            # elif today < quiz.start_date:
            # abort(400, message="Quiz not open for submissions.")

    @jwt_required()
    @roles_required('admin')
    def delete(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            abort(404, message="Quiz does not exist")
        try:
            db.session.delete(quiz)
            db.session.commit()
            return {"message": "Quiz deleted successfully."}
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error deleting quiz: {e}")


class QuestionAPI(Resource):
    @marshal_with(question_attempt_fields)
    @jwt_required()
    @roles_accepted('admin', 'user')
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            abort(404, message="Quiz does not exist")
        questions = quiz.questions
        return questions

    @jwt_required()
    @roles_required('admin')
    def post(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            abort(404, message="Quiz does not exist")
        data = request.get_json()
        try:
            question_statement = data["question_statement"]
            ans_type = data["ans_type"]
            options = data.get("options", [])
            correct_options = data.get("correct_options", [])
            correct_min = data.get("correct_min")
            correct_max = data.get("correct_max")
            marks = data.get("marks", 0)
        except KeyError as e:
            abort(400, message=f"Missing required field: {str(e)}")
        try:
            question = Question(
                question_statement=question_statement,
                ans_type=ans_type,
                options=options,
                correct_options=correct_options,
                correct_min=correct_min,
                correct_max=correct_max,
                marks=marks,
                quiz_id=quiz_id
            )
            db.session.add(question)
            db.session.commit()
            return {"message": "Question added successfully"}, 201
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error adding question: {e}")


class QuestionIdAPI(Resource):
    @jwt_required()
    @roles_accepted('admin')
    def put(self, question_id):
        question = Question.query.get(question_id)
        if not question:
            abort(404, message="Question does not exist")
        data = request.get_json()
        question_statement = data.get("question_statement")
        ans_type = data.get("ans_type")
        options = data.get("options", [])
        correct_options = data.get("correct_options", [])
        correct_min = data.get("correct_min")
        correct_max = data.get("correct_max")
        marks = data.get("marks", 0)
        if not question_statement and not ans_type and not options and not correct_options and not correct_min and not correct_max and not marks:
            abort(400, message="Provide data to modify")
        try:
            if question_statement:
                question.question_statement = question_statement
            if ans_type:
                question.ans_type = ans_type
            if options:
                question.options = options
            if correct_options:
                question.correct_options = correct_options
            if correct_min:
                question.correct_min = correct_min
            if correct_max:
                question.correct_max = correct_max
            if marks:
                question.marks = marks
            db.session.commit()
            return {"message": "Question successfully modified"}
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error modifying question: {e}")

    @jwt_required()
    @roles_required('admin')
    def delete(self, question_id):
        question = Question.query.get(question_id)
        if not question:
            abort(404, message="Question does not exist")
        try:
            db.session.delete(question)
            db.session.commit()
            return {"message": "Question deleted successfully."}
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error deleting question: {e}")


class ResponseViewAPI(Resource):
    @jwt_required()
    @roles_accepted('admin', 'user')
    def get(self, attempt_id):
        attempt = Attempt.query.get(attempt_id)
        if attempt:
            quiz = Quiz.query.get(attempt.quiz_id)
            return {
                "attempt": marshal(attempt, attempts_fields),
                "quiz": marshal(quiz, quiz_view_fields)
            }
        else:
            abort(404, "Unknown resourse")


class ResponseCreateAPI(Resource):
    @jwt_required()
    @roles_accepted('admin', 'user')
    def post(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        today = datetime.now()
        if today > quiz.deadline:
            abort(400, message="Deadline for this quiz has passed.")
        elif today < quiz.start_date:
            abort(400, message="Quiz not open for submissions.")
        user = get_jwt_identity()
        userObj = User.query.filter_by(email=user).first()
        if not quiz:
            abort(404, message="Quiz does not exist")
        data = request.get_json()
        user_id = userObj.id if userObj else None
        answers = data.get("answers", {})

        if not user_id or not answers:
            abort(400, message="User ID and answers are required")

        score = 0
        answer_key = {}
        for question in quiz.questions:
            qid = question.id
            user_answer = answers.get(str(qid))
            if question.ans_type == "mcq":
                answer = [user_answer]
                if answer == question.correct_options:
                    score += question.marks
                    answer_key[qid] = [True, answer]
                else:
                    answer_key[qid] = [False, answer]
            elif question.ans_type == "num":
                if question.correct_min <= user_answer <= question.correct_max:
                    score += question.marks
                    answer_key[qid] = [True, user_answer]
                else:
                    answer_key[qid] = [False, user_answer]
            elif question.ans_type == "msq":
                if set(user_answer) == set(question.correct_options):
                    score += question.marks
                    answer_key[qid] = [True, user_answer]
                else:
                    answer_key[qid] = [False, user_answer]
            else:
                answer_key[qid] = []

        latest_attempt = Attempt.query.filter_by(
            user_id=user_id, quiz_id=quiz_id).order_by(Attempt.id.desc()).first()
        try:
            with db.session.begin_nested():
                if not latest_attempt:
                    attempt = Attempt(
                        user_id=user_id, quiz_id=quiz_id, score=score)
                else:
                    attempt = Attempt(user_id=user_id, quiz_id=quiz_id, score=score,
                                      attempt_number=latest_attempt.attempt_number + 1)
                db.session.add(attempt)
                db.session.flush()
                attempt_id = attempt.id
                for key, value in answer_key.items():
                    response = Response(
                        question_id=key, attempt_id=attempt_id, answer=value[-1], isCorrect=value[0])
                    db.session.add(response)
                db.session.commit()
            return {"message": "Responses submitted successfully"}, 201
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error submitting responses: {e}")


class MySubjects(Resource):
    @marshal_with(subject_fields)
    @jwt_required()
    @roles_accepted('user')
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(email=user_id).first()
        id = user.id if user else None
        mySubjects = db.session.query(Subject)\
            .join(Chapter, Chapter.subject_id == Subject.id)\
            .join(Quiz, Quiz.chapter_id == Chapter.id)\
            .join(Attempt, Attempt.user_id == id).distinct().all()
        if not mySubjects:
            abort(404, message="You have not attempted quizzes for any subjects.")
        return mySubjects


class AttemptsAPI(Resource):
    @jwt_required()
    @roles_accepted('user', 'admin')
    def get(self):
        user_identity = get_jwt_identity()
        user = User.query.filter_by(email=user_identity).first()
        user_id = user.id
        user_role = user.roles[0].name
        if user_role == "user":
            my_attempts = db.session.query(Attempt).filter_by(
                user_id=user_id).order_by(Attempt.submitted_at.desc()).all()
            if my_attempts:
                return {"myAttempts": marshal(my_attempts, attempts_fields)}
            else:
                abort(404, message='You have not attempted this quiz.')
        elif user_role == "admin":
            all_attempts = all_attempts = db.session.query(
                Subject.name.label('subject_name'),
                Subject.id.label('subject_id'),
                Subject.image_url.label('subject_image_url'),
                Chapter.name.label('chapter_name'),
                Chapter.id.label('chapter_id'),
                Quiz.name.label('quiz_name'),
                Quiz.id.label('quiz_id'),
                Quiz.total_marks,
                Attempt.attempt_number,
                Attempt.score,
                Attempt.id.label('attempt_id'),
                Attempt.submitted_at,
                User.id.label('user_id'),
                User.name.label('user_name'),
                User.avatar_seed,
                User.avatar_style
            ).join(Chapter, Chapter.subject_id == Subject.id)\
                .join(Quiz, Quiz.chapter_id == Chapter.id)\
                .join(Attempt, Attempt.quiz_id == Quiz.id)\
                .join(User, Attempt.user_id == User.id)\
                .order_by(Attempt.submitted_at.desc())\
                .all()
            today = date.today()
            attempts_today = Attempt.query.filter(db.func.date(
                Attempt.submitted_at) == today).order_by(Attempt.submitted_at.desc()).all()
            if all_attempts:
                results = [marshal(row._asdict(), attempt_output_fields)
                           for row in all_attempts]
                return {
                    "all_attempts": results,
                    "attempts_today": marshal(attempts_today, attempts_fields)
                }
            else:
                abort(404, message='No user activity.')


class AttemptsIdAPI(Resource):

    @jwt_required()
    @roles_accepted('admin', 'user')
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        user_identity = get_jwt_identity()
        user = User.query.filter_by(email=user_identity).first()
        user_id = user.id
        user_role = user.roles[0].name
        if quiz:
            if user_role == "user":
                all_attempts = db.session.query(Attempt).filter_by(
                    user_id=user_id, quiz_id=quiz_id).order_by(Attempt.submitted_at.desc()).all()
                all_attempts = all_attempts = db.session.query(
                    Subject.name.label('subject_name'),
                    Subject.id.label('subject_id'),
                    Subject.image_url.label('subject_image_url'),
                    Chapter.name.label('chapter_name'),
                    Chapter.id.label('chapter_id'),
                    Quiz.name.label('quiz_name'),
                    Quiz.id.label('quiz_id'),
                    Quiz.total_marks,
                    Attempt.attempt_number,
                    Attempt.score,
                    Attempt.id.label('attempt_id'),
                    Attempt.submitted_at,
                    User.id.label('user_id'),
                    User.name.label('user_name'),
                    User.avatar_seed,
                    User.avatar_style
                ).join(Chapter, Chapter.subject_id == Subject.id)\
                    .join(Quiz, Quiz.chapter_id == Chapter.id)\
                    .join(Attempt, Attempt.quiz_id == Quiz.id)\
                    .join(User, Attempt.user_id == User.id)\
                    .filter(Attempt.quiz_id == quiz_id, Attempt.user_id == user_id)\
                    .order_by(Attempt.submitted_at.desc())\
                    .all()
                if all_attempts:
                    results = [marshal(row._asdict(), attempt_output_fields)
                               for row in all_attempts]
                    return {"all_attempts": results}
                else:
                    abort(404, message='You have not attempted this quiz.')
            if user_role == "admin":
                all_attempts = all_attempts = db.session.query(
                    Subject.name.label('subject_name'),
                    Subject.id.label('subject_id'),
                    Subject.image_url.label('subject_image_url'),
                    Chapter.name.label('chapter_name'),
                    Chapter.id.label('chapter_id'),
                    Quiz.name.label('quiz_name'),
                    Quiz.id.label('quiz_id'),
                    Quiz.total_marks,
                    Attempt.attempt_number,
                    Attempt.score,
                    Attempt.id.label('attempt_id'),
                    Attempt.submitted_at,
                    User.id.label('user_id'),
                    User.name.label('user_name'),
                    User.avatar_seed,
                    User.avatar_style
                ).join(Chapter, Chapter.subject_id == Subject.id)\
                    .join(Quiz, Quiz.chapter_id == Chapter.id)\
                    .join(Attempt, Attempt.quiz_id == Quiz.id)\
                    .join(User, Attempt.user_id == User.id)\
                    .filter(Attempt.quiz_id == quiz_id)\
                    .order_by(Attempt.submitted_at.desc())\
                    .all()
            if all_attempts:
                results = [marshal(row._asdict(), attempt_output_fields)
                           for row in all_attempts]
                return {
                    "all_attempts": results,
                }
            else:
                abort(404, message='No attempts.')
        return quiz


class UsersAPI(Resource):

    @marshal_with(user_fields)
    @jwt_required()
    @roles_required('admin')
    def get(self):
        users = User.query.all()
        if users:
            return users
        else:
            abort(404, message="No registered users")


class UserSearchAPI(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    @roles_required('admin')
    def get(self):
        query = request.args.get('query')
        try:
            users = User.query.whooshee_search(query).all()
            if users:
                return users
            else:
                abort(404, message="No Search Results")
        except ValueError:
            abort(500, message="Search query must contain atleast 3 characters")


class SearchAPI(Resource):
    @jwt_required()
    @roles_accepted('user', 'admin')
    def get(self):
        query = request.args.get('query')

        try:
            subjects = Subject.query.whooshee_search(query).all()
            chapters = Chapter.query.whooshee_search(query).all()
            quizzes = Quiz.query.whooshee_search(query).all()
            response = {}
            response["subjects"] = marshal(
                subjects, subject_fields) if subjects else None
            response["chapters"] = marshal(
                chapters, chapter_fields) if chapters else None
            response["quizzes"] = marshal(
                quizzes, quiz_fields) if quizzes else None

            return response
        except ValueError:
            abort(500, message="Search query must contain atleast 3 characters")


# ==================================================================================================================

class AdminStatsResource(Resource):
    @marshal_with(admin_stats_fields)
    @jwt_required()
    @roles_required('admin')
    def get(self):
        data = {}

        # --- USER PERFORMANCE ---
        data['avg_score_per_quiz'] = db.session.query(
            Quiz.name, func.avg(Attempt.score)
        ).join(Attempt).group_by(Quiz.id).all()

        data['top_users'] = db.session.query(
            User.name, func.avg(Attempt.score)
        ).join(Attempt).group_by(User.id).order_by(func.avg(Attempt.score).desc()).limit(5).all()

        data['low_performing_quizzes'] = db.session.query(
            Quiz.name, func.avg(Attempt.score)
        ).join(Attempt).group_by(Quiz.id).order_by(func.avg(Attempt.score)).limit(5).all()

        data['subject_performance'] = db.session.query(
            Subject.name, func.avg(Attempt.score)
        ).join(Quiz, Quiz.subject_id == Subject.id
               ).join(Attempt, Attempt.quiz_id == Quiz.id
                      ).group_by(Subject.id).all()

        # --- USER ACTIVITY ---
        data['daily_active'] = db.session.query(
            func.date(Attempt.submitted_at), func.count(
                func.distinct(Attempt.user_id))
        ).group_by(func.date(Attempt.submitted_at)).all()

        data['most_active_users'] = db.session.query(
            User.name, func.count(Attempt.id)
        ).join(Attempt).group_by(User.id).order_by(func.count(Attempt.id).desc()).limit(5).all()

        data['attempt_heatmap'] = db.session.query(
            func.extract('hour', Attempt.submitted_at), func.count(Attempt.id)
        ).group_by(func.extract('hour', Attempt.submitted_at)).all()

        # --- QUIZ ENGAGEMENT ---
        data['most_attempted_quizzes'] = db.session.query(
            Quiz.name, func.count(Attempt.id)
        ).join(Attempt).group_by(Quiz.id).order_by(func.count(Attempt.id).desc()).limit(5).all()

        data['avg_attempts_per_quiz'] = db.session.query(
            Quiz.name, func.count(Attempt.id)
        ).join(Attempt).group_by(Quiz.id).all()

        total_users = db.session.query(User.id).count()
        data['completion_rate'] = db.session.query(
            Quiz.name, (func.count(Attempt.id) / total_users)
        ).join(Attempt).group_by(Quiz.id).all()

        # --- OTHER INSIGHTS ---
        data['totals'] = {
            "users": db.session.query(User.id).count(),
            "quizzes": db.session.query(Quiz.id).count(),
            "attempts": db.session.query(Attempt.id).count(),
        }

        data['user_growth'] = db.session.query(
            func.date(User.created_at), func.count(User.id)
        ).group_by(func.date(User.created_at)).all()

        # Format all result sets
        def serialize(rows):
            return [{"label": r[0], "value": float(r[1])} for r in rows]

        return {
            "avg_score_per_quiz": serialize(data['avg_score_per_quiz']),
            "top_users": serialize(data['top_users']),
            "low_performing_quizzes": serialize(data['low_performing_quizzes']),
            "subject_performance": serialize(data['subject_performance']),
            "daily_active": [{"date": str(r[0]), "users": r[1]} for r in data['daily_active']],
            "most_active_users": serialize(data['most_active_users']),
            "attempt_heatmap": [{"hour": int(r[0]), "count": r[1]} for r in data['attempt_heatmap']],
            "most_attempted_quizzes": serialize(data['most_attempted_quizzes']),
            "avg_attempts_per_quiz": serialize(data['avg_attempts_per_quiz']),
            "completion_rate": serialize(data['completion_rate']),
            "totals": data['totals'],
            "user_growth": [{"date": str(r[0]), "count": r[1]} for r in data['user_growth']]
        }


# ==================================================================================================================


api.add_resource(SubjectAPI, "/subject")
api.add_resource(SubjectIdAPI, "/subject/<int:id>")
api.add_resource(ChapterAPI, "/subject/<int:subject_id>/chapters")
api.add_resource(ChpaterIdAPI, "/chapter/<int:chapter_id>")
api.add_resource(QuizAPI, "/chapter/<int:chapter_id>/quiz")
api.add_resource(QuizIdAPI, "/quiz/<int:quiz_id>")
api.add_resource(QuizIdViewAPI, "/quiz/<int:quiz_id>/view")
api.add_resource(QuestionAPI, "/quiz/<int:quiz_id>/questions")
api.add_resource(QuestionIdAPI, "/question/<int:question_id>")
api.add_resource(ResponseCreateAPI, "/quiz/<int:quiz_id>/response")
api.add_resource(ResponseViewAPI, "/response/<int:attempt_id>")
api.add_resource(MySubjects, "/my-subjects")
api.add_resource(AttemptsAPI, "/attempts")
api.add_resource(AttemptsIdAPI, "/attempts/<int:quiz_id>")
api.add_resource(UsersAPI, "/users")
api.add_resource(UserSearchAPI, "/users/search")
api.add_resource(SearchAPI, "/search")
api.add_resource(AdminStatsResource, "/admin/stats")
