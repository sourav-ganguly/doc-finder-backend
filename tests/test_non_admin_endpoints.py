import os
import unittest
from datetime import date, datetime, timezone
from unittest.mock import patch

from fastapi.testclient import TestClient


os.environ.setdefault("DATABASE_URL", "sqlite:///./test_api.db")

from app import database as app_database

with patch.object(app_database.Base.metadata, "create_all", return_value=None):
    from app.main import app


class TestNonAdminEndpoints(unittest.TestCase):
    def setUp(self):
        self.mock_doctors = [
            {
                "id": 1,
                "name": "Dr. Example",
                "title": "Consultant",
                "speciality": "General Medicine",
                "educational_degree": "MBBS",
                "description": "Test profile",
                "location": "Dhaka",
                "data_source": "unit-test",
                "data_scrapped_at": date(2026, 1, 1),
                "clinics": ["Clinic A"],
                "chambers": ["Chamber A"],
            }
        ]
        self.mock_user = {
            "id": 1,
            "email": "user@example.com",
            "username": "user1",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        self.patchers = [
            patch(
                "app.api.doctors.router.service.get_doctors",
                return_value=self.mock_doctors,
            ),
            patch(
                "app.api.doctors.router.service.create_doctor",
                return_value=self.mock_doctors[0],
            ),
            patch(
                "app.api.cron.router.doctors_service.get_doctors",
                return_value=self.mock_doctors,
            ),
            patch(
                "app.api.auth.router.service.create_user",
                return_value=self.mock_user,
            ),
            patch(
                "app.api.auth.router.service.authenticate_user",
                return_value=type("AuthUser", (), {"email": "user@example.com"})(),
            ),
            patch(
                "app.api.auth.router.service.create_access_token",
                return_value="test-access-token",
            ),
        ]
        for patcher in self.patchers:
            patcher.start()
        self.client = TestClient(app)

    def tearDown(self):
        for patcher in reversed(self.patchers):
            patcher.stop()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_doctors_get(self):
        response = self.client.get("/doctors/")
        self.assertEqual(response.status_code, 200)

    def test_doctors_post(self):
        payload = {
            "name": "Dr. Example",
            "speciality": "General Medicine",
        }
        response = self.client.post("/doctors/", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_auth_register(self):
        payload = {
            "email": "user@example.com",
            "username": "user1",
            "password": "secret123",
        }
        response = self.client.post("/auth/register", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_auth_login(self):
        response = self.client.post(
            "/auth/login",
            data={"username": "user@example.com", "password": "secret123"},
        )
        self.assertEqual(response.status_code, 200)

    def test_cron_ping_doctors(self):
        response = self.client.get("/api/cron/ping-doctors", params={"type": "general"})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
