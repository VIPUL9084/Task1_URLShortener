 Folder Name: Task1_URLShortener
app.py
python
Copy
Edit
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import string
import random

app = Flask(__name__)

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ---------- Routes ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = generate_short_code()

        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        c.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)", (original_url, short_code))
        conn.commit()
        conn.close()

        return render_template('short_code.html', short_code=short_code)
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "Invalid short URL", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
📂 templates/index.html
html
Copy
Edit
<!DOCTYPE html>
<html>
<head>
    <title>URL Shortener</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>URL Shortener</h1>
    <form method="POST">
        <input type="url" name="url" placeholder="Enter your URL" required>
        <button type="submit">Shorten</button>
    </form>
</body>
</html>
📂 templates/short_code.html
html
Copy
Edit
<!DOCTYPE html>
<html>
<head>
    <title>Shortened URL</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Your Shortened URL</h1>
    <p>
        <a href="{{ url_for('redirect_to_url', short_code=short_code, _external=True) }}">
            {{ url_for('redirect_to_url', short_code=short_code, _external=True) }}
        </a>
    </p>
    <a href="{{ url_for('index') }}">Shorten another</a>
</body>
</html>
📂 static/style.css
css
Copy
Edit
body {
    font-family: Arial, sans-serif;
    text-align: center;
    background-color: #f2f2f2;
}

h1 {
    color: #333;
}

form {
    margin-top: 20px;
}

input[type="url"] {
    padding: 10px;
    width: 300px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

button {
    padding: 10px 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
📄 README.md
markdown
Copy
Edit
# Task 1 - URL Shortener

## 📌 Description
A simple Flask-based URL shortener that converts long URLs into short codes and stores them in an SQLite database.

## 🚀 Features
- Shortens any valid URL
- Stores URL mapping in SQLite database
- Redirects short URL to the original URL

## 🛠 Requirements
- Python 3.x
- Flask

## 📥 Installation
```bash
pip install flask
▶ Usage
bash
Copy
Edit
python app.py
Open http://127.0.0.1:5000/ in your browser.

📂 Project Structure
cpp
Copy
Edit
Task1_URLShortener/
├── app.py
├── templates/
│   ├── index.html
│   └── short_code.html
├── static/
│   └── style.css
└── README.md















Ch