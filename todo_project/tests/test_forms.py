import pytest
from todo_project import app, forms

@pytest.fixture
def app_context():
    with app.app_context():
        yield

@pytest.mark.parametrize("FormClass,expected_fields", [
    (forms.RegistrationForm, ['username', 'password', 'confirm_password', 'submit']),
    (forms.LoginForm, ['username', 'password', 'submit']),
    (forms.UpdateUserInfoForm, ['username', 'submit']),
    (forms.UpdateUserPassword, ['old_password', 'new_password', 'submit']),
    (forms.TaskForm, ['task_name', 'submit']),
    (forms.UpdateTaskForm, ['task_name', 'submit'])
])
def test_form_fields(app_context, FormClass, expected_fields):
    with app.test_request_context():
        form = FormClass()
        for field in expected_fields:
            assert hasattr(form, field)