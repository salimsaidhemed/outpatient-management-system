from datetime import date, datetime, timezone

from flask import Blueprint, jsonify, request
from sqlalchemy import desc, func, or_

from .auth import require_auth
from .extensions import db
from .models import Admission, Patient

api = Blueprint("api", __name__)


@api.before_request
def authenticate_api_request():
    if request.method == "OPTIONS":
        return None
    return require_auth(lambda: None)()


def parse_date(value, field_name):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must use YYYY-MM-DD format")


def required(payload, fields):
    missing = [field for field in fields if not payload.get(field)]
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")


def next_mrn():
    value = db.session.query(func.count(Patient.id)).scalar() + 1
    return f"MRN-{value:06d}"


def next_admission_no():
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    value = db.session.query(func.count(Admission.id)).scalar() + 1
    return f"OPD-{today}-{value:04d}"


@api.errorhandler(ValueError)
def handle_value_error(error):
    return jsonify({"error": str(error)}), 400


@api.get("/dashboard")
def dashboard():
    today = date.today()
    total_patients = db.session.query(func.count(Patient.id)).scalar()
    active_admissions = db.session.query(func.count(Admission.id)).filter(Admission.status != "Discharged").scalar()
    visits_today = (
        db.session.query(func.count(Admission.id))
        .filter(func.date(Admission.admitted_at) == today)
        .scalar()
    )
    recent_admissions = Admission.query.order_by(desc(Admission.admitted_at)).limit(6).all()

    by_department = (
        db.session.query(Admission.department, func.count(Admission.id))
        .group_by(Admission.department)
        .order_by(desc(func.count(Admission.id)))
        .all()
    )

    return {
        "totalPatients": total_patients,
        "activeAdmissions": active_admissions,
        "visitsToday": visits_today,
        "recentAdmissions": [admission.to_dict() for admission in recent_admissions],
        "departmentLoad": [{"department": name, "count": count} for name, count in by_department],
    }


@api.get("/patients")
def list_patients():
    query = request.args.get("q", "").strip()
    patients = Patient.query
    if query:
        pattern = f"%{query}%"
        patients = patients.filter(
            or_(
                Patient.mrn.ilike(pattern),
                Patient.first_name.ilike(pattern),
                Patient.last_name.ilike(pattern),
                Patient.phone.ilike(pattern),
            )
        )
    return {"patients": [patient.to_dict() for patient in patients.order_by(desc(Patient.created_at)).all()]}


@api.post("/patients")
def create_patient():
    payload = request.get_json() or {}
    required(payload, ["firstName", "lastName", "dateOfBirth", "sex", "phone", "address"])

    patient = Patient(
        mrn=payload.get("mrn") or next_mrn(),
        first_name=payload["firstName"].strip(),
        last_name=payload["lastName"].strip(),
        date_of_birth=parse_date(payload["dateOfBirth"], "dateOfBirth"),
        sex=payload["sex"],
        phone=payload["phone"],
        email=payload.get("email"),
        address=payload["address"],
        emergency_contact=payload.get("emergencyContact"),
    )
    db.session.add(patient)
    db.session.commit()
    return patient.to_dict(), 201


@api.get("/patients/<int:patient_id>")
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    visits = Admission.query.filter_by(patient_id=patient.id).order_by(desc(Admission.admitted_at)).all()
    return {"patient": patient.to_dict(), "visits": [visit.to_dict(include_patient=False) for visit in visits]}


@api.get("/admissions")
def list_admissions():
    admissions = Admission.query.order_by(desc(Admission.admitted_at)).all()
    return {"admissions": [admission.to_dict() for admission in admissions]}


@api.post("/admissions")
def create_admission():
    payload = request.get_json() or {}
    required(
        payload,
        ["patientId", "department", "provider", "visitType", "chiefComplaint", "paymentMethod"],
    )
    Patient.query.get_or_404(payload["patientId"])

    admission = Admission(
        admission_no=next_admission_no(),
        patient_id=payload["patientId"],
        department=payload["department"],
        provider=payload["provider"],
        visit_type=payload["visitType"],
        chief_complaint=payload["chiefComplaint"],
        priority=payload.get("priority", "Routine"),
        payment_method=payload["paymentMethod"],
        notes=payload.get("notes"),
    )
    db.session.add(admission)
    db.session.commit()
    return admission.to_dict(), 201


@api.patch("/admissions/<int:admission_id>/discharge")
def discharge_admission(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    admission.status = "Discharged"
    admission.discharged_at = datetime.now(timezone.utc)
    db.session.commit()
    return admission.to_dict()


@api.get("/admissions/<int:admission_id>/receipt")
def admission_receipt(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    return {
        "facility": {
            "name": "Outpatient Admissions Center",
            "address": "100 Wellness Avenue",
            "phone": "+1 (555) 010-2040",
        },
        "receipt": admission.to_dict(),
        "issuedAt": datetime.now(timezone.utc).isoformat(),
    }
