# main.py

from flask import Flask, redirect, render_template, request, url_for, session, flash
from dotenv import load_dotenv
from datetime import datetime
import os
import database as db

from pprint import pprint

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('secret_key')
db.init_database()

#
@app.route('/')
def welcome():
    return render_template('welcome.html')

#
@app.route("/index")
def home():
    username = session.get('username')
    tasks = ["Вивчити Flask", "Зробити CRUD", "Створити Telegram-бота"]
    return render_template('index.html', username=username, todo_list=tasks)

#
@app.route("/login", methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user(username)
        if user and user[2] == password:
            session['username'] = username
            session['role'] = user[4]
            if session ['role'] == 'admin':
                return redirect(url_for('admin_board'))
            return redirect(url_for('tasks'))
        else:
            message = 'Неправильний логін або пароль'

    return render_template('login.html', message_html=message)

#
@app.route("/admin")
def admin_board():
    users = db.get_all_users()
    tasks = db.get_all_tasks()
    pprint(users)
    pprint(tasks)

    tasks_by_users = {}

    for user in users:
        list_tasks = []
        for task in tasks:
            list_tasks.append(task) if task[1] == user[0] else None
        tasks_by_users.setdefault(user[0], list_tasks)
    pprint(tasks_by_users)
    return render_template('admin.html', users=users, tasks=tasks_by_users)

#
@app.route("/register", methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        try:
            db.add_user(username, password, age)
            session['username'] = username
            flash("Реєстрація пройшла успішно")
            return redirect(url_for('tasks'))
        except Exception as e:
            message = "Користувач вже існує"
    return render_template('register.html', message=message)

#
@app.route("/delete_account", methods=['POST'])
def delete_account():
    if "username" not in  session:
        return redirect(url_for('login'))
    user = db.get_user(session['username'])
    user_id = user[0]
    db.delete_user(user_id)
    session.clear()
    print("Акаунт успішно видалено")
    flash("Акаунт успішно видалено")
    return redirect(url_for('welcome'))

#
priority_map = {1: "Низький", 2: "Середній", 3: "Високий"}
@app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    if "username" not in session:
        return redirect(url_for('login'))

    user = db.get_user(session['username'])
    user_id = user[0]
    if request.method == 'POST':
        task_id = request.form['task_id']
        done_value = 'done' in request.form
        db.toggle_task_done(task_id, done_value)

    status = request.args.get('status')
    priority = request.args.get('priority')

    todo_list = db.get_filtr_tasks(user_id, status, priority)
    return render_template(
        'tasks.html',
        username=session['username'],
        todo_list=todo_list,
        priority_map=priority_map,
        status=status,
        priority=priority)

#
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    db.delete_task(task_id)
    return redirect(url_for('tasks'))

#
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if "username" not in session:
        return redirect(url_for('login'))

    user = db.get_user(session['username'])
    user_id = user[0]

    if request.method == 'POST':
        description = request.form['description']
        creat_at = datetime.now().date()
        due_at = request.form['due_at']
        priority = request.form['priority']
        db.add_task(user_id, description, creat_at, due_at, priority)
        return redirect(url_for('tasks'))
    return render_template('add_task.html')

#
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if "username" not in session:
        return redirect(url_for('login'))

    task = db.get_task(task_id)
    if request.method == 'POST':
        description = request.form['description']
        due_at = request.form['due_at']
        priority = request.form['priority']
        db.update_task(task_id, description, due_at, priority)
        flash("Задача оновлена")
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', task=task, priority_map=priority_map)

#
@app.route("/admin/delete_user/<int:user_id>", methods=['POST'])
def admin_delete_user(user_id):
    if "username" not in session or session.get("role") != "admin":
        flash("Доступ заборонено")
        return redirect(url_for("login"))

    db.delete_user(user_id)
    flash("Користувач видалений")
    return redirect(url_for("admin_board"))

#
@app.route("/admin/delete_task/<int:task_id>", methods=['POST'])
def admin_delete_task(task_id):
    if "username" not in session or session.get("role") != "admin":
        flash("Доступ заборонено")
        return redirect(url_for("login"))

    db.delete_task(task_id)
    flash("Задача видалена")
    return redirect(url_for("admin_board"))
if __name__ == "__main__":
    app.run(debug=True)