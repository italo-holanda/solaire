import pytest
from backend.infra.agents.publication_content_generator_agent import PublicationContentGeneratorAgent
from backend.core.thought.domain.entities.thought import Thought
from backend.core.category.domain.entities.category import Category

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

_OUTLINING = [
    "Introduction: Why software craftsmanship matters",
    "The role of testing in sustainable development",
    "Architectural thinking for long-term success",
    "Patterns and practices for effective teams",
    "Conclusion: Continuous improvement as a mindset"
]


@pytest.fixture
def agent():
    return PublicationContentGeneratorAgent()


def make_thought(text: str, title: str = "Test Thought") -> Thought:
    return Thought(
        text=text,
        title=title,
        summary="",
        embeddings=[],
        categories=[]
    )


def test_agent_instantiates(agent):
    assert isinstance(agent, PublicationContentGeneratorAgent)


def test_agent_has_required_methods(agent):
    assert hasattr(agent, "_generate_content")
    assert hasattr(agent, "invoke")
    assert callable(agent._generate_content)
    assert callable(agent.invoke)


def test_agent_has_llm_attribute(agent):
    assert hasattr(agent, "llm")
    assert agent.llm is not None


def test__generate_content_should_return_structured_response(agent):
    thoughts = [
        make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
        make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
    ]
    result = agent._generate_content(thoughts, _USER_GUIDELINE, _OUTLINING)
    assert result is not None
    assert hasattr(result, "outlining")
    assert isinstance(result.outlining, list)
    assert len(result.outlining) > 0


def test__generate_content_should_handle_empty_guideline(agent):
    thoughts = [
        make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
        make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
    ]
    result = agent._generate_content(thoughts, None, _OUTLINING)
    assert result is not None
    assert hasattr(result, "outlining")
    assert isinstance(result.outlining, list)
    assert len(result.outlining) > 0


def test__generate_content_should_handle_single_thought(agent):
    thoughts = [make_thought(_THOUGHT_1_TEXT, "Unit Testing")]
    result = agent._generate_content(thoughts, _USER_GUIDELINE, _OUTLINING)
    assert result is not None
    assert hasattr(result, "outlining")
    assert isinstance(result.outlining, list)
    assert len(result.outlining) > 0


def test__generate_content_should_handle_multiple_thoughts(agent):
    thoughts = [
        make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
        make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
        make_thought(_THOUGHT_3_TEXT, "Design Patterns"),
    ]
    result = agent._generate_content(thoughts, _USER_GUIDELINE, _OUTLINING)
    assert result is not None
    assert hasattr(result, "outlining")
    assert isinstance(result.outlining, list)
    assert len(result.outlining) > 0


def test_invoke_should_return_list_of_strings(agent):
    thoughts = [
        make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
        make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
    ]
    result = agent.invoke(thoughts, _USER_GUIDELINE, _OUTLINING)
    assert isinstance(result, list)
    assert len(result) > 0
    for item in result:
        assert isinstance(item, str)
        assert len(item) > 0


def test_invoke_should_handle_empty_guideline(agent):
    thoughts = [
        make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
        make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
    ]
    result = agent.invoke(thoughts, None, _OUTLINING)
    assert isinstance(result, list)
    assert len(result) > 0
    for item in result:
        assert isinstance(item, str)
        assert len(item) > 0


def test_invoke_should_handle_single_thought(agent):
    thoughts = [make_thought(_THOUGHT_1_TEXT, "Unit Testing")]
    result = agent.invoke(thoughts, _USER_GUIDELINE, _OUTLINING)
    assert isinstance(result, list)
    assert len(result) > 0
    for item in result:
        assert isinstance(item, str)
        assert len(item) > 0


def test_invoke_should_handle_multiple_thoughts(agent):
    thoughts = [
        make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
        make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
        make_thought(_THOUGHT_3_TEXT, "Design Patterns"),
    ]
    result = agent.invoke(thoughts, _USER_GUIDELINE, _OUTLINING)
    assert isinstance(result, list)
    assert len(result) > 0
    for item in result:
        assert isinstance(item, str)
        assert len(item) > 0


def test_content_items_should_be_meaningful(agent):
    thoughts = [
        make_thought(_THOUGHT_1_TEXT, "Unit Testing"),
        make_thought(_THOUGHT_2_TEXT, "Software Architecture"),
    ]
    result = agent.invoke(thoughts, _USER_GUIDELINE, _OUTLINING)
    for item in result:
        assert isinstance(item, str)
        assert len(item) > 5
        assert item.strip() != ""


def test_agent_implements_interface():
    from backend.core.publication.domain.services.publication_content_generator import PublicationContentGeneratorInterface
    assert issubclass(PublicationContentGeneratorAgent,
                      PublicationContentGeneratorInterface)
