from datetime import date, datetime, timezone

from .extensions import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(24), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(24), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(240), nullable=False)
    emergency_contact = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    admissions = db.relationship("Admission", back_populates="patient", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def to_dict(self):
        return {
            "id": self.id,
            "mrn": self.mrn,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "fullName": self.full_name,
            "dateOfBirth": self.date_of_birth.isoformat(),
            "age": self.age,
            "sex": self.sex,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "emergencyContact": self.emergency_contact,
            "createdAt": self.created_at.isoformat(),
        }


class Admission(db.Model):
    __tablename__ = "admissions"

    id = db.Column(db.Integer, primary_key=True)
    admission_no = db.Column(db.String(28), unique=True, nullable=False, index=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    visit_type = db.Column(db.String(60), nullable=False)
    chief_complaint = db.Column(db.String(240), nullable=False)
    priority = db.Column(db.String(30), nullable=False, default="Routine")
    status = db.Column(db.String(30), nullable=False, default="Admitted")
    payment_method = db.Column(db.String(60), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    admitted_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    discharged_at = db.Column(db.DateTime(timezone=True), nullable=True)

    patient = db.relationship("Patient", back_populates="admissions")

    def to_dict(self, include_patient=True):
        payload = {
            "id": self.id,
            "admissionNo": self.admission_no,
            "patientId": self.patient_id,
            "department": self.department,
            "provider": self.provider,
            "visitType": self.visit_type,
            "chiefComplaint": self.chief_complaint,
            "priority": self.priority,
            "status": self.status,
            "paymentMethod": self.payment_method,
            "notes": self.notes,
            "admittedAt": self.admitted_at.isoformat(),
            "dischargedAt": self.discharged_at.isoformat() if self.discharged_at else None,
        }
        if include_patient:
            payload["patient"] = self.patient.to_dict()
        return payload
