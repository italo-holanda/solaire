import unittest
from uuid import uuid4
from faker import Faker
from pydantic import ValidationError
from src.core.category.domain.entities.category import Category

faker = Faker()


class TestCategory(unittest.TestCase):
    def test__should_instantiate_correctly(self):
        id = str(uuid4())
        name = faker.word()
        color = faker.color_name()

        category = Category(
            id=id,
            name=name,
            color=color
        )

        self.assertIsNotNone(category)
        self.assertEqual(category.id, id)
        self.assertEqual(category.name, name)
        self.assertEqual(category.color, color)

    def test__should_auto_generate_color_when_not_provided(self):
        id = str(uuid4())
        name = faker.word()
        category = Category(
            id=id,
            name=name
        )
        self.assertIsNotNone(category.color)
        self.assertRegex(category.color, r"^#[0-9a-fA-F]{6}$")

    def test__should_fail_with_missing_fields(self):
        with self.assertRaises(ValidationError):
            Category(
                id=str(uuid4()),
                color=faker.color_name()
            )


if __name__ == "__main__":
    unittest.main()
