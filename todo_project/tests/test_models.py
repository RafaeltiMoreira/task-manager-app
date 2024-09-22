import pytest
from tests import app
from todo_project import db, create_app
from todo_project.models import User, Task

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.app_context().push()
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()

def test_user_model(app):
    user = User(username='testuser', password='testpassword')
    db.session.add(user)
    db.session.commit()
    assert user.id == 1
    assert user.username == 'testuser'
    assert user.password == 'testpassword'

def test_task_model(app):
    user = User(username='testuser', password='testpassword')
    db.session.add(user)
    db.session.commit()
    task = Task(content='Test task', user_id=user.id)
    db.session.add(task)
    db.session.commit()
    assert task.id == 1
    assert task.content == 'Test task'
    assert task.date_posted is not None
    assert task.user_id == user.id

def test_user_tasks_relationship(app):
    user = User(username='testuser', password='testpassword')
    db.session.add(user)
    db.session.commit()
    task1 = Task(content='Task 1', user_id=user.id)
    task2 = Task(content='Task 2', user_id=user.id)
    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()
    assert user.tasks == [task1, task2]

def test_task_author_relationship(app):
    user = User(username='testuser', password='testpassword')
    db.session.add(user)
    db.session.commit()
    task = Task(content='Test task', user_id=user.id)
    db.session.add(task)
    db.session.commit()
    assert task.author == user