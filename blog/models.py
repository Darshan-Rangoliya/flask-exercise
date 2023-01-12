from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f'{self.username}'

class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(300),nullable=False)
    answer = db.Column(db.String(600),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('auth.id'),nullable=False)
    user = db.relationship('UserModel')

    def __repr__(self):
        return f'{self.question}'