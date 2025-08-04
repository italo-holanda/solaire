import os
import logging

from typing import List, Union
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from src.core.thought.domain.entities.thought import Thought
from src.core.thought.domain.services.thought_topic_suggester import ThoughtTopicSuggesterInterface, ThoughtTopicSuggesterOutput


LOG_LEVEL = os.getenv("AGENT_LOG_LEVEL", "INFO").upper()
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

_AGENT_PROMPT = """
    You will receive up to five different blocks of thoughts written by the user. Your task 
    is to analyze these blocks carefully, identify the main topics discussed in each of them, 
    and then return a list of topics or ideas that could elevate these thoughts to a new 
    level of depth, innovation, or insight.
    Focus on extracting and synthesizing key themes, and propose potential directions for 
    expansion, refinement, or transformation.
    Return only a simple array of strings, each representing one of the suggested topics 
    for elevating the user’s thinking. Do not include explanations or summaries.
"""


class AgentResponse(BaseModel):
    suggested_topics: list[str] = Field(description="Suggested topics")


class ThoughtTopicSuggesterAgent(ThoughtTopicSuggesterInterface):
    """
    ThoughtTopicSuggesterAgent
    ---
    The `ThoughtInterpreterAgent` is responsible for suggesting
    new topics based on the given user thoughts.
    """

    def __init__(self):
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", ""),
            base_url=os.getenv("OLLAMA_LOCAL_URL", ""),
        )

    def _topic_suggestioner(
        self, main_thought: Thought, similar_thoughts: List[Thought]
    ) -> AgentResponse:

        messages: List[Union[SystemMessage, HumanMessage]] = []
        messages = [SystemMessage(content=_AGENT_PROMPT)]
        messages.append(HumanMessage(content=main_thought.text))

        for thought in similar_thoughts[:4]:
            messages.append(HumanMessage(content=thought.text))

        response = self.llm.with_structured_output(
            AgentResponse
        ).invoke(messages)

        return response

    def invoke(self, main_thought: Thought, similar_thoughts: List[Thought]) -> ThoughtTopicSuggesterOutput:
        thought_titles = [f"- {main_thought.title}"] + [f"- {thought.title}" for thought in similar_thoughts]
        logger.info(
            "Invoking ThoughtTopicSuggesterAgent workflow with thoughts: %s",
            ", ".join(thought_titles)
        )
        result = self._topic_suggestioner(
            main_thought,
            similar_thoughts,
        )
        logger.info("Workflow result: %s", result)
        
        suggested_topics = result.suggested_topics
        return ThoughtTopicSuggesterOutput(
            suggested_topics=suggested_topics
        )
