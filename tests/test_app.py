from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_api_do_zero.app import app


@pytest.fixture
def cliente():
    return TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo(cliente):
    resposta = cliente.get("/")

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {"message": "Olá Mundo!"}


def test_root_deve_retornar_ok_e_ola_mundo_em_formato_html(cliente):
    cliente = TestClient(app)

    resposta = cliente.get("/html")

    assert resposta.status_code == HTTPStatus.OK
    assert (
        resposta.text
        == """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""
    )


def test_create_user(cliente):
    response = cliente.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def test_read_users(cliente):
    response = cliente.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "alice",
                "email": "alice@example.com",
                "id": 1,
            }
        ]
    }


def test_update_user(cliente):
    response = cliente.put(
        "/users/0",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}

    response = cliente.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_delete_user(cliente):
    response = cliente.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}
