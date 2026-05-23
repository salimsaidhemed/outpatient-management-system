from datetime import date, datetime, timezone

from flask import Blueprint, jsonify, request
from sqlalchemy import desc, func, or_

from .auth import require_auth, require_roles
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


def reject_blank(payload, fields):
    blank = [field for field in fields if field in payload and not str(payload.get(field) or "").strip()]
    if blank:
        raise ValueError(f"Field(s) cannot be blank: {', '.join(blank)}")


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
    active_admissions = (
        db.session.query(func.count(Admission.id))
        .filter(Admission.status.notin_(["Discharged", "Cancelled"]))
        .scalar()
    )
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
@require_roles("admissions_user", "admissions_admin")
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


@api.patch("/patients/<int:patient_id>")
@require_roles("admissions_user", "admissions_admin")
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    payload = request.get_json() or {}
    reject_blank(payload, ["firstName", "lastName", "dateOfBirth", "sex", "phone", "address"])

    if "firstName" in payload:
        patient.first_name = payload["firstName"].strip()
    if "lastName" in payload:
        patient.last_name = payload["lastName"].strip()
    if "dateOfBirth" in payload:
        patient.date_of_birth = parse_date(payload["dateOfBirth"], "dateOfBirth")
    if "sex" in payload:
        patient.sex = payload["sex"]
    if "phone" in payload:
        patient.phone = payload["phone"]
    if "email" in payload:
        patient.email = payload.get("email") or None
    if "address" in payload:
        patient.address = payload["address"]
    if "emergencyContact" in payload:
        patient.emergency_contact = payload.get("emergencyContact") or None

    db.session.commit()
    return patient.to_dict()


@api.get("/admissions")
def list_admissions():
    admissions = Admission.query.order_by(desc(Admission.admitted_at)).all()
    return {"admissions": [admission.to_dict() for admission in admissions]}


@api.post("/admissions")
@require_roles("admissions_user", "admissions_admin")
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
@require_roles("admissions_admin")
def discharge_admission(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    admission.status = "Discharged"
    admission.discharged_at = datetime.now(timezone.utc)
    db.session.commit()
    return admission.to_dict()


@api.patch("/admissions/<int:admission_id>/status")
@require_roles("admissions_admin")
def update_admission_status(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    payload = request.get_json() or {}
    required(payload, ["status"])

    allowed_statuses = {"Admitted", "In Progress", "Ready for Discharge", "Discharged", "Cancelled"}
    if payload["status"] not in allowed_statuses:
        raise ValueError(f"status must be one of: {', '.join(sorted(allowed_statuses))}")

    admission.status = payload["status"]
    admission.discharged_at = datetime.now(timezone.utc) if admission.status == "Discharged" else None
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
