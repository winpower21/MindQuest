from datetime import datetime, timezone, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_security.core import UserMixin, RoleMixin
from .extensions import whooshee

db = SQLAlchemy()

@whooshee.register_model('name','email')
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    avatar_seed = db.Column(db.String(), nullable=False)
    avatar_style = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    fs_uniquifier = db.Column(db.String(), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship("Role", backref="bearers", secondary="user_roles") # type: ignore
    attempts = db.relationship("Attempt", backref="user", cascade="all, delete-orphan")
    
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id", ondelete='CASCADE'))

@whooshee.register_model('name', 'description')
class Subject(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.Text())
    image_url = db.Column(db.String(), default="https://images.unsplash.com/photo-1513185041617-8ab03f83d6c5?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete-orphan")
    

@whooshee.register_model('name', 'description')    
class Chapter(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    subject_id = db.Column(db.Integer(), db.ForeignKey('subject.id', ondelete="CASCADE"))
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text())
    quizzes = db.relationship("Quiz", backref="chapter", cascade = "all, delete-orphan")
    __table_args__ = (
        db.UniqueConstraint('name','subject_id', name="unique_chapter_per_subject"),
    )

@whooshee.register_model('name', 'description')    
class Quiz(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    chapter_id = db.Column(db.Integer(), db.ForeignKey('chapter.id', ondelete="CASCADE"))
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), default=datetime.now)
    total_marks = db.Column(db.Integer(), nullable=False)
    time_limit = db.Column(db.Integer(), nullable=False)
    start_date = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.combine(
            datetime.now(timezone.utc).date(),
            datetime.min.time(),
            tzinfo=timezone.utc
        )
    )
    deadline = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.combine(
            (datetime.now(timezone.utc) + timedelta(days=8)).date(),
            datetime.min.time(),
            tzinfo=timezone.utc
        )
    )
    questions = db.relationship("Question", backref="quiz", cascade = "all, delete-orphan")
    attempts = db.relationship("Attempt", backref="quiz", cascade = "all, delete-orphan")
    # Add subject_id directly for easier access
    subject_id = db.Column(db.Integer())

    @db.validates('chapter_id')
    def update_subject_id(self, key, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        self.subject_id = chapter.subject_id if chapter else None
        return chapter_id

@whooshee.register_model('question_statement')
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_no = db.Column(db.Integer, nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'))
    question_statement = db.Column(db.Text, nullable=False)
    ans_type = db.Column(db.String, nullable=False)  # 'MCQ', 'MSQ', 'NUM'
    options = db.Column(db.JSON, nullable=True)  # Only for single/multiple-choice questions
    correct_options = db.Column(db.JSON, nullable=True)  # Only for single/multiple-choice questions
    correct_min = db.Column(db.Float, nullable=True)  # Only for numerical answers
    correct_max = db.Column(db.Float, nullable=True)  # Only for numerical answers
    marks = db.Column(db.Integer, nullable=False)


class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    quiz_id = db.Column(db.Integer(), db.ForeignKey('quiz.id', ondelete='CASCADE'))
    attempt_number = db.Column(db.Integer(), default=1)
    responses = db.relationship('Response', backref='attempt', cascade="all, delete-orphan")
    score = db.Column(db.Integer(), default=0)
    submitted_at = db.Column(db.DateTime(), default=datetime.now)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id', ondelete='CASCADE'))
    answer = db.Column(db.JSON, nullable=False)
    isCorrect = db.Column(db.Boolean)