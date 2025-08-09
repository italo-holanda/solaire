from typing import List
import unittest

from backend.infra.agents.thought_topic_suggester_agent import (
    ThoughtTopicSuggesterAgent,
)
from backend.core.thought.domain.entities.thought import Thought
from backend.core.thought.domain.services.thought_topic_suggester import ThoughtTopicSuggesterOutput


_MAIN_THOUGHT_TEXT = """
I think unit testing in Python is one of those things
I used to brush off, but now I see it differently.
At first, it felt like extra work—writing tests for
something I just finished coding? Hmm, felt redundant.
But over time, I realized tests are more like a
conversation with your future self. They say, "Hey,
this is what I expected back then." So when things break—
and they will—those tests become your guide. It's not just
about catching bugs; it's about designing with clarity.
Like, if something's hard to test, maybe it's too complex.
That thought changed the way I code.
"""

_SIMILAR_THOUGHT_1_TEXT = """
Software architecture is fascinating. The way we structure
our code can make or break a project. Clean architecture
principles help us create maintainable systems that can
evolve over time. It's not just about making it work now,
but about making it work tomorrow and next year.
"""

_SIMILAR_THOUGHT_2_TEXT = """
Design patterns in programming are like recipes for solving
common problems. They provide proven solutions that have
been tested and refined over time. Learning these patterns
helps you write better code and communicate more effectively
with other developers.
"""

_SIMILAR_THOUGHT_3_TEXT = """
Continuous integration and deployment have revolutionized how we deliver software.
The idea of automating the build, test, and deployment process seemed overwhelming
at first, but now I can't imagine working without it. It's not just about speed;
it's about confidence. Every commit triggers a cascade of automated checks that
validate our code quality, run tests, and ensure everything works together.
This safety net allows us to move fast without breaking things, and it catches
issues early before they become expensive problems.
"""

_SIMILAR_THOUGHT_4_TEXT = """
Code reviews are one of the most powerful tools for improving code quality and
team collaboration. When done right, they're not about criticism but about
collective ownership of the codebase. I've learned that the best reviews focus
on the code, not the person, and ask questions rather than make demands.
They help spread knowledge across the team and catch issues that automated
tests might miss. The key is creating a culture where feedback is welcomed
and constructive.
"""


class TestThoughtTopicSuggesterAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ThoughtTopicSuggesterAgent()

    def make_thought(self, text: str, title: str = "Test Thought") -> Thought:
        return Thought(text=text, title=title, summary="", embeddings=[], categories=[])

    def test_agent_instantiates(self):
        self.assertIsInstance(self.agent, ThoughtTopicSuggesterAgent)

    def test__topic_suggestioner_should_return_structured_response(self):
        main_thought = self.make_thought(_MAIN_THOUGHT_TEXT, "Unit Testing")
        similar_thoughts = [
            self.make_thought(_SIMILAR_THOUGHT_1_TEXT, "Software Architecture"),
            self.make_thought(_SIMILAR_THOUGHT_2_TEXT, "Design Patterns"),
        ]

        result = self.agent._topic_suggestioner(main_thought, similar_thoughts)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "suggested_topics"))
        self.assertIsInstance(result.suggested_topics, list)
        self.assertGreater(len(result.suggested_topics), 0)

    def test__topic_suggestioner_should_limit_similar_thoughts_to_four(self):
        main_thought = self.make_thought(_MAIN_THOUGHT_TEXT)
        similar_thoughts = [
            self.make_thought(_SIMILAR_THOUGHT_1_TEXT),
            self.make_thought(_SIMILAR_THOUGHT_2_TEXT),
            self.make_thought(_SIMILAR_THOUGHT_3_TEXT),
            self.make_thought(_SIMILAR_THOUGHT_4_TEXT),
        ]

        result = self.agent._topic_suggestioner(main_thought, similar_thoughts)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "suggested_topics"))
        self.assertIsInstance(result.suggested_topics, list)

    def test__topic_suggestioner_should_handle_empty_similar_thoughts(self):
        main_thought = self.make_thought(_MAIN_THOUGHT_TEXT)
        similar_thoughts = []

        result = self.agent._topic_suggestioner(main_thought, similar_thoughts)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "suggested_topics"))
        self.assertIsInstance(result.suggested_topics, list)

    def test_invoke_should_return_ThoughtTopicSuggesterOutput_with_suggested_topics(self):
        main_thought = self.make_thought(_MAIN_THOUGHT_TEXT, "Unit Testing")
        similar_thoughts = [
            self.make_thought(_SIMILAR_THOUGHT_1_TEXT, "Architecture"),
            self.make_thought(_SIMILAR_THOUGHT_2_TEXT, "Design Patterns"),
        ]

        result = self.agent.invoke(main_thought, similar_thoughts)

        print(result)

        self.assertIsInstance(result, ThoughtTopicSuggesterOutput)
        self.assertIsInstance(result.suggested_topics, list)
        self.assertGreater(len(result.suggested_topics), 0)

    def test_invoke_should_handle_single_similar_thought(self):
        main_thought = self.make_thought(_MAIN_THOUGHT_TEXT)
        similar_thoughts = [self.make_thought(_SIMILAR_THOUGHT_1_TEXT)]

        result = self.agent.invoke(main_thought, similar_thoughts)

        self.assertIsInstance(result, ThoughtTopicSuggesterOutput)
        self.assertIsInstance(result.suggested_topics, list)

    def test_invoke_should_handle_empty_similar_thoughts(self):
        main_thought = self.make_thought(_MAIN_THOUGHT_TEXT)
        similar_thoughts = []

        result = self.agent.invoke(main_thought, similar_thoughts)

        self.assertIsInstance(result, ThoughtTopicSuggesterOutput)
        self.assertIsInstance(result.suggested_topics, list)

    def test_agent_has_required_methods(self):
        self.assertTrue(hasattr(self.agent, "_topic_suggestioner"))
        self.assertTrue(hasattr(self.agent, "invoke"))
        self.assertTrue(callable(self.agent._topic_suggestioner))
        self.assertTrue(callable(self.agent.invoke))

    def test_agent_has_llm_attribute(self):
        self.assertTrue(hasattr(self.agent, "llm"))
        self.assertIsNotNone(self.agent.llm)
