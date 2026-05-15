import gc

import pytest
import app
import database as db
import os

DB_TEST = 'test_todo.db'

@pytest.fixture
def client():
    db.DB_NAME = DB_TEST
    if os.path.exists(db.DB_NAME):
        os.remove(db.DB_NAME)
    db.init_database()
    app.app.config['TESTING'] = True
    yield app.app.test_client()
    gc.collect()
    os.remove(db.DB_NAME)


# Тестовий адмін
@pytest.fixture
def test_admin():
    db.add_user('test_admin', '123', 30)
    yield 'test_admin'


# Публічні сторінки
def test_publik_page(client):
    for url, text in {
            '/': 'Вітаю',
            '/login': 'Login',
            '/register': 'Реєстрація',
            'index': 'Головна'
        }.items():
        response = client.get(url)
        assert response.status_code == 200
        assert text in response.get_data(as_text=True)

# Захищені сторінки без логіну
def test_protected_page_redirect_content(client):
    for url in ['/tasks', '/add_task', '/admin']:
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        assert 'Login' in response.get_data(as_text=True)

# Логін
def test_login_success(client, test_admin):
    response = client.post('/login', data={'username': test_admin,'password':'123'}, follow_redirects=True)
    assert 'Список завдань' in response.get_data(as_text=True)

def test_login_fail(client, test_admin):
    response = client.post('/login', data={'username':test_admin,'password':'wrong'}, follow_redirects=True)
    assert 'Неправильний логін або пароль' in response.get_data(as_text=True)

# Реєстрація
def test_register_new_user(client):
    response = client.post('/register', data={'username': 'test_user', 'password':'123','age':'20'}, follow_redirects=True)
    assert 'Реєстрація пройшла успішно' in response.get_data(as_text=True)

# Реєстрація існуючого користувача
def test_register_existing_user(client):
    db.add_user('test_user', '123', 30)
    response = client.post('/register', data={'username':'test_user', 'password':'123','age':'20'}, follow_redirects=True)
    assert 'Користувач вже існує' in response.get_data(as_text=True)
