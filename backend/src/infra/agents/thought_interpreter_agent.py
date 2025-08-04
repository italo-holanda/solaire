import os
import logging

from typing import Dict, List, Literal, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

from src.core.category.domain.entities.category import Category
from src.core.thought.domain.entities.thought import Thought
from src.core.thought.domain.services.thought_interpreter import ThoughtInterpreterInterface, ThoughtInterpreterOutput


LOG_LEVEL = os.getenv('AGENT_LOG_LEVEL', 'INFO').upper()
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class SummaryOutput(BaseModel):
    summary: str = Field(
        default=None,
        description="A plain string containing the summary of the thought."
    )


class TitleOutput(BaseModel):
    title: str = Field(
        default=None,
        description="A plain string containing the title of the thought."
    )


class CategoriesOutput(BaseModel):
    categories: List[str] = Field(
        default=None,
        description="An array of category names (strings)"
    )


class ThoughtInterpreterAgent(ThoughtInterpreterInterface):
    """
    ThoughtInterpreterAgent
    ---
    The `ThoughtInterpreterAgent` is responsible for reflecting
    on human thoughts and generating a comment (summary) about them. 
    It also generates a concise title, extracts topic categories.
    """

    def __init__(self):
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", ""),
            base_url=os.getenv("OLLAMA_LOCAL_URL", ""),
        )
        self.graph = self._setup_graph()

    def _setup_graph(self):
        builder = StateGraph(Thought)
        builder.add_node('summary_generator', self._summary_generator)
        builder.add_node('title_generator', self._title_generator)
        builder.add_node('categories_extractor', self._categories_extractor)

        builder.set_entry_point('summary_generator')
        builder.add_edge("summary_generator", "title_generator")
        builder.add_edge("title_generator", "categories_extractor")
        builder.add_edge("categories_extractor", END)

        return builder.compile()

    def _summary_generator(self, thought: Thought) -> Thought:
        logger.debug('Calling `_summary_generator` with thought: %s', thought)
        summary_generation_prompt = """
            You will receive a block of thought written by a user. 
            Your task is to analyze the content and produce a brief, 
            friendly summary in plain text, without any formatting. 
            Return your answer as a JSON object with a single key "summary".
            Example: {"summary": "Your summary here"}
        """
        output = self.llm.with_structured_output(SummaryOutput).invoke(
            [
                SystemMessage(content=summary_generation_prompt),
                HumanMessage(content=thought.text)
            ]
        )
        logger.debug(f'Summary generated: "%s"', output.summary)
        return {'summary': output.summary}

    def _title_generator(self, thought: Thought) -> Thought:
        logger.debug('Calling `_title_generator` with thought: %s', thought)
        title_generation_prompt = """
            You are an assistant designed to analyze thought entries 
            written by the user. Carefully read the provided text and
            identify the main ideas and key topics discussed. Then, 
            generate a concise and meaningful title that clearly 
            communicates the overall intention or theme of the text.
            The title should be short, relevant, and reflective of the 
            core message in the entry.
        """
        output = self.llm.with_structured_output(TitleOutput).invoke(
            [
                SystemMessage(content=title_generation_prompt),
                HumanMessage(content=thought.text)
            ]
        )
        logger.debug(f'Title generated: "%s"', output.title)
        return {'title': output.title}

    def _categories_extractor(self, thought: Thought) -> Thought:
        logger.debug(
            'Calling `_categories_extractor` with thought: %s', thought
        )
        categories_extraction_prompt = """
            Analyze the following block of text written by the user. 
            Identify the main topics discussed and return a list of 
            subject categories in the form of an array. Focus on the
            key themes and concepts conveyed throughout the text. 
            Avoid unnecessary details and only include clear, 
            distinct categories.
        """
        output = self.llm.with_structured_output(CategoriesOutput).invoke(
            [
                SystemMessage(content=categories_extraction_prompt),
                HumanMessage(content=thought.text)
            ]
        )
        categories_entities = []
        for category_name in output.categories:
            categories_entities.append(
                Category(name=category_name)
            )
        logger.debug('Categories extracted: %s', categories_entities)
        return {'categories': categories_entities}

    def invoke(self, thought: Thought) -> Dict:
        logger.info(
            'Invoking ThoughtInterpreterAgent workflow with thought: %s', thought
        )
        result = self.graph.invoke(
            Thought(**thought.model_dump(), route=None)
        )
        logger.info('Workflow result: %s', result)
        return ThoughtInterpreterOutput(**result)
