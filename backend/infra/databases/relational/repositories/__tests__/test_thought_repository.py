import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from faker import Faker

from backend.infra.databases.relational.models import Base
from backend.infra.databases.relational.repositories.thought_repository import ThoughtRepository
from backend.infra.databases.relational.repositories.category_repository import CategoryRepository
from backend.core.thought.domain.entities.thought import Thought
from backend.core.category.domain.entities.category import Category

class TestThoughtRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.faker = Faker()

    def setUp(self):
        self.session = self.Session()
        self.repo = ThoughtRepository(self.session)
        self.cat_repo = CategoryRepository(self.session)

    def tearDown(self):
        self.session.close()
        with self.engine.connect() as conn:
            for tbl in reversed(Base.metadata.sorted_tables):
                conn.execute(tbl.delete())
            conn.commit()

    def make_category(self):
        category = Category(id=str(uuid4()), name=self.faker.word(), color=self.faker.color_name())
        self.cat_repo.save(category)
        return category

    def make_thought(self, category=None):
        if category is None:
            category = self.make_category()
        text = self.faker.text(max_nb_chars=200) + (" lorem ipsum" * 10)  # ensure >100 chars
        return Thought(
            id=str(uuid4()),
            title=self.faker.sentence(nb_words=6),
            summary=self.faker.sentence(nb_words=12),
            text=text,
            categories=[category],
            embeddings=[]
        )

    def test__should_save_thought_and_get_by_id(self):
        category = self.make_category()
        thought = self.make_thought(category)
        self.repo.save(thought)
        fetched = self.repo.get_by_id(thought.id)
        self.assertEqual(fetched.id, thought.id)
        self.assertEqual(fetched.title, thought.title)
        self.assertEqual(fetched.summary, thought.summary)
        self.assertEqual(fetched.text, thought.text)
        self.assertEqual(len(fetched.categories), 1)
        self.assertEqual(fetched.categories[0].id, category.id)
        self.assertEqual(fetched.embeddings, [])

    def test__should_list_saved_thoughts(self):
        category = self.make_category()
        thoughts = [self.make_thought(category) for _ in range(3)]
        for t in thoughts:
            self.repo.save(t)
        all_thoughts = self.repo.list()
        self.assertEqual(len(all_thoughts), 3)
        ids = {t.id for t in all_thoughts}
        for t in thoughts:
            self.assertIn(t.id, ids)

    def test__should_delete_thought(self):
        category = self.make_category()
        thought = self.make_thought(category)
        self.repo.save(thought)
        self.repo.delete(thought.id)
        with self.assertRaises(ValueError):
            self.repo.get_by_id(thought.id)

    def test__should_update_thought(self):
        category1 = self.make_category()
        category2 = self.make_category()

        thought = self.make_thought(category1)
        self.repo.save(thought)

        new_text = self.faker.text(max_nb_chars=200) + (" lorem ipsum" * 10)
        new_summary = self.faker.sentence(nb_words=15)
        new_title = self.faker.sentence(nb_words=8)
        thought.text = new_text
        thought.summary = new_summary
        thought.title = new_title
        thought.categories = [category2]
        self.repo.update(thought)
 
        updated = self.repo.get_by_id(thought.id)
        self.assertEqual(updated.text, new_text)
        self.assertEqual(updated.summary, new_summary)
        self.assertEqual(updated.title, new_title)
        self.assertEqual(len(updated.categories), 1)
        self.assertEqual(updated.categories[0].id, category2.id)

    def test__should_throw_when_not_found(self):
        with self.assertRaises(ValueError):
            self.repo.get_by_id(str(uuid4()))

if __name__ == "__main__":
    unittest.main()
