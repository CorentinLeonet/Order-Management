from sqlalchemy.orm import Session
from sqlalchemy import select
from src.Models.Category import Category


def create_category(session: Session, name: str, description: str) -> Category:
    try:
        category = Category(name=name, description=description)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    except Exception as e:
        print(e)
    
def get_category_by_id(session: Session, id: int) -> Category:
    try:
        stmt = select(Category).where(Category.id == id)
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_category_by_name(session: Session, name: str) -> Category:
    try:
        stmt = select(Category).where(Category.name == name)
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_all_categories(session: Session) -> list[Category]:
    try:
        stmt = select(Category)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def delete_category(session: Session, category: Category) -> None:
    try:
        session.delete(category)
        session.commit()
    except Exception as e:
        print(e)

def delete_category_by_id(session: Session, id: int) -> bool:
    try:
        stmt = select(Category).where(Category.id == id)
        category = session.execute(stmt).scalar_one_or_none()

        if category is None:
            return False
        session.delete(category)
        session.commit()
        return True
    except Exception as e:
        print(e)

def update_category(session: Session, category: Category, name: str, description: str) -> bool:
    try:
        category.name = name
        category.description = description
        session.commit()
    except Exception  as e:
        print(e)
        return False
    return True