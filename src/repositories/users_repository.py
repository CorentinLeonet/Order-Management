from sqlalchemy.orm import Session
from sqlalchemy import select
from src.Models.User import User
from datetime import datetime


def create_user(session: Session, username: str, date_of_creation: datetime) -> User:
    try:
        user = User(username=username, date_of_creation=date_of_creation)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        print(e)
    
def get_user_by_id(session: Session, id: int) -> User:
    try:
        stmt = select(User).where(User.id == id)
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_all_users(session: Session) -> list[User]:
    try:
        stmt = select(User)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def delete_user(session: Session, user: User) -> None:
    try:
        session.delete(user)
        session.commit()
    except Exception as e:
        print(e)

def delete_user_by_id(session: Session, id: int) -> bool:
    try:
        stmt = select(User).where(User.id == id)
        user = session.execute(stmt).scalar_one_or_none()

        if user is None:
            return False
        session.delete(user)
        session.commit()
        return True
    except Exception as e:
        print(e)