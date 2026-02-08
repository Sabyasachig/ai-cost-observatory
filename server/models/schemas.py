"""Pydantic schemas for API requests and responses"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from uuid import UUID


class EventCreate(BaseModel):
    """Schema for creating an event"""
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    event_type: str = "llm_call"
    
    # LLM details
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: Optional[int] = None
    latency_ms: int = 0
    
    # Cost information
    input_cost: float = 0.0
    output_cost: float = 0.0
    total_cost: float = 0.0
    currency: str = "USD"
    
    # Metadata
    project: Optional[str] = None
    agent: Optional[str] = None
    step: Optional[str] = None
    user_id: Optional[str] = None
    tags: Dict[str, Any] = Field(default_factory=dict)
    
    # RAG metrics (optional)
    chunks: Optional[int] = None
    context_tokens: Optional[int] = None
    source: Optional[str] = None


class EventResponse(BaseModel):
    """Schema for event response"""
    id: UUID
    timestamp: datetime
    event_type: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_ms: int
    project: Optional[str]
    agent: Optional[str]
    step: Optional[str]
    user_id: Optional[str]
    tags: Dict[str, Any]
    total_cost: Optional[float] = None
    
    class Config:
        from_attributes = True


class CostStats(BaseModel):
    """Cost statistics"""
    total_cost: float
    total_tokens: int
    total_requests: int
    avg_cost_per_request: float
    currency: str = "USD"


class ModelStats(BaseModel):
    """Model usage statistics"""
    model: str
    requests: int
    tokens: int
    cost: float


class AgentStats(BaseModel):
    """Agent usage statistics"""
    agent: str
    requests: int
    tokens: int
    cost: float


class TimeSeriesPoint(BaseModel):
    """Time series data point"""
    timestamp: datetime
    value: float
    label: Optional[str] = None


class DashboardOverview(BaseModel):
    """Dashboard overview data"""
    today_cost: float
    month_cost: float
    total_tokens: int
    avg_cost_per_request: float
    active_models: int
    cost_over_time: List[TimeSeriesPoint]
    top_models: List[ModelStats]
    top_agents: List[AgentStats]


class ForecastResponse(BaseModel):
    """Forecast response"""
    monthly_projection: float
    daily_average: float
    trend: str  # "increasing", "decreasing", "stable"
    confidence: str  # "high", "medium", "low"


class OptimizationSuggestion(BaseModel):
    """Optimization suggestion"""
    type: str  # "model", "prompt", "caching"
    current: str
    suggested: str
    estimated_savings: float
    estimated_savings_percent: float
    reason: str
