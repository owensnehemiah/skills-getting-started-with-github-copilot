from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_success():
    activity_name = "Chess Club"
    email = "newstudent@example.com"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    activity_name = "Gym Class"
    email = "missingstudent@example.com"

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
