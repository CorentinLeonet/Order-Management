from src.repositories import categories_repository
from tests.conftest import CATEGORY_NAME, CATEGORY_DESCRIPTION

category_new_name = "category_test_new"
category_new_description = "Test new description"

def test_create_category(session, category):
    assert category.name == CATEGORY_NAME
    assert category.description == CATEGORY_DESCRIPTION

def test_read_category(session, category):
    fetched = categories_repository.get_category_by_id(session, category.id)
    assert fetched is not None
    assert fetched.id == category.id
    assert fetched.name == CATEGORY_NAME

def test_update_category(session, category):
    assert categories_repository.update_category(session, category, category_new_name, category_new_description) == True
    assert category.name == category_new_name
    assert category.description == category_new_description

def test_delete_category(session, category):
    categories_repository.delete_category(session, category)
    assert categories_repository.get_category_by_id(session, category.id) is None