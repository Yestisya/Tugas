from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    # One-to-one relationship with StudentInfo
    student_info = db.relationship('StudentInfo', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'

class StudentInfo(db.Model):
    __tablename__ = 'student_info'
    
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jurusan = db.Column(db.String(100), nullable=False)
    program_studi = db.Column(db.String(100), nullable=False)  # Menambahkan kolom program_studi
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)  # Menambahkan unique=True
    
    # One-to-many relationship with Course
    courses = db.relationship('Course', backref='student', lazy=True, cascade="all, delete-orphan")  # Menambahkan cascade

    def __repr__(self):
        return f'<StudentInfo {self.nama}>'

class Course(db.Model):
    __tablename__ = 'course'
    
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(20), nullable=False)
    mata_kuliah = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    nilai = db.Column(db.String(2), nullable=False)
    
    # Foreign key to StudentInfo
    student_id = db.Column(db.Integer, db.ForeignKey('student_info.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Course {self.mata_kuliah}>'