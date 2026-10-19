import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Boolean, Float
from app.database import Base

class ApplicationSubmission(Base):
    __tablename__ = "application_submissions"

    id = Column(String(64), primary_key=True, default=lambda: f"VF-{datetime.now().year}-{uuid.uuid4().hex[:8].upper()}")
    form_id = Column(String(64), nullable=False, index=True)
    form_name = Column(String(255), nullable=False)
    applicant_name = Column(String(255), nullable=True)
    applicant_phone = Column(String(20), nullable=True)
    applicant_aadhaar = Column(String(20), nullable=True)
    status = Column(String(50), default="SUBMITTED")  # SUBMITTED, UNDER_VERIFICATION, APPROVED
    form_data = Column(JSON, nullable=False)
    extracted_entities = Column(JSON, nullable=True)
    raw_transcript = Column(Text, nullable=True)
    language = Column(String(10), default="en")
    submitted_at = Column(DateTime, default=datetime.utcnow)
    verification_hash = Column(String(64), nullable=True)

class SchemeRecord(Base):
    __tablename__ = "schemes"

    id = Column(String(64), primary_key=True)
    title = Column(String(255), nullable=False)
    title_hi = Column(String(255), nullable=True)
    title_mr = Column(String(255), nullable=True)
    category = Column(String(100), nullable=False)  # Agriculture, Healthcare, Housing, Social Welfare, Education
    ministry = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    description_hi = Column(Text, nullable=True)
    description_mr = Column(Text, nullable=True)
    benefits = Column(JSON, nullable=False)  # List of benefit strings
    eligibility_criteria = Column(JSON, nullable=False)  # Min age, max age, max income, occupations, categories, etc.
    documents_required = Column(JSON, nullable=False)  # List of required docs
    official_portal_url = Column(String(255), nullable=True)
    target_beneficiaries = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

class VoiceAuditLog(Base):
    __tablename__ = "voice_audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), nullable=True)
    detected_language = Column(String(20), nullable=True)
    transcription = Column(Text, nullable=True)
    extracted_fields_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class ConsentedAudioSample(Base):
    __tablename__ = "consented_audio_samples"

    id = Column(String(64), primary_key=True, default=lambda: f"SMP-{datetime.now().year}-{uuid.uuid4().hex[:8].upper()}")
    audio_filename = Column(String(255), nullable=False)
    audio_relpath = Column(String(500), nullable=False)
    language = Column(String(20), nullable=False)
    transcript = Column(Text, nullable=False)
    review_status = Column(String(30), default="PENDING")  # PENDING, APPROVED, REJECTED
    consent_given = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

