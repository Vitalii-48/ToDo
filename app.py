#__init__.py
from flask import Flask, redirect, render_template, request, url_for, session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('secret_key')

@app.route("/home")
def home():
    username = session.get('username')
    tasks = ["Вивчити Flask", "Зробити CRUD", "Створити Telegram-бота"]
    return render_template('home.html', user=username, todo_list=tasks)

@app.route("/", methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == '123':
            session['username'] = username
            return redirect(url_for('home'))
        else:
            message = 'Неправильний логін або пароль'

    return render_template('login.html', message_html=message)

if __name__ == "__main__":
    app.run(debug=True)