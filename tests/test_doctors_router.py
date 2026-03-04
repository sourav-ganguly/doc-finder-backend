import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_api.db")

from app.api.doctors import schemas
from app.api.doctors.router import router
from app.database import get_db


@pytest.fixture
def client_and_db():
    app = FastAPI()
    app.include_router(router, prefix="/doctors")

    db = MagicMock(name="db_session")

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client, db


def test_get_doctors_without_search(client_and_db):
    client, db = client_and_db
    doctors = [{"id": 1, "name": "Dr. A", "speciality": "Cardiology"}]

    with patch(
        "app.api.doctors.router.service.get_doctors",
        return_value=doctors,
    ) as get_doctors_mock, patch(
        "app.api.doctors.router.match_specialization"
    ) as match_mock:
        response = client.get("/doctors/", params={"skip": 2, "limit": 5})

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Dr. A",
            "title": None,
            "speciality": "Cardiology",
            "educational_degree": None,
            "description": None,
            "location": None,
            "data_source": None,
            "data_scrapped_at": None,
            "clinics": [],
            "chambers": [],
        }
    ]
    match_mock.assert_not_called()
    get_doctors_mock.assert_called_once_with(
        db=db, skip=2, limit=5, specializations=None
    )


def test_get_doctors_with_search_maps_specializations(client_and_db):
    client, db = client_and_db

    with patch(
        "app.api.doctors.router.service.get_doctors",
        return_value=[],
    ) as get_doctors_mock, patch(
        "app.api.doctors.router.match_specialization",
        return_value="Cardiology; Neurology",
    ) as match_mock:
        response = client.get("/doctors/", params={"search": "headache"})

    assert response.status_code == 200
    assert response.json() == []
    match_mock.assert_called_once_with("headache")
    get_doctors_mock.assert_called_once_with(
        db=db, skip=0, limit=100, specializations=["Cardiology", "Neurology"]
    )


def test_create_doctor_calls_service_with_schema(client_and_db):
    client, db = client_and_db
    created = {"id": 7, "name": "Dr. New", "speciality": "Dermatology"}

    with patch(
        "app.api.doctors.router.service.create_doctor",
        return_value=created,
    ) as create_mock:
        response = client.post(
            "/doctors/",
            json={"name": "Dr. New", "speciality": "Dermatology"},
        )

    assert response.status_code == 201
    assert response.json()["id"] == 7
    assert response.json()["name"] == "Dr. New"
    assert response.json()["speciality"] == "Dermatology"

    create_mock.assert_called_once()
    kwargs = create_mock.call_args.kwargs
    assert kwargs["db"] is db
    assert isinstance(kwargs["doctor"], schemas.DoctorCreate)
    assert kwargs["doctor"].name == "Dr. New"
    assert kwargs["doctor"].speciality == "Dermatology"
