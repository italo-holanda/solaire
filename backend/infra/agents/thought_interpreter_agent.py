import os

from typing import Dict, List, Literal, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

from backend.core.category.domain.entities.category import Category
from backend.core.thought.domain.entities.thought import Thought


AgentRoute = Literal[
    'summary_generator',
    'title_generator',
    'categories_extractor',
    'finish'
]


class AgentState(Thought):
    route: Optional[AgentRoute]


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


class ThoughtInterpreterAgent:
    """
    ThoughtInterpreterAgent
    ---
    The `ThoughtInterpreterAgent` is responsible for reflecting
    on human thoughts and generating a comment (summary) about them. 
    It also generates a concise title, extracts topic categories.
    """

    def __init__(self):
        self.llm = ChatOllama(model=os.getenv('OLLAMA_MODEL'))
        self.graph = self._setup_graph()

    def _setup_graph(self):
        builder = StateGraph(AgentState)
        builder.add_node('summary_generator', self._summary_generator)
        builder.add_node('title_generator', self._title_generator)
        builder.add_node('categories_extractor', self._categories_extractor)

        builder.set_entry_point('summary_generator')
        builder.add_edge("summary_generator", "title_generator")
        builder.add_edge("title_generator", "categories_extractor")
        builder.add_edge("categories_extractor", END)

        return builder.compile()

    def _summary_generator(self, thought: AgentState) -> AgentState:
        summary_generation_prompt = """
            You will receive a block of thought written by a user. 
            Your task is to analyze the content and produce a brief, 
            friendly summary in plain text, without any formatting. 
            Highlight the key topics and noteworthy elements present 
            in the user's writing. The summary should be concise, easy
            to read, and should gently inform the user of the main points
            or emotions expressed in their text, using a warm and under-
            standing tone.
        """
        output = self.llm.with_structured_output(SummaryOutput).invoke(
            [
                SystemMessage(content=summary_generation_prompt),
                HumanMessage(content=thought.text)
            ]
        )
        return {'summary': output.summary}

    def _title_generator(self, thought: AgentState) -> AgentState:
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
        return {'title': output.title}

    def _categories_extractor(self, thought: AgentState) -> AgentState:
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
        return {'categories': categories_entities}

    def invoke(self, thought: Thought) -> Dict:
        return self.graph.invoke(
            AgentState(**thought.model_dump(), route=None)
        )
