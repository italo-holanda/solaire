import os
import logging

from typing import List, Optional, Union
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from backend.core.thought.domain.entities.thought import Thought
from backend.core.publication.domain.services.publication_content_generator import PublicationContentGeneratorInterface


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
You are an AI tasked with writing a cohesive, long-form publication based solely 
on a provided outline and style guideline. The text must follow the exact structure 
of the outlining list, adopt the tone and style of the guideline, and form a unified, 
thesis-driven piece with a clear introduction, development, and conclusion. 
VERY IMPORTANT: No external information is allowed. 
The final output should be a polished, human-like text in Markdown format, with smooth 
transitions and consistent tone throughout.
"""


class AgentResponse(BaseModel):
    outlining: list[str] = Field(description="The list of outlining topics")


class PublicationContentGeneratorAgent(PublicationContentGeneratorInterface):
    """
    PublicationOutliningGeneratorAgent
    ---
    The `PublicationOutliningGeneratorAgent` is responsible for generating
    Markdown Text for publications based on user thoughts and guidelines.
    """

    def __init__(self):
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", ""),
            base_url=os.getenv("OLLAMA_LOCAL_URL", ""),
        )

    def _generate_content(
        self, thoughts: List[Thought], user_guideline: Optional[str], outlining: List[str]
    ) -> AgentResponse:
        outlining_md = "\n".join([f"### {i+1}. {item}" for i, item in enumerate(outlining)])
        system_prompt = _AGENT_PROMPT + "\n\n# Outlining\n" + outlining_md
        messages: List[Union[SystemMessage, HumanMessage]] = []
        messages.append(SystemMessage(content=system_prompt))

        if user_guideline:
            messages.append(HumanMessage(content=user_guideline))

        if thoughts:
            combined_thoughts = "".join([
                f"## Thought {i+1}\n{thought.text.strip()}\n" for i, thought in enumerate(thoughts)
            ])
            messages.append(HumanMessage(content=combined_thoughts))

        response = self.llm.with_structured_output(
            AgentResponse
        ).invoke(messages)

        return response

    def invoke(
        self,
        thoughts: List[Thought],
        user_guideline: Optional[str],
        outlining: List[str]
    ) -> List[str]:
        thought_titles = [f"- {thought.title}" for thought in thoughts]
        logger.info(
            "Invoking PublicationOutliningGeneratorAgent workflow with thoughts: %s",
            ", ".join(thought_titles)
        )

        if user_guideline:
            logger.info("Using user guideline: %s", user_guideline[:100] + "..." if len(
                user_guideline) > 100 else user_guideline)

        result = self._generate_content(thoughts, user_guideline, outlining)
        logger.info("Workflow result: %s", result)

        return result.outlining
