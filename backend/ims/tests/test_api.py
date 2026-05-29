import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        email='testuser@ims.test',
        password='TestPass123!',
        first_name='Test',
        last_name='User',
        role='student',
        username='testuser'
    )
    assert user.email == 'testuser@ims.test'
    assert user.role == 'student'

@pytest.mark.django_db
def test_login_endpoint(client):
    user = User(
        email='login@ims.test',
        first_name='Login',
        last_name='User',
        role='student',
        username='loginuser'
    )
    user.set_password('TestPass123!')
    user.save()
    response = client.post('/api/v1/auth/login/', {
        'username': 'login@ims.test',
        'password': 'TestPass123!'
    }, content_type='application/json')
    print("RESPONSE BODY:", response.json())
    assert response.status_code == 200
    assert 'access' in response.json()

@pytest.mark.django_db
def test_unauthenticated_access(client):
    response = client.get('/api/v1/students/')
    assert response.status_code == 401

@pytest.mark.django_db
def test_admin_user_creation():
    admin = User.objects.create_superuser(
        email='admin@ims.test',
        password='AdminPass123!',
        first_name='Admin',
        last_name='User',
        username='adminuser'
    )
    assert admin.is_staff == True
