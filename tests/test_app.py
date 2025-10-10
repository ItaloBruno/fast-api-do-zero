from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api_do_zero.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    cliente = TestClient(app)

    resposta = cliente.get("/")

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {"message": "Olá Mundo!"}
