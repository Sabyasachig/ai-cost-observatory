"""Main FastAPI application"""

import os
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import uuid

import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import get_db, init_db
from models.database import Event, Cost, RetrievalMetric, ModelPricing, DailyAggregate
from models.schemas import (
    EventCreate,
    EventResponse,
    DashboardOverview,
    CostStats,
    ModelStats,
    AgentStats,
    TimeSeriesPoint,
    ForecastResponse,
    OptimizationSuggestion,
)
from services.analytics import AnalyticsService
from services.forecasting import ForecastingService
from services.optimization import OptimizationService

# Create FastAPI app
app = FastAPI(
    title="AI Cost Observatory",
    description="Open-source observability layer for agentic systems",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
analytics_service = AnalyticsService()
forecasting_service = ForecastingService()
optimization_service = OptimizationService()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("AI Cost Observatory API started successfully!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI Cost Observatory",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/events", response_model=dict)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event
    
    This endpoint receives events from the SDK and stores them in the database.
    """
    try:
        # Create event record
        event_id = uuid.UUID(event.event_id) if event.event_id else uuid.uuid4()
        timestamp = event.timestamp or datetime.utcnow()
        
        # Calculate total tokens if not provided
        total_tokens = event.total_tokens or (event.prompt_tokens + event.completion_tokens)
        
        db_event = Event(
            id=event_id,
            timestamp=timestamp,
            event_type=event.event_type,
            model=event.model,
            prompt_tokens=event.prompt_tokens,
            completion_tokens=event.completion_tokens,
            total_tokens=total_tokens,
            latency_ms=event.latency_ms,
            project=event.project,
            agent=event.agent,
            step=event.step,
            user_id=event.user_id,
            tags=event.tags,
        )
        db.add(db_event)
        
        # Create cost record if provided
        if event.input_cost > 0 or event.output_cost > 0 or event.total_cost > 0:
            db_cost = Cost(
                event_id=event_id,
                input_cost=event.input_cost,
                output_cost=event.output_cost,
                total_cost=event.total_cost,
                currency=event.currency,
            )
            db.add(db_cost)
        
        # Create retrieval metrics if provided
        if event.chunks is not None or event.context_tokens is not None:
            db_retrieval = RetrievalMetric(
                event_id=event_id,
                chunks=event.chunks or 0,
                context_tokens=event.context_tokens or 0,
                source=event.source,
            )
            db.add(db_retrieval)
        
        db.commit()
        
        return {"status": "success", "event_id": str(event_id)}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events", response_model=List[EventResponse])
async def get_events(
    project: Optional[str] = None,
    agent: Optional[str] = None,
    model: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    Get events with filtering
    """
    query = db.query(Event)
    
    if project:
        query = query.filter(Event.project == project)
    if agent:
        query = query.filter(Event.agent == agent)
    if model:
        query = query.filter(Event.model == model)
    if start_date:
        query = query.filter(Event.timestamp >= start_date)
    if end_date:
        query = query.filter(Event.timestamp <= end_date)
    
    events = query.order_by(Event.timestamp.desc()).limit(limit).offset(offset).all()
    
    # Add cost information
    result = []
    for event in events:
        event_dict = {
            "id": event.id,
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "model": event.model,
            "prompt_tokens": event.prompt_tokens,
            "completion_tokens": event.completion_tokens,
            "total_tokens": event.total_tokens,
            "latency_ms": event.latency_ms,
            "project": event.project,
            "agent": event.agent,
            "step": event.step,
            "user_id": event.user_id,
            "tags": event.tags,
            "total_cost": event.cost.total_cost if event.cost else 0.0,
        }
        result.append(EventResponse(**event_dict))
    
    return result


@app.get("/dashboard/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    project: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get dashboard overview data
    """
    return analytics_service.get_overview(db, project)


@app.get("/stats/costs", response_model=CostStats)
async def get_cost_stats(
    project: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    """
    Get cost statistics
    """
    return analytics_service.get_cost_stats(db, project, start_date, end_date)


@app.get("/stats/models", response_model=List[ModelStats])
async def get_model_stats(
    project: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get model usage statistics
    """
    return analytics_service.get_model_stats(db, project, start_date, end_date, limit)


@app.get("/stats/agents", response_model=List[AgentStats])
async def get_agent_stats(
    project: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get agent usage statistics
    """
    return analytics_service.get_agent_stats(db, project, start_date, end_date, limit)


@app.get("/forecast", response_model=ForecastResponse)
async def get_forecast(
    project: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get cost forecast
    """
    return forecasting_service.get_forecast(db, project)


@app.get("/optimize", response_model=List[OptimizationSuggestion])
async def get_optimization_suggestions(
    project: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get optimization suggestions
    """
    return optimization_service.get_suggestions(db, project)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
