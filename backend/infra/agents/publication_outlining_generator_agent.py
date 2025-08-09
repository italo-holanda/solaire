import os
import logging

from typing import List, Optional, Union
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from backend.core.thought.domain.entities.thought import Thought
from backend.core.publication.domain.services.publication_outlining_generator import PublicationOutliningGeneratorInterface


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
    ## Task
    You are an AI agent specialized in **generating structured text outlines** for 
    long-form content. Your goal is to create a **linear and logical outline** for a 
    totally new cohesive text that addresses the provided topics, following a given 
    tone and approach guide.

    ### Input
    You will receive:
    - A list of **distinct topics or concepts** to be covered in the final text.
    - A **manual** that defines the **tone of voice**, **communication style**, and 
    **guidelines** for how the text should connect and treat the topics.

    > Disclaimer: the guideline is created by a human user. You must follow it carefully
    as long as it does not contradict the main instructions defined in this prompt.
   
    > Disclaimer: do not use any external sources or information beyond the content 
    provided in the topics and the manual. Your output must rely solely on the input 
    data.

    ### Your output
    You must:
    - Generate a single, **coherent outline** for a text that incorporates all the 
    provided topics.
    - Output only a list of strings representing **sections or key points** in the 
    order they should appear in the final text.
    - Do not include the full text — only the outline.

    ### Output format
    Return a list of strings in the following format:
    ```python
    [
    "Section 1 title or idea",
    "Section 2 title or idea",
    ...
    "Final section title or idea"
    ]
    ```

    #### Structural requirements
    - The text must have a clear beginning (introduction), middle (development of 
    arguments or narrative), and end (conclusion or final reflection).
    - The structure should support one central thesis or main idea, and all sections
    must contribute to the development or reinforcement of that thesis.

    Each item should represent a **distinct segment** of the imagined text, showing the 
    logical development of the argument or narrative.

    ### OBS
    * Ensure the outline reflects the tone and direction described in the manual.
    * Use transitions and logic that connect the topics meaningfully.
    * Be imaginative and strategic — this outline will guide the writing of a 
    full article or essay.
"""


class AgentResponse(BaseModel):
    outlining: list[str] = Field(description="The list of outlining topics")


class PublicationOutliningGeneratorAgent(PublicationOutliningGeneratorInterface):
    """
    PublicationOutliningGeneratorAgent
    ---
    The `PublicationOutliningGeneratorAgent` is responsible for generating
    structured outlines for publications based on user thoughts and guidelines.
    """

    def __init__(self):
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", ""),
            base_url=os.getenv("OLLAMA_LOCAL_URL", ""),
        )

    def _generate_outline(
        self, thoughts: List[Thought], user_guideline: Optional[str]
    ) -> AgentResponse:
        messages: List[Union[SystemMessage, HumanMessage]] = []
        messages.append(SystemMessage(content=_AGENT_PROMPT))
        
        # Add user guideline if provided
        if user_guideline:
            messages.append(HumanMessage(content=user_guideline))
        
        # Add all thoughts as content
        for thought in thoughts:
            messages.append(HumanMessage(content=thought.text))

        response = self.llm.with_structured_output(
            AgentResponse
        ).invoke(messages)

        return response

    def invoke(
        self,
        thoughts: List[Thought],
        user_guideline: Optional[str],
    ) -> List[str]:
        thought_titles = [f"- {thought.title}" for thought in thoughts]
        logger.info(
            "Invoking PublicationOutliningGeneratorAgent workflow with thoughts: %s",
            ", ".join(thought_titles)
        )
        
        if user_guideline:
            logger.info("Using user guideline: %s", user_guideline[:100] + "..." if len(user_guideline) > 100 else user_guideline)
        
        result = self._generate_outline(thoughts, user_guideline)
        logger.info("Workflow result: %s", result)
        
        return result.outlining
