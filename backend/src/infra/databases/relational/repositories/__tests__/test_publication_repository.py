import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from faker import Faker

from src.infra.databases.relational.models import Base
from src.infra.databases.relational.repositories.publication_repository import PublicationRepository
from src.infra.databases.relational.repositories.category_repository import CategoryRepository
from src.core.publication.domain.entities.publication import Publication
from src.core.category.domain.entities.category import Category

class TestPublicationRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.faker = Faker()

    def setUp(self):
        self.session = self.Session()
        self.pub_repo = PublicationRepository(self.session)
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

    def make_publication(self, category=None):
        if category is None:
            category = self.make_category()
        return Publication(
            id=str(uuid4()),
            title=self.faker.sentence(nb_words=6),
            content=self.faker.text(max_nb_chars=200),
            categories=[category],
            outlining=[self.faker.sentence() for _ in range(3)],
            format="blog_post",
            stage="preview",
            thought_ids=[str(uuid4()) for _ in range(2)],
            user_guideline=self.faker.sentence()
        )

    def test__should_save_publication_and_get_by_id(self):
        category = self.make_category()
        publication = self.make_publication(category)
        self.pub_repo.save(publication)
        fetched = self.pub_repo.get_by_id(publication.id)
        self.assertEqual(fetched.id, publication.id)
        self.assertEqual(fetched.title, publication.title)
        self.assertEqual(fetched.content, publication.content)
        self.assertEqual(len(fetched.categories), 1)
        self.assertEqual(fetched.categories[0].id, category.id)
        self.assertEqual(fetched.outlining, publication.outlining)
        self.assertEqual(fetched.format, publication.format)
        self.assertEqual(fetched.stage, publication.stage)
        self.assertEqual(fetched.thought_ids, publication.thought_ids)
        self.assertEqual(fetched.user_guideline, publication.user_guideline)

    def test__should_list_saved_publications(self):
        category = self.make_category()
        publications = [self.make_publication(category) for _ in range(3)]
        for pub in publications:
            self.pub_repo.save(pub)
        all_pubs = self.pub_repo.list()
        self.assertEqual(len(all_pubs), 3)
        ids = {pub.id for pub in all_pubs}
        for pub in publications:
            self.assertIn(pub.id, ids)

    def test__should_delete_publication(self):
        category = self.make_category()
        publication = self.make_publication(category)
        self.pub_repo.save(publication)
        self.pub_repo.delete(publication.id)
        self.assertIsNone(self.pub_repo.get_by_id(publication.id))

    def test__should_update_publication(self):
        category = self.make_category()
        publication = self.make_publication(category)
        self.pub_repo.save(publication)
        # Update fields
        new_title = self.faker.sentence(nb_words=8)
        new_content = self.faker.text(max_nb_chars=300)
        new_outlining = [self.faker.sentence() for _ in range(2)]
        new_format = "linkedin_post"
        new_stage = "ready"
        new_thought_ids = [str(uuid4()) for _ in range(3)]
        new_user_guideline = self.faker.sentence()
        publication.title = new_title
        publication.content = new_content
        publication.outlining = new_outlining
        publication.format = new_format
        publication.stage = new_stage
        publication.thought_ids = new_thought_ids
        publication.user_guideline = new_user_guideline
        self.pub_repo.update(publication)
        updated = self.pub_repo.get_by_id(publication.id)
        self.assertEqual(updated.title, new_title)
        self.assertEqual(updated.content, new_content)
        self.assertEqual(updated.outlining, new_outlining)
        self.assertEqual(updated.format, new_format)
        self.assertEqual(updated.stage, new_stage)
        self.assertEqual(updated.thought_ids, new_thought_ids)
        self.assertEqual(updated.user_guideline, new_user_guideline)

    def test__should_throw_when_not_found(self):
        result = self.pub_repo.get_by_id(str(uuid4()))
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
