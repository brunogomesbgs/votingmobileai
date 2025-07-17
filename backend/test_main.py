import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer
from main import app
from models import Feature, Vote
import json

# Test client
client = TestClient(app)


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module", autouse=True)
async def initialize_tests():
    # Initialize test database
    initializer(["models"], db_url="sqlite://:memory:")
    yield
    finalizer()


class TestFeatureAPI:

    def test_create_feature_success(self):
        """Test successful feature creation"""
        feature_data = {
            "title": "Test Feature",
            "description": "Test Description",
            "created_by": "test_user"
        }

        response = client.post("/features", json=feature_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Feature"
        assert data["description"] == "Test Description"
        assert data["created_by"] == "test_user"
        assert data["vote_count"] == 0
        assert "id" in data
        assert "created_at" in data

    def test_create_feature_empty_title(self):
        """Test feature creation with empty title"""
        feature_data = {
            "title": "",
            "description": "Test Description",
            "created_by": "test_user"
        }

        response = client.post("/features", json=feature_data)

        assert response.status_code == 400
        assert "Title cannot be empty" in response.json()["detail"]

    def test_create_feature_empty_description(self):
        """Test feature creation with empty description"""
        feature_data = {
            "title": "Test Feature",
            "description": "",
            "created_by": "test_user"
        }

        response = client.post("/features", json=feature_data)

        assert response.status_code == 400
        assert "Description cannot be empty" in response.json()["detail"]

    def test_get_features(self):
        """Test getting all features"""
        # Create a feature first
        feature_data = {
            "title": "Test Feature 2",
            "description": "Test Description 2",
            "created_by": "test_user2"
        }
        client.post("/features", json=feature_data)

        response = client.get("/features")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_feature_by_id(self):
        """Test getting a specific feature"""
        # Create a feature first
        feature_data = {
            "title": "Test Feature 3",
            "description": "Test Description 3",
            "created_by": "test_user3"
        }
        create_response = client.post("/features", json=feature_data)
        feature_id = create_response.json()["id"]

        response = client.get(f"/features/{feature_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == feature_id
        assert data["title"] == "Test Feature 3"

    def test_get_nonexistent_feature(self):
        """Test getting a nonexistent feature"""
        response = client.get("/features/99999")

        assert response.status_code == 404
        assert "Feature not found" in response.json()["detail"]


class TestVoteAPI:

    def test_vote_feature_success(self):
        """Test successful vote creation"""
        # Create a feature first
        feature_data = {
            "title": "Votable Feature",
            "description": "Feature to vote on",
            "created_by": "creator"
        }
        feature_response = client.post("/features", json=feature_data)
        feature_id = feature_response.json()["id"]

        # Vote for the feature
        vote_data = {
            "feature_id": feature_id,
            "voter_id": "voter1"
        }

        response = client.post("/votes", json=vote_data)

        assert response.status_code == 201
        data = response.json()
        assert data["feature_id"] == feature_id
        assert data["voter_id"] == "voter1"
        assert "id" in data
        assert "created_at" in data

        # Check if vote count increased
        feature_response = client.get(f"/features/{feature_id}")
        assert feature_response.json()["vote_count"] == 1

    def test_vote_nonexistent_feature(self):
        """Test voting for a nonexistent feature"""
        vote_data = {
            "feature_id": 99999,
            "voter_id": "voter1"
        }

        response = client.post("/votes", json=vote_data)

        assert response.status_code == 404
        assert "Feature not found" in response.json()["detail"]

    def test_vote_empty_voter_id(self):
        """Test voting with empty voter_id"""
        # Create a feature first
        feature_data = {
            "title": "Another Votable Feature",
            "description": "Feature to vote on",
            "created_by": "creator"
        }
        feature_response = client.post("/features", json=feature_data)
        feature_id = feature_response.json()["id"]

        vote_data = {
            "feature_id": feature_id,
            "voter_id": ""
        }

        response = client.post("/votes", json=vote_data)

        assert response.status_code == 400
        assert "Voter ID cannot be empty" in response.json()["detail"]

    def test_duplicate_vote(self):
        """Test duplicate vote prevention"""
        # Create a feature first
        feature_data = {
            "title": "Duplicate Vote Feature",
            "description": "Feature to test duplicate votes",
            "created_by": "creator"
        }
        feature_response = client.post("/features", json=feature_data)
        feature_id = feature_response.json()["id"]

        # First vote
        vote_data = {
            "feature_id": feature_id,
            "voter_id": "duplicate_voter"
        }

        first_response = client.post("/votes", json=vote_data)
        assert first_response.status_code == 201

        # Second vote (should fail)
        second_response = client.post("/votes", json=vote_data)
        assert second_response.status_code == 409
        assert "already voted" in second_response.json()["detail"]


class TestHealthCheck:

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}