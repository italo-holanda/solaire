import unittest
from uuid import uuid4
from faker import Faker
from backend.core.publication.domain.entities.publication import Publication
from backend.core.category.domain.entities.category import Category

faker = Faker()

class TestPublication(unittest.TestCase):
    def make_category(self):
        return Category(
            id=str(uuid4()),
            name=faker.word(),
            color=faker.color_name()
        )

    def test__should_instantiate_correctly(self):
        id = str(uuid4())
        title = faker.sentence(nb_words=6)
        content = faker.text(max_nb_chars=200)
        categories = [self.make_category() for _ in range(2)]
        outlining = [faker.sentence() for _ in range(3)]
        publication_format = "blog_post"
        stage = "preview"
        thought_ids = [str(uuid4()) for _ in range(2)]
        user_guideline = faker.sentence()

        publication = Publication(
            id=id,
            title=title,
            content=content,
            categories=categories,
            outlining=outlining,
            format=publication_format,
            stage=stage,
            thought_ids=thought_ids,
            user_guideline=user_guideline
        )

        self.assertIsNotNone(publication)
        self.assertEqual(publication.id, id)
        self.assertEqual(publication.title, title)
        self.assertEqual(publication.content, content)
        self.assertEqual(publication.categories, categories)
        self.assertEqual(publication.outlining, outlining)
        self.assertEqual(publication.format, publication_format)
        self.assertEqual(publication.stage, stage)
        self.assertEqual(publication.thought_ids, thought_ids)
        self.assertEqual(publication.user_guideline, user_guideline)

    def test__should_fail_with_invalid_format(self):
        with self.assertRaises(ValueError):
            Publication(
                title=faker.sentence(),
                content=faker.text(),
                categories=[self.make_category()],
                outlining=[faker.sentence()],
                format="invalid_format",
                stage="preview",
                thought_ids=[str(uuid4())],
                user_guideline=faker.sentence()
            )

    def test__should_fail_with_invalid_stage(self):
        with self.assertRaises(ValueError):
            Publication(
                title=faker.sentence(),
                content=faker.text(),
                categories=[self.make_category()],
                outlining=[faker.sentence()],
                format="blog_post",
                stage="invalid_stage",
                thought_ids=[str(uuid4())],
                user_guideline=faker.sentence()
            )

if __name__ == "__main__":
    unittest.main() 