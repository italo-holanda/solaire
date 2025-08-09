import os
import pytest
import time
from faker import Faker

from backend.core.thought.domain.entities.thought import Thought
from backend.infra.databases.vectorial.thought_vector_store import ThoughtVectorStore
from backend.infra.databases.vectorial.weaviate_db import WeaviateDB


faker = Faker()


class TestThoughtVectorStore:
    """Integration tests for ThoughtVectorStore using real Weaviate and Ollama connections"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures with real connections"""
        self.original_env = os.environ.copy()
        self.vector_store = ThoughtVectorStore()
        self.weaviate_db = WeaviateDB()
        time.sleep(1)

    def test__cleanup_schema(self):
        self.weaviate_db._delete_thought_schema()

    def test__should_connect_with_db(self):
        """Test initialization with real Weaviate connection"""
        assert hasattr(self.vector_store, 'db')
        assert hasattr(self.vector_store, 'vector_provider')
        assert self.vector_store.vector_provider == 'ollama'

    def test__should_create_new_thought_index(self):
        """Test .create_index() method"""

        thought = Thought(
            title="My weekend in Estonia",
            text="""
                Tallinn's Old Town felt like stepping into a fairytale—cobbled streets,
                medieval towers, and cozy cafés. Took a ferry to Saaremaa island, where
                the peaceful nature and windmills totally reset my mind. Tried smoked 
                fish and local beer—both amazing. Locals were friendly, though reserved.
                Loved the mix of Nordic calm and Eastern European charm. Would go back
                in a heartbeat. Estonia's small, but it packs a surprising punch.
            """,
            summary="""
                Weekend in Estonia: medieval Tallinn, peaceful Saaremaa, great food, 
                friendly vibes, unforgettable trip.
            """,
            categories=[],
            embeddings=[]
        )
        self.vector_store.create_index(thought)

    def test__should_search_by_thought_similarity(self):
        """Test .search_similar()"""

        thought = Thought(
            title="Exploring Estonia's Quiet Corners",
            text="""
                Spent a few calm days in Tartu—less touristy than Tallinn but full of charm. 
                The town square, street art, and university vibe gave it a youthful energy. 
                Wandered through forest trails in Lahemaa National Park—misty, serene, and 
                completely peaceful. Stumbled on a tiny seaside village where I tried freshly 
                baked rye bread with smoked herring. Estonians kept to themselves, but were 
                kind when approached. Loved the contrast of quiet nature and clever urban spaces. 
                Estonia feels understated, but deeply rewarding.
            """,
            summary="""
                Trip through Estonia: Tartu's culture, Lahemaa's forests, seaside quiet, 
                subtle beauty, gentle pace, and good food.
            """,
            categories=[],
            embeddings=[]
        )
        search_result = self.vector_store.search_similar(thought)
        assert len(search_result) == 1

    def test__should_search_by_text_similarity(self):
        """Test .search_similar_by_text()"""

        thought_text = """
            Spent a few calm days in Tartu—less touristy than Tallinn but full of charm. 
            The town square, street art, and university vibe gave it a youthful energy. 
            Wandered through forest trails in Lahemaa National Park—misty, serene, and 
            completely peaceful. Stumbled on a tiny seaside village where I tried freshly 
            baked rye bread with smoked herring. Estonians kept to themselves, but were 
            kind when approached. Loved the contrast of quiet nature and clever urban spaces. 
            Estonia feels understated, but deeply rewarding.
        """

        search_result = self.vector_store.search_similar_by_text(thought_text)
        assert len(search_result) == 1

    def test__should_delete_index_by_thought_id(self):
        """Test .delete_index()"""

        thought = Thought(
            title="My weekend in Estonia",
            text="""
                Tallinn's Old Town felt like stepping into a fairytale—cobbled streets,
                medieval towers, and cozy cafés. Took a ferry to Saaremaa island, where
                the peaceful nature and windmills totally reset my mind. Tried smoked 
                fish and local beer—both amazing. Locals were friendly, though reserved.
                Loved the mix of Nordic calm and Eastern European charm. Would go back
                in a heartbeat. Estonia's small, but it packs a surprising punch.
            """,
            summary="""
                Weekend in Estonia: medieval Tallinn, peaceful Saaremaa, great food, 
                friendly vibes, unforgettable trip.
            """,
            categories=[],
            embeddings=[]
        )

        self.vector_store.create_index(thought)
        search_result = self.vector_store.search_similar(thought)
        assert len(search_result) == 2

        self.vector_store.delete_index(thought)
        search_result = self.vector_store.search_similar(thought)
        assert len(search_result) == 1
