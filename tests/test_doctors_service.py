import json
import os
import tempfile
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_api.db")

from app.api.doctors import models, schemas, service


def _mock_query_chain(all_result):
    query = MagicMock(name="query")
    query.filter.return_value = query
    query.order_by.return_value = query
    query.offset.return_value = query
    query.limit.return_value = query
    query.all.return_value = all_result
    return query


def test_get_doctors_without_specializations():
    query = _mock_query_chain(all_result=["doctor"])
    db = MagicMock(name="db")
    db.query.return_value = query

    result = service.get_doctors(db=db, skip=1, limit=3, specializations=None)

    assert result == ["doctor"]
    db.query.assert_called_once_with(models.Doctor)
    query.filter.assert_not_called()
    query.order_by.assert_called_once()
    query.offset.assert_called_once_with(1)
    query.limit.assert_called_once_with(3)
    query.all.assert_called_once()


def test_get_doctors_with_specializations_applies_filter():
    query = _mock_query_chain(all_result=[])
    db = MagicMock(name="db")
    db.query.return_value = query

    result = service.get_doctors(
        db=db,
        skip=0,
        limit=10,
        specializations=["Cardiology", "Neurology"],
    )

    assert result == []
    query.filter.assert_called_once()
    filter_expression = query.filter.call_args.args[0]
    filter_params = filter_expression.compile().params
    assert "%Cardiology%" in filter_params.values()
    assert "%Neurology%" in filter_params.values()
    query.order_by.assert_called_once()
    query.offset.assert_called_once_with(0)
    query.limit.assert_called_once_with(10)


def test_create_doctor_persists_and_returns_entity():
    db = MagicMock(name="db")
    doctor_in = schemas.DoctorCreate(name="Dr. Create", speciality="Cardiology")

    created = service.create_doctor(db=db, doctor=doctor_in)

    assert isinstance(created, models.Doctor)
    assert created.name == "Dr. Create"
    assert created.speciality == "Cardiology"
    db.add.assert_called_once_with(created)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(created)


def test_import_doctors_updates_existing_and_creates_new():
    doctors_payload = [
        {
            "name": "Dr. Existing",
            "title": "Consultant",
            "specialty": "Cardiology",
            "educationalDegree": "MBBS",
            "description": "Updated profile",
            "location": "Dhaka",
            "dataSource": "unit-test",
            "dataScrappedAt": "2026-01-15",
            "clinics": ["Clinic X"],
            "chambers": ["Chamber X"],
        },
        {
            "name": "Dr. New",
            "title": "Assistant Professor",
            "specialty": "Neurology",
            "educationalDegree": "MD",
            "description": "New profile",
            "location": "Chittagong",
            "dataSource": "unit-test",
            "dataScrappedAt": None,
            "clinics": ["Clinic A"],
            "chambers": ["Chamber A"],
        },
    ]

    existing_doctor = SimpleNamespace(
        name="Old Name",
        title=None,
        speciality="Old Specialty",
        educational_degree=None,
        description=None,
        location=None,
        data_source=None,
        data_scrapped_at=None,
        clinics=[],
        chambers=[],
    )

    db = MagicMock(name="db")
    query = MagicMock(name="query")
    db.query.return_value = query
    query.filter.return_value = query
    query.first.side_effect = [existing_doctor, None]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as file:
        json.dump(doctors_payload, file)
        file_path = file.name

    try:
        result = service.import_doctors(db=db, file_path=file_path)
    finally:
        os.unlink(file_path)

    assert result == {"imported": 1, "updated": 1}
    assert existing_doctor.name == "Dr. Existing"
    assert existing_doctor.title == "Consultant"
    assert existing_doctor.speciality == "Cardiology"
    assert existing_doctor.location == "Dhaka"
    assert existing_doctor.data_source is None
    assert existing_doctor.dataSource == "unit-test"
    assert existing_doctor.data_scrapped_at == datetime(2026, 1, 15)
    assert existing_doctor.clinics == ["Clinic X"]
    assert existing_doctor.chambers == ["Chamber X"]

    db.add.assert_called_once()
    added_doctor = db.add.call_args.args[0]
    assert isinstance(added_doctor, models.Doctor)
    assert added_doctor.name == "Dr. New"
    assert added_doctor.speciality == "Neurology"
    assert added_doctor.educational_degree == "MD"
    assert added_doctor.data_scrapped_at is None
    assert added_doctor.clinics == ["Clinic A"]
    assert added_doctor.chambers == ["Chamber A"]

    assert query.first.call_count == 2
    db.commit.assert_called_once()
