from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.Models.Category import Category
from src.Models.Article_Category import Article_Category


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

def get_all_categories_by_name(session: Session, category_name: str):
    try:
        stmt = select(Category).where(Category.name.ilike("%" + category_name + "%"))
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_all_categories(session: Session) -> list[Category]:
    try:
        stmt = select(Category)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_categories_paginated(session: Session, page: int, per_page: int = 10, category_name=""):
    try:
        stmt = select(
                    Category
                ).where(
                    Category.name.ilike("%" + category_name + "%")
                ).order_by(
                    Category.id.desc()
                ).offset(
                    (page - 1) * per_page
                ).limit(
                    per_page
                )
        items = session.execute(stmt).scalars().all()
        stmt2 = select(
                    func.count(Category.id)
                ).where(
                    Category.name.ilike(f"%{category_name}%")
                )
        total = session.execute(stmt2).scalar()

        return items, total
    except Exception as e:
        print(e)

def get_all_active_categories(session: Session) -> list[Category]:
    try:
        stmt = select(Category).where(Category.active == True)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_count_categories(session: Session) -> int:
    try: 
        stmt = select(func.count(Category.id))
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def delete_category(session: Session, category: Category) -> bool:
    try:
        session.delete(category)
        session.commit()
    except Exception as e:
        print(e)
        return False
    return True

def delete_category_by_id(session: Session, id: int) -> bool:
    try:
        stmt = select(Category).where(Category.id == id)
        category = session.execute(stmt).scalar_one_or_none()
        if category is None:
            return False
        session.delete(category)
        session.commit()
    except Exception as e:
        print(e)
        return False
    return True

def update_category(session: Session, category: Category, name: str, description: str, active: bool) -> bool:
    try:
        category.name = name
        category.description = description
        category.active = active
        session.commit()
    except Exception as e:
        print(e)
        return False
    return True