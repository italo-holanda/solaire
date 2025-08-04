import unittest
from datetime import datetime
from uuid import uuid4
from faker import Faker
from src.core.thought.domain.entities.thought import Thought
from src.core.category.domain.entities.category import Category

faker = Faker()


class TestThought(unittest.TestCase):
    def make_category(self):
        return Category(
            id=str(uuid4()),
            name=faker.word(),
            color=faker.color_name()
        )

    def test__should_instantiate_correctly(self):
        id = str(uuid4())
        title = faker.sentence(nb_words=6)
        summary = faker.sentence(nb_words=12)
        text = faker.text(max_nb_chars=200) + \
            (" lorem ipsum" * 10)  # ensure >100 chars
        categories = [self.make_category() for _ in range(2)]
        embeddings = [faker.pyfloat(left_digits=1, right_digits=5)
                      for _ in range(5)]

        # Passing id
        thought = Thought(
            id=id,
            title=title,
            summary=summary,
            text=text,
            categories=categories,
            embeddings=embeddings
        )

        self.assertIsNotNone(thought)
        self.assertEqual(thought.id, id)
        self.assertEqual(thought.title, title)
        self.assertEqual(thought.summary, summary)
        self.assertEqual(thought.text, text)
        self.assertEqual(thought.categories, categories)
        self.assertEqual(thought.embeddings, embeddings)
        self.assertIsInstance(thought.created_at, datetime)
        self.assertIsInstance(thought.updated_at, datetime)
        self.assertIsNone(thought.deleted_at)

        # Without passing id
        thought = Thought(
            title=title,
            summary=summary,
            text=text,
            categories=categories,
            embeddings=embeddings
        )

        self.assertIsNotNone(thought)
        self.assertIsNotNone(thought.id, id)
        self.assertEqual(thought.title, title)
        self.assertEqual(thought.summary, summary)
        self.assertEqual(thought.text, text)
        self.assertEqual(thought.categories, categories)
        self.assertEqual(thought.embeddings, embeddings)
        self.assertIsInstance(thought.created_at, datetime)
        self.assertIsInstance(thought.updated_at, datetime)
        self.assertIsNone(thought.deleted_at)

    def test__text_must_not_be_too_short(self):
        with self.assertRaises(ValueError):
            Thought(
                title=faker.sentence(),
                summary=faker.sentence(),
                text="short text",
                categories=[self.make_category()],
                embeddings=[0.1, 0.2]
            )

    def test__text_must_not_be_too_long(self):
        long_text = "a" * 1001
        with self.assertRaises(ValueError):
            Thought(
                title=faker.sentence(),
                summary=faker.sentence(),
                text=long_text,
                categories=[self.make_category()],
                embeddings=[0.1, 0.2]
            )

    def test__text_must_be_validated_when_updated(self):
        thought = Thought(
            title=faker.sentence(),
            summary=faker.sentence(),
            text=faker.text(max_nb_chars=200) + (" lorem ipsum" * 10),
            categories=[self.make_category()],
            embeddings=[0.1, 0.2]
        )

        with self.assertRaises(ValueError):
            thought.text = "short text"

        with self.assertRaises(ValueError):
            thought.text = "a" * 1001

        valid_text = faker.text(max_nb_chars=200) + (" lorem ipsum" * 10)
        thought.text = valid_text
        self.assertEqual(thought.text, valid_text)


if __name__ == "__main__":
    unittest.main()
