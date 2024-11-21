from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "facebook_login"
}

#connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Create user table if it doesn't exist
def create_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if conn:
            conn.close()

create_table()

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()

            if user:
                return jsonify({"message": "Login successful!"})
            else:
                return jsonify({"message": "Invalid email or password!"})

        except Exception as e:
            return jsonify({"message": f"An error occurred: {e}"})
        finally:
            if conn:
                conn.close()

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            return jsonify({"message": "Account created successfully!"})
        except mysql.connector.errors.IntegrityError:
            return jsonify({"message": "Email already exists!"})
        except Exception as e:
            return jsonify({"message": f"An error occurred: {e}"})
        finally:
            if conn:
                conn.close()

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
