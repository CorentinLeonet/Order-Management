from src.repositories import clients_repository as clients_repository
from datetime import datetime
from tests.conftest import CLIENT_FIRSTNAME, CLIENT_SURNAME, CLIENT_EMAIL, CLIENT_DATE


client_new_firstname = "client_new_firstname"
client_new_surname = "client_new_surname"
client_new_email = "client_new_email"
client_new_date = datetime.strptime("21/05/2026", "%d/%m/%Y")


def test_create_client(session, client):
    assert client.firstname == CLIENT_FIRSTNAME
    assert client.surname == CLIENT_SURNAME
    assert client.email == CLIENT_EMAIL
    assert client.date_of_creation == CLIENT_DATE


def test_read_client(session, client):
    fetched_client = clients_repository.get_client_by_id(session, client.id)
    assert fetched_client.firstname == CLIENT_FIRSTNAME
    assert fetched_client.surname == CLIENT_SURNAME
    assert fetched_client.email == CLIENT_EMAIL
    assert fetched_client.date_of_creation == CLIENT_DATE

def test_update_client(session, client):
    assert clients_repository.update_client(session, client, client_new_firstname, client_new_surname, client_new_email, client_new_date, True) == True
    assert client.firstname == client_new_firstname
    assert client.surname == client_new_surname
    assert client.email == client_new_email
    assert client.date_of_creation == client_new_date

def test_delete_client(session, client):
    clients_repository.delete_client(session, client)
    assert clients_repository.get_client_by_id(session, client.id) is None