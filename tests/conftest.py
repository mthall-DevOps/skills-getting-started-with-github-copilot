import sys
import os
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient

# Add src to Python path so we can import the app module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app, activities as initial_activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities state before and after each test."""
    # Store the initial state
    original_activities = deepcopy(initial_activities)
    # Reset to initial state
    app.activities = deepcopy(original_activities)
    yield
    # Restore after test
    app.activities = original_activities


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI app."""
    return TestClient(app)