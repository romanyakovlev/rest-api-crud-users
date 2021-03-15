from rest_framework.authtoken.models import Token
import pytest
import json


def make_token_credentials(client, token):
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


# fixtures


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_token_and_user(db, create_user):
    def make_token(**kwargs):
        data = {"username": "username", "password": "password", "is_superuser": True}
        user = create_user(**data)
        token, _ = Token.objects.get_or_create(user=user)
        return token
    return make_token


# tests


@pytest.mark.django_db
def test_view_token_auth_200_status(api_client, create_user):
    url = '/api/v1/api-token-auth/'
    data = {"username": "username", "password": "password"}
    user = create_user(**data)
    response = api_client.post(url, data=data)
    assert response.status_code == 200
    assert json.loads(response.content)['token'] == user.auth_token.key


@pytest.mark.django_db
def test_view_token_auth_400_status(api_client, create_user):
    url = '/api/v1/api-token-auth/'
    data = {"username": "username", "password": "password"}
    invalid_data = {"username": "username1", "password": "password1"}
    _ = create_user(**data)
    response = api_client.post(url, data=invalid_data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_view_list_200_status(api_client, create_token_and_user):
    url = '/api/v1/users/'
    token = create_token_and_user()
    make_token_credentials(api_client, token)
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_list_401_status(api_client):
    url = '/api/v1/users/'
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_view_create_201_status(api_client, create_token_and_user):
    url = '/api/v1/users/'
    token = create_token_and_user()
    make_token_credentials(api_client, token)
    data = {
        'username': 'username1',
        'first_name': 'first_name1',
        'last_name': 'last_name1',
        'password': 'password1',
        'is_active': True,
    }
    response = api_client.post(url, data=data)
    assert response.status_code == 201
    assert json.loads(response.content) == data


@pytest.mark.django_db
def test_view_create_401_status(api_client):
    url = '/api/v1/users/'
    response = api_client.post(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_view_retrieve_200_status(api_client, create_token_and_user):
    url = '/api/v1/users/1/'
    token = create_token_and_user()
    make_token_credentials(api_client, token)
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_retrieve_401_status(api_client, create_user):
    url = '/api/v1/users/1/'
    data = {"username": "username", "password": "password"}
    _ = create_user(**data)
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_view_update_200_status(api_client, create_token_and_user):
    url = '/api/v1/users/1/'
    token = create_token_and_user()
    make_token_credentials(api_client, token)
    data = {
        'username': 'username',
        'first_name': 'first_name1',
        'last_name': 'last_name1',
        'password': 'password',
        'is_active': True,
    }
    response = api_client.patch(url, data=data)
    assert response.status_code == 200
    assert json.loads(response.content) == data


@pytest.mark.django_db
def test_view_update_404_status(api_client, create_token_and_user):
    url = '/api/v1/users/2/'
    token = create_token_and_user()
    make_token_credentials(api_client, token)
    data = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'password': 'password',
        'is_active': True,
    }
    response = api_client.patch(url, data=data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_view_update_401_status(api_client):
    url = '/api/v1/users/1/'
    response = api_client.patch(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_view_partial_update_200_status(api_client, create_token_and_user):
    url = '/api/v1/users/1/'
    token = create_token_and_user()
    make_token_credentials(api_client, token)
    data = {
        'username': 'username',
        'first_name': 'first_name1',
        'last_name': 'last_name1',
        'password': 'password',
        'is_active': True,
    }
    response = api_client.put(url, data=data)
    assert response.status_code == 200
    assert json.loads(response.content) == data


@pytest.mark.django_db
def test_view_partial_update_404_status(api_client, create_token_and_user):
    url = '/api/v1/users/2/'
    token = create_token_and_user()
    make_token_credentials(api_client, token)
    data = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'password': 'password',
        'is_active': True,
    }
    response = api_client.put(url, data=data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_view_partial_update_401_status(api_client):
    url = '/api/v1/users/1/'
    response = api_client.put(url)
    assert response.status_code == 401
