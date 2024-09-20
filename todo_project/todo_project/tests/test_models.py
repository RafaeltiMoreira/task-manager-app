import pytest
from todo_project import create_app, db
from todo_project.models import User, Task

@pytest.fixture
def app():
    """Configura a aplicação para testes."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Cria um cliente de teste para a aplicação."""
    return app.test_client()

def test_user_creation(app):
    """Teste a criação de um usuário."""
    user = User(username='testuser', password='password')
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.username == 'testuser'
    assert User.query.count() == 1

def test_user_representation(app):
    """Teste a representação do usuário."""
    user = User(username='testuser', password='password')
    db.session.add(user)
    db.session.commit()

    assert repr(user) == "User('testuser')"

def test_task_creation(app):
    """Teste a criação de uma tarefa."""
    user = User(username='testuser', password='password')
    db.session.add(user)
    db.session.commit()

    task = Task(content='Test task', user_id=user.id)
    db.session.add(task)
    db.session.commit()

    assert task.id is not None
    assert task.content == 'Test task'
    assert task.user_id == user.id
    assert Task.query.count() == 1

def test_task_representation(app):
    """Teste a representação da tarefa."""
    user = User(username='testuser', password='password')
    db.session.add(user)
    db.session.commit()

    task = Task(content='Test task', user_id=user.id)
    db.session.add(task)
    db.session.commit()

    assert repr(task) == f"Task('Test task', '{task.date_posted}', '{user.id}')"