"""Database models for AI Cost Observatory"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Date, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Event(Base):
    """Core events table - stores all LLM call events"""
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    event_type = Column(String(50), nullable=False, default="llm_call")
    
    # LLM details
    model = Column(String(100), nullable=False, index=True)
    prompt_tokens = Column(Integer, nullable=False, default=0)
    completion_tokens = Column(Integer, nullable=False, default=0)
    total_tokens = Column(Integer, nullable=False, default=0)
    latency_ms = Column(Integer, nullable=False, default=0)
    
    # Metadata
    project = Column(String(100), index=True)
    agent = Column(String(100), index=True)
    step = Column(String(100))
    user_id = Column(String(100), index=True)
    tags = Column(JSON, default=dict)
    
    # Relationships
    cost = relationship("Cost", back_populates="event", uselist=False, cascade="all, delete-orphan")
    retrieval_metrics = relationship("RetrievalMetric", back_populates="event", uselist=False, cascade="all, delete-orphan")
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_project_timestamp', 'project', 'timestamp'),
        Index('idx_agent_timestamp', 'agent', 'timestamp'),
        Index('idx_model_timestamp', 'model', 'timestamp'),
    )


class Cost(Base):
    """Cost information for events"""
    __tablename__ = "costs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    input_cost = Column(Float, nullable=False, default=0.0)
    output_cost = Column(Float, nullable=False, default=0.0)
    total_cost = Column(Float, nullable=False, default=0.0)
    currency = Column(String(10), nullable=False, default="USD")
    
    # Relationship
    event = relationship("Event", back_populates="cost")


class RetrievalMetric(Base):
    """Retrieval metrics for RAG systems"""
    __tablename__ = "retrieval_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    chunks = Column(Integer, nullable=False, default=0)
    context_tokens = Column(Integer, nullable=False, default=0)
    source = Column(String(100))
    
    # Relationship
    event = relationship("Event", back_populates="retrieval_metrics")


class ModelPricing(Base):
    """Model pricing reference table"""
    __tablename__ = "model_pricing"
    
    name = Column(String(100), primary_key=True)
    input_price = Column(Float, nullable=False, default=0.0)  # Per 1M tokens
    output_price = Column(Float, nullable=False, default=0.0)  # Per 1M tokens
    currency = Column(String(10), nullable=False, default="USD")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class DailyAggregate(Base):
    """Daily aggregates for fast dashboard queries"""
    __tablename__ = "daily_aggregates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False, index=True)
    project = Column(String(100), index=True)
    agent = Column(String(100))
    model = Column(String(100))
    
    total_requests = Column(Integer, nullable=False, default=0)
    total_tokens = Column(Integer, nullable=False, default=0)
    total_cost = Column(Float, nullable=False, default=0.0)
    avg_latency_ms = Column(Float, nullable=False, default=0.0)
    
    __table_args__ = (
        Index('idx_daily_agg_date_project', 'date', 'project'),
    )
