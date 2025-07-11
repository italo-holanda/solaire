import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from faker import Faker

from backend.infra.databases.relational.models import Base
from backend.infra.databases.relational.repositories.category_repository import CategoryRepository
from backend.core.category.domain.entities.category import Category

class TestCategoryRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use in-memory SQLite for isolation
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.faker = Faker()

    def setUp(self):
        self.session = self.Session()
        self.repo = CategoryRepository(self.session)

    def tearDown(self):
        self.session.close()
        with self.engine.connect() as conn:
            for tbl in reversed(Base.metadata.sorted_tables):
                conn.execute(tbl.delete())
            conn.commit()

    def test__should_save_category_and_get_by_id(self):
        category_id = str(uuid4())
        name = self.faker.word()
        color = self.faker.color_name()
        category = Category(id=category_id, name=name, color=color)
        self.repo.save(category)
        fetched = self.repo.get_by_id(category_id)
        self.assertEqual(fetched.id, category_id)
        self.assertEqual(fetched.name, name)
        self.assertEqual(fetched.color, color)

    def test__should_list_saved_categories(self):
        categories = [
            Category(id=str(uuid4()), name=self.faker.word(), color=self.faker.color_name())
            for _ in range(3)
        ]
        for cat in categories:
            self.repo.save(cat)
        all_categories = self.repo.list()
        self.assertEqual(len(all_categories), 3)
        ids = {cat.id for cat in all_categories}
        for cat in categories:
            self.assertIn(cat.id, ids)

    def test__should_delete_category(self):
        category_id = str(uuid4())
        category = Category(id=category_id, name=self.faker.word(), color=self.faker.color_name())
        self.repo.save(category)
        self.repo.delete(category_id)
        with self.assertRaises(ValueError):
            self.repo.get_by_id(category_id)

    def test__should_throw_when_not_found(self):
        with self.assertRaises(ValueError):
            self.repo.get_by_id(str(uuid4()))

    def test__should_find_by_name(self):
        category_id = str(uuid4())
        name = self.faker.word()
        color = self.faker.color_name()
        category = Category(id=category_id, name=name, color=color)
        self.repo.save(category)
        fetched = self.repo.get_by_name(name)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.id, category_id)
        self.assertEqual(fetched.name, name)
        self.assertEqual(fetched.color, color)

if __name__ == "__main__":
    unittest.main()
