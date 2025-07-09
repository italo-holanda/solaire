from typing import List
import unittest

from backend.infra.agents.thought_interpreter_agent import ThoughtInterpreterAgent
from backend.core.thought.domain.entities.thought import Thought
from backend.core.category.domain.entities.category import Category


_TEXT_EXAMPLE = """
I think unit testing in Python is one of those things
I used to brush off, but now I see it differently.
At first, it felt like extra work—writing tests for
something I just finished coding? Hmm, felt redundant.
But over time, I realized tests are more like a
conversation with your future self. They say, “Hey,
this is what I expected back then.” So when things break—
and they will—those tests become your guide. It's not just
about catching bugs; it's about designing with clarity.
Like, if something's hard to test, maybe it's too complex.
That thought changed the way I code.
"""

_TITLE_EXAMPLE = "Unit testing with Python"

_SUMMARY_EXAMPLE = """
Unit testing felt tedious at first, but now I see it as 
a guide and design tool for future clarity.
"""


class TestThoughtInterpreterAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ThoughtInterpreterAgent()

    def make_category(self):
        return Category(name='Test', color='blue')

    def test_agent_instantiates(self):
        self.assertIsInstance(self.agent, ThoughtInterpreterAgent)

    def test__summary_generator_should_generate_a_valid_str(self):
        thought = Thought(
            text=_TEXT_EXAMPLE,
            title=_TITLE_EXAMPLE,
            summary='',
            embeddings=[],
            categories=[Category(
                name='Python'
            )]
        )
        thought = self.agent._summary_generator(thought)
        assert isinstance(thought.get('summary'), str)
        assert len(thought.get('summary')) >= 55

    def test__title_generator_should_generate_a_valid_str(self):
        thought = Thought(
            text=_TEXT_EXAMPLE,
            title='',
            summary=_SUMMARY_EXAMPLE,
            embeddings=[],
            categories=[Category(
                name='Python'
            )]
        )
        thought = self.agent._title_generator(thought)
        assert isinstance(thought.get('title'), str)
        assert len(thought.get('title')) >= 25

    def test__category_extractor_should_extract_categories(self):
        thought = Thought(
            text=_TEXT_EXAMPLE,
            title=_TITLE_EXAMPLE,
            summary=_SUMMARY_EXAMPLE,
            embeddings=[],
            categories=[]
        )
        thought = self.agent._categories_extractor(thought)
        assert isinstance(thought.get('categories'), List)
        assert isinstance(thought.get('categories')[0], Category)

    def test__agent_should_interpret_the_thought(self):
        thought = Thought(
            text=_TEXT_EXAMPLE,
            title='',
            summary='',
            embeddings=[],
            categories=[]
        )

        interpreted_thought = self.agent.invoke(thought)
        summary = interpreted_thought.summary
        title = interpreted_thought.title
        categories = interpreted_thought.categories

        assert isinstance(summary, str)
        assert len(summary) >= 55

        assert isinstance(title, str)
        assert len(title) >= 25

        assert isinstance(categories, List)
        assert isinstance(categories[0], Category)
