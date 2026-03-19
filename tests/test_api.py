def test_get_activities_returns_activities(client):
    """Test that /activities endpoint returns the activities data."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_adds_participant_and_rejects_duplicate(client):
    """Test signing up a new participant and rejecting duplicates."""
    # Sign up a new participant
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]

    # Verify the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]

    # Try to sign up again - should fail
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up" in data["detail"]


def test_remove_participant(client):
    """Test removing an existing participant."""
    # Remove an existing participant
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Removed michael@mergington.edu from Chess Club" in data["message"]

    # Verify the participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "michael@mergington.edu" not in data["Chess Club"]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    """Test removing a participant who is not signed up returns 404."""
    response = client.delete("/activities/Chess%20Club/signup?email=nonexistent@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test signing up for a nonexistent activity returns 404."""
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_remove_from_nonexistent_activity_returns_404(client):
    """Test removing from a nonexistent activity returns 404."""
    response = client.delete("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]