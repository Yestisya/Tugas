from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia Anda

# Konfigurasi Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uasdb'

mysql = MySQL(app)

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('datadiri'))
    return render_template('signin.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM user WHERE username = %s", (username,))
            user = cur.fetchone()
        
        if user and check_password_hash(user[3], password):  # Pastikan index 3 adalah password
            session['user_id'] = user[0]  # Simpan user_id di session
            session['username'] = user[1]  # Simpan username di session
            flash('Login berhasil!', 'success')
            return redirect(url_for('datadiri'))
        else:
            flash('Username atau password salah.', 'danger')
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, password))
            mysql.connection.commit()

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/datadiri', methods=['GET', 'POST'])
def datadiri():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    
    user_id = session['user_id']
    with mysql.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM student_info WHERE user_id = %s", (user_id,))
        student = cursor.fetchone()  # Ambil data mahasiswa

    if request.method == 'POST':
        if not student:
            nim = request.form['nim']
            nama = request.form['nama']
            jurusan = request.form['jurusan']
            program_studi = request.form['program_studi']  # Ambil program studi dari form
            with mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO student_info (nim, nama, jurusan, program_studi, user_id) VALUES (%s, %s, %s, %s, %s)", 
                               (nim, nama, jurusan, program_studi, user_id))
                mysql.connection.commit()
            flash('Data berhasil disimpan!', 'success')
            return redirect(url_for('datadiri'))  # Redirect untuk menampilkan data yang baru disimpan

    # Tampilkan data mahasiswa yang sudah diinput
    return render_template('datadiri.html', student=student)

@app.route('/krs', methods=['GET', 'POST'])
def krs():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    
    user_id = session['user_id']
    
    # Ambil data mahasiswa
    with mysql.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM student_info WHERE user_id = %s", (user_id,))
        student = cursor.fetchone()
    
    # Jika data mahasiswa tidak ditemukan, kembalikan ke halaman login atau berikan pesan error
    if not student:
        flash('Data mahasiswa tidak ditemukan. Silakan login ulang.', 'error')
        return redirect(url_for('signin'))

    if request.method == 'POST':
        kode = request.form['kode']
        mata_kuliah = request.form['mata_kuliah']
        sks = request.form['sks']
        nilai = request.form['nilai']
        
        # Simpan data mata kuliah ke database
        with mysql.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO course (kode, mata_kuliah, sks, nilai, student_id) 
                VALUES (%s, %s, %s, %s, %s)
            """, (kode, mata_kuliah, sks, nilai, student[0]))  # student[0] adalah ID mahasiswa
            mysql.connection.commit()
        
        flash('Mata kuliah berhasil ditambahkan!', 'success')
        return redirect(url_for('krs'))  # Redirect untuk mencegah pengiriman ulang form
    
    # Ambil daftar mata kuliah mahasiswa
    with mysql.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM course WHERE student_id = %s", (student[0],))
        courses = cursor.fetchall()
    
    return render_template('krs.html', student=student, courses=courses)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)  # Hapus username dari session
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)