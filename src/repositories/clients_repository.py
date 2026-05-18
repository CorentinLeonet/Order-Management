from sqlalchemy.orm import Session
from sqlalchemy import select
from src.Models.Client import Client
from datetime import datetime


def create_client(session: Session, firstname: str, surname : str, email: str, date_of_creation: datetime) -> Client:
    try:
        client = Client(firstname=firstname, surname=surname, email=email, date_of_creation=date_of_creation)
        session.add(client)
        session.commit()
        session.refresh(client)
        return client
    except Exception as e:
        print(e)
    
def get_client_by_id(session: Session, id: int) -> Client:
    try:
        stmt = select(Client).where(Client.id == id)
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_all_clients(session: Session) -> list[Client]:
    try:
        stmt = select(Client)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def update_client(session: Session, client:Client, firstname: str, surname: str, email: str, date_of_creation: datetime):
    try:
        client.firstname = firstname
        client.surname = surname
        client.email = email
        client.date_of_creation = date_of_creation
        session.commit()
    except Exception as e:
        print(e)
        return False
    return True

def delete_client(session: Session, client: Client) -> None:
    try:
        session.delete(client)
        session.commit()
    except Exception as e:
        print(e)

def delete_client_by_id(session: Session, id: int) -> bool:
    try:
        stmt = select(Client).where(Client.id == id)
        client = session.execute(stmt).scalar_one_or_none()

        if client is None:
            return False
        session.delete(client)
        session.commit()
        return True
    except Exception as e:
        print(e)