from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_db_connection():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    return conn


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    feeling = request.form.get('feeling')
    employment_status = request.form.get('employment_status')
    dob = request.form.get('dob')
    gender = request.form.get('gender')
    country = request.form.get('country')
    state = request.form.get('state')

    if not first_name or not last_name or not email or not phone:
        flash('Please fill out all required fields.', 'error')
        return redirect(url_for('form'))

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('''
            INSERT INTO users (first_name, last_name, email, phone, feeling, employment_status, dob, gender, country, state)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        ''', (first_name, last_name, email, phone, feeling, employment_status, dob, gender, country, state))

        conn.commit()
        cur.close()
        conn.close()

        flash('Form submitted successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')

    return redirect(url_for('form'))


if __name__ == '__main__':
    app.run(debug=True)
