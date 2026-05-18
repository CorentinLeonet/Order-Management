from sqlalchemy.orm import Session
from sqlalchemy import select
from src.Models.Client import Client


def create_client(session: Session, name: str, description: str) -> Client:
    try:
        client = Client(name=name, description=description)
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