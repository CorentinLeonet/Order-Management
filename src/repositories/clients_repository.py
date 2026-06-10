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

def get_clients_paginated(session: Session, page: int, per_page: int = 10, client_name=""):
    try:
        stmt = select(
                    Client
                ).where(
                    Client.surname.ilike("%" + client_name + "%")
                ).order_by(
                    Client.id.desc()
                ).offset(
                    (page - 1) * per_page
                ).limit(
                    per_page
                )
        items = session.execute(stmt).scalars().all()
        stmt2 = select(
                    func.count(Client.id)
                ).where(
                    Client.surname.ilike(f"%{client_name}%")
                )
        total = session.execute(stmt2).scalar()

        return items, total
    except Exception as e:
        print(e)

def get_all_active_clients(session: Session) -> list[Client]:
    try:
        stmt = select(Client).where(Client.active == True)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_count_clients(session: Session) -> int:
    try: 
        stmt = select(func.count(Client.id))
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_all_clients_by_name(session: Session, client_name: str):
    try:
        stmt = select(Client).where(Client.surname.ilike("%" + client_name + "%"))
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)


def update_client(session: Session, client:Client, firstname: str, surname: str, email: str, date_of_creation: datetime, active: bool):
    try:
        client.firstname = firstname
        client.surname = surname
        client.email = email
        client.date_of_creation = date_of_creation
        client.active = active
        session.commit()
    except Exception as e:
        print(e)
        return False
    return True

def delete_client(session: Session, client: Client) -> bool:
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
    