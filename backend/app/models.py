"""Database tables — mirrors the SDD page 3 data layout.

Claim -> Document -> ExtractedFact        (intake + extraction)
Claim -> Analysis                          (severity / priority / risk, versioned)
PolicyChunk                                (RAG corpus, embedded)
Claim -> Decision                          (human decision, mandatory rationale)
AuditEvent                                 (append-only history)
"""
import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _uuid():
    return uuid.uuid4()


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    policy_number: Mapped[str] = mapped_column(String(64), index=True)
    loss_date: Mapped[datetime] = mapped_column(DateTime)
    loss_type: Mapped[str] = mapped_column(String(64))  # e.g. collision, theft, vandalism
    description: Mapped[str] = mapped_column(Text)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(32), default="open")  # open|in_review|decided
    version: Mapped[int] = mapped_column(Integer, default=1)  # bump on material edits
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    documents: Mapped[list["Document"]] = relationship(back_populates="claim")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    claim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("claims.id"), index=True)
    filename: Mapped[str] = mapped_column(String(255))
    doc_type: Mapped[str] = mapped_column(String(64))  # estimate | invoice | police_report | photo | other
    size_bytes: Mapped[int] = mapped_column(Integer)
    checksum_sha256: Mapped[str] = mapped_column(String(64), unique=True)
    s3_key: Mapped[str] = mapped_column(String(512))
    extraction_status: Mapped[str] = mapped_column(String(32), default="pending")  # pending|done|failed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    claim: Mapped["Claim"] = relationship(back_populates="documents")
    facts: Mapped[list["ExtractedFact"]] = relationship(back_populates="document")


class ExtractedFact(Base):
    """One extracted value with provenance: which document, which page."""
    __tablename__ = "extracted_facts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"), index=True)
    field: Mapped[str] = mapped_column(String(128))   # e.g. "repair_estimate_total"
    value: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    page: Mapped[int] = mapped_column(Integer)

    document: Mapped["Document"] = relationship(back_populates="facts")


class Analysis(Base):
    """AI output for one claim VERSION. Never edited in place — new version = new row."""
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    claim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("claims.id"), index=True)
    claim_version: Mapped[int] = mapped_column(Integer)
    severity: Mapped[str] = mapped_column(String(32))       # low | medium | high
    priority: Mapped[str] = mapped_column(String(32))       # routine | elevated | urgent
    risk_score: Mapped[float] = mapped_column(Float)        # 0..1, advisory only
    risk_reasons: Mapped[str] = mapped_column(Text)         # JSON list of reason codes
    summary: Mapped[str] = mapped_column(Text, default="")   # LLM structured summary (JSON)
    model_version: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default="done")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PolicyChunk(Base):
    """Chunked policy text + embedding for RAG. Filter by policy_id + version."""
    __tablename__ = "policy_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    policy_id: Mapped[str] = mapped_column(String(64), index=True)
    version: Mapped[str] = mapped_column(String(32), index=True)
    effective_date: Mapped[datetime] = mapped_column(DateTime)
    section: Mapped[str] = mapped_column(String(255))
    page: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list] = mapped_column(Vector(384))  # all-MiniLM-L6-v2 dim


class Decision(Base):
    """Human decision. rationale is mandatory; recorded_by identifies the adjuster."""
    __tablename__ = "decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    claim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("claims.id"), index=True)
    claim_version: Mapped[int] = mapped_column(Integer)
    action: Mapped[str] = mapped_column(String(32))  # approve | deny | request_info | refer
    rationale: Mapped[str] = mapped_column(Text)
    recorded_by: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AuditEvent(Base):
    """Append-only: who did what to which entity, when. Never updated/deleted."""
    __tablename__ = "audit_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    actor: Mapped[str] = mapped_column(String(128))
    action: Mapped[str] = mapped_column(String(64))
    entity: Mapped[str] = mapped_column(String(64))
    entity_id: Mapped[str] = mapped_column(String(64))
    claim_version: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
