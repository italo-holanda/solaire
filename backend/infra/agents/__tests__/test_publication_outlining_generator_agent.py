import unittest

from backend.infra.agents.publication_outlining_generator_agent import PublicationOutliningGeneratorAgent
from backend.core.thought.domain.entities.thought import Thought


_THOUGHT_1_TEXT = """
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

_THOUGHT_2_TEXT = """
Software architecture is fascinating. The way we structure
our code can make or break a project. Clean architecture
principles help us create maintainable systems that can
evolve over time. It's not just about making it work now,
but about making it work tomorrow and next year.
"""

_THOUGHT_3_TEXT = """
Design patterns in programming are like recipes for solving
common problems. They provide proven solutions that have
been tested and refined over time. Learning these patterns
helps you write better code and communicate more effectively
with other developers.
"""

_USER_GUIDELINE = """
Write in a conversational, educational tone that connects with software developers.
Focus on practical insights and real-world applications. Use examples and analogies
to make complex concepts accessible. The content should inspire readers to improve
their development practices.
"""


class TestPublicationOutliningGeneratorAgent(unittest.TestCase):
    def setUp(self):
        self.agent = PublicationOutliningGeneratorAgent()

    def make_thought(self, text: str, title: str = "Test Thought") -> Thought:
        return Thought(
            text=text,
            title=title,
            summary="",
            embeddings=[],
            categories=[]
        )

    def test_agent_instantiates(self):
        self.assertIsInstance(self.agent, PublicationOutliningGeneratorAgent)

    def test_agent_has_required_methods(self):
        self.assertTrue(hasattr(self.agent, "_generate_outline"))
        self.assertTrue(hasattr(self.agent, "invoke"))
        self.assertTrue(callable(self.agent._generate_outline))
        self.assertTrue(callable(self.agent.invoke))

    def test_agent_has_llm_attribute(self):
        self.assertTrue(hasattr(self.agent, "llm"))
        self.assertIsNotNone(self.agent.llm)

    def test__generate_outline_should_return_structured_response(self):
        thoughts = [
            self.make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
            self.make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
        ]

        result = self.agent._generate_outline(thoughts, _USER_GUIDELINE)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "outlining"))
        self.assertIsInstance(result.outlining, list)
        self.assertGreater(len(result.outlining), 0)

    def test__generate_outline_should_handle_empty_guideline(self):
        thoughts = [
            self.make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
            self.make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
        ]

        result = self.agent._generate_outline(thoughts, None)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "outlining"))
        self.assertIsInstance(result.outlining, list)
        self.assertGreater(len(result.outlining), 0)

    def test__generate_outline_should_handle_single_thought(self):
        thoughts = [self.make_thought(_THOUGHT_1_TEXT, "Unit Testing")]

        result = self.agent._generate_outline(thoughts, _USER_GUIDELINE)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "outlining"))
        self.assertIsInstance(result.outlining, list)
        self.assertGreater(len(result.outlining), 0)

    def test__generate_outline_should_handle_multiple_thoughts(self):
        thoughts = [
            self.make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
            self.make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
            self.make_thought(_THOUGHT_3_TEXT, "Design Patterns"),
        ]

        result = self.agent._generate_outline(thoughts, _USER_GUIDELINE)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "outlining"))
        self.assertIsInstance(result.outlining, list)
        self.assertGreater(len(result.outlining), 0)

    def test_invoke_should_return_list_of_strings(self):
        thoughts = [
            self.make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
            self.make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
        ]

        result = self.agent.invoke(thoughts, _USER_GUIDELINE)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertIsInstance(item, str)
            self.assertGreater(len(item), 0)

    def test_invoke_should_handle_empty_guideline(self):
        thoughts = [
            self.make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
            self.make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
        ]

        result = self.agent.invoke(thoughts, None)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertIsInstance(item, str)
            self.assertGreater(len(item), 0)

    def test_invoke_should_handle_single_thought(self):
        thoughts = [self.make_thought(_THOUGHT_1_TEXT, "Unit Testing")]

        result = self.agent.invoke(thoughts, _USER_GUIDELINE)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertIsInstance(item, str)
            self.assertGreater(len(item), 0)

    def test_invoke_should_handle_multiple_thoughts(self):
        thoughts = [
            self.make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
            self.make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
            self.make_thought(_THOUGHT_3_TEXT, "Design Patterns"),
        ]

        result = self.agent.invoke(thoughts, _USER_GUIDELINE)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertIsInstance(item, str)
            self.assertGreater(len(item), 0)

    def test_outline_items_should_be_meaningful(self):
        thoughts = [
            self.make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
            self.make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
        ]

        result = self.agent.invoke(thoughts, _USER_GUIDELINE)

        for item in result:
            self.assertIsInstance(item, str)
            self.assertGreater(len(item), 5)
            self.assertNotEqual(item.strip(), "")

    def test_outline_should_have_logical_structure(self):
        thoughts = [
            self.make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
            self.make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
        ]

        result = self.agent.invoke(thoughts, _USER_GUIDELINE)

        self.assertGreaterEqual(len(result), 3)
        
        first_item = result[0].lower()
        last_item = result[-1].lower()
        
        self.assertTrue(
            any(keyword in first_item for keyword in ["intro", "beginning", "start", "overview"]),
            f"First item should indicate introduction: {first_item}"
        )
        
        self.assertTrue(
            any(keyword in last_item for keyword in ["conclusion", "ending", "final", "summary"]),
            f"Last item should indicate conclusion: {last_item}"
        )

    def test_agent_implements_interface(self):
        from backend.core.publication.domain.services.publication_outlining_generator import PublicationOutliningGeneratorInterface
        
        self.assertTrue(issubclass(PublicationOutliningGeneratorAgent, PublicationOutliningGeneratorInterface))
