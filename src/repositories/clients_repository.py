from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.Models.Client import Client
from src.Models.Order import Order
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

def get_count_clients(session: Session) -> int:
    try: 
        stmt = select(func.count(Client.id))
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_clients_count_orders(session: Session):
    try: 
        stmt = select(func.concat(Client.firstname, Client.surname), func.count(Order.id)).where(Order.client_id == Client.id).group_by(func.concat(Client.firstname, Client.surname), Client.id)
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)

def get_all_clients_by_name(session: Session, client_name: str):
    try:
        stmt = select(Client).where(Client.surname.ilike("%" + client_name + "%"))
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
        return False
    return True

def delete_client_by_id(session: Session, id: int) -> bool:
    try:
        stmt = select(Client).where(Client.id == id)
        client = session.execute(stmt).scalar_one_or_none()

        if client is None:
            return False
        session.delete(client)
        session.commit()
    except Exception as e:
        print(e)
        return False
    return True
    