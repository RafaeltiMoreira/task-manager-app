import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task
from flask_login import login_user, logout_user

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    db.session.remove()
    db.drop_all()

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200

def test_login(client):
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302

def test_register(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_all_tasks(client):
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    with app.test_request_context():
        login_user(user)
    response = client.get('/all_tasks')
    assert response.status_code == 200

def test_add_task(client):
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    with app.test_request_context():
        login_user(user)
    response = client.get('/add_task')
    assert response.status_code == 200

def test_update_task(client):
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    task = Task(content='Test Task', author=user)
    db.session.add(task)
    db.session.commit()
    with app.test_request_context():
        login_user(user)
    task_id = db.session.execute(db.select(Task).filter_by(content='Test Task')).scalar().id
    response = client.get(f'/all_tasks/{task_id}/update_task')
    assert response.status_code == 200

def test_delete_task(client):
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    task = Task(content='Test Task', author=user)
    db.session.add(task)
    db.session.commit()
    with app.test_request_context():
        login_user(user)
    task_id = db.session.execute(db.select(Task).filter_by(content='Test Task')).scalar().id
    response = client.get(f'/all_tasks/{task_id}/delete_task')
    assert response.status_code == 302

def test_account(client):
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    with app.test_request_context():
        login_user(user)
    response = client.get('/account')
    assert response.status_code == 200

def test_change_password(client):
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    with app.test_request_context():
        login_user(user)
    response = client.get('/account/change_password')
    assert response.status_code == 200