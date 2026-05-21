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

def get_all_categories(session: Session) -> list[Category]:
    try:
        stmt = select(Category)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_count_categories(session: Session) -> int:
    try: 
        stmt = select(func.count(Category.id))
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_categories_count_articles(session: Session):
    try: 
        stmt = select(Category.name, func.count(Article_Category.article_id)).where(Article_Category.category_id == Category.id).group_by(Category.name)
        return session.execute(stmt).fetchall()
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

def update_category(session: Session, category: Category, name: str, description: str) -> bool:
    try:
        category.name = name
        category.description = description
        session.commit()
    except Exception as e:
        print(e)
        return False
    return True