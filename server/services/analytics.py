"""Analytics service for computing statistics"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Optional, List
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import Event, Cost
from models.schemas import (
    DashboardOverview,
    CostStats,
    ModelStats,
    AgentStats,
    TimeSeriesPoint,
)


class AnalyticsService:
    """Service for analytics and statistics"""
    
    def get_overview(self, db: Session, project: Optional[str] = None) -> DashboardOverview:
        """Get dashboard overview data"""
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Base query
        base_query = db.query(Event)
        if project:
            base_query = base_query.filter(Event.project == project)
        
        # Today's cost
        today_events = base_query.filter(Event.timestamp >= today_start).all()
        today_cost = sum(e.cost.total_cost if e.cost else 0.0 for e in today_events)
        
        # Month's cost
        month_events = base_query.filter(Event.timestamp >= month_start).all()
        month_cost = sum(e.cost.total_cost if e.cost else 0.0 for e in month_events)
        
        # Total tokens
        total_tokens = sum(e.total_tokens for e in month_events)
        
        # Average cost per request
        avg_cost = month_cost / len(month_events) if month_events else 0.0
        
        # Active models
        active_models = len(set(e.model for e in month_events))
        
        # Cost over time (last 30 days)
        cost_over_time = self._get_cost_over_time(db, project, days=30)
        
        # Top models
        top_models = self.get_model_stats(db, project, limit=5)
        
        # Top agents
        top_agents = self.get_agent_stats(db, project, limit=5)
        
        return DashboardOverview(
            today_cost=round(today_cost, 4),
            month_cost=round(month_cost, 4),
            total_tokens=total_tokens,
            avg_cost_per_request=round(avg_cost, 6),
            active_models=active_models,
            cost_over_time=cost_over_time,
            top_models=top_models,
            top_agents=top_agents,
        )
    
    def get_cost_stats(
        self,
        db: Session,
        project: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> CostStats:
        """Get cost statistics"""
        query = db.query(Event)
        
        if project:
            query = query.filter(Event.project == project)
        if start_date:
            query = query.filter(Event.timestamp >= start_date)
        if end_date:
            query = query.filter(Event.timestamp <= end_date)
        
        events = query.all()
        
        total_cost = sum(e.cost.total_cost if e.cost else 0.0 for e in events)
        total_tokens = sum(e.total_tokens for e in events)
        total_requests = len(events)
        avg_cost = total_cost / total_requests if total_requests > 0 else 0.0
        
        return CostStats(
            total_cost=round(total_cost, 4),
            total_tokens=total_tokens,
            total_requests=total_requests,
            avg_cost_per_request=round(avg_cost, 6),
            currency="USD",
        )
    
    def get_model_stats(
        self,
        db: Session,
        project: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10,
    ) -> List[ModelStats]:
        """Get model usage statistics"""
        query = db.query(Event)
        
        if project:
            query = query.filter(Event.project == project)
        if start_date:
            query = query.filter(Event.timestamp >= start_date)
        if end_date:
            query = query.filter(Event.timestamp <= end_date)
        
        events = query.all()
        
        # Group by model
        model_data = {}
        for event in events:
            if event.model not in model_data:
                model_data[event.model] = {
                    "requests": 0,
                    "tokens": 0,
                    "cost": 0.0,
                }
            
            model_data[event.model]["requests"] += 1
            model_data[event.model]["tokens"] += event.total_tokens
            model_data[event.model]["cost"] += event.cost.total_cost if event.cost else 0.0
        
        # Sort by cost
        result = [
            ModelStats(
                model=model,
                requests=data["requests"],
                tokens=data["tokens"],
                cost=round(data["cost"], 4),
            )
            for model, data in sorted(
                model_data.items(),
                key=lambda x: x[1]["cost"],
                reverse=True,
            )
        ]
        
        return result[:limit]
    
    def get_agent_stats(
        self,
        db: Session,
        project: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10,
    ) -> List[AgentStats]:
        """Get agent usage statistics"""
        query = db.query(Event).filter(Event.agent.isnot(None))
        
        if project:
            query = query.filter(Event.project == project)
        if start_date:
            query = query.filter(Event.timestamp >= start_date)
        if end_date:
            query = query.filter(Event.timestamp <= end_date)
        
        events = query.all()
        
        # Group by agent
        agent_data = {}
        for event in events:
            if event.agent not in agent_data:
                agent_data[event.agent] = {
                    "requests": 0,
                    "tokens": 0,
                    "cost": 0.0,
                }
            
            agent_data[event.agent]["requests"] += 1
            agent_data[event.agent]["tokens"] += event.total_tokens
            agent_data[event.agent]["cost"] += event.cost.total_cost if event.cost else 0.0
        
        # Sort by cost
        result = [
            AgentStats(
                agent=agent,
                requests=data["requests"],
                tokens=data["tokens"],
                cost=round(data["cost"], 4),
            )
            for agent, data in sorted(
                agent_data.items(),
                key=lambda x: x[1]["cost"],
                reverse=True,
            )
        ]
        
        return result[:limit]
    
    def _get_cost_over_time(
        self,
        db: Session,
        project: Optional[str] = None,
        days: int = 30,
    ) -> List[TimeSeriesPoint]:
        """Get cost over time series data"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        query = db.query(Event).filter(Event.timestamp >= start_date)
        if project:
            query = query.filter(Event.project == project)
        
        events = query.all()
        
        # Group by date
        daily_costs = {}
        for event in events:
            date = event.timestamp.date()
            if date not in daily_costs:
                daily_costs[date] = 0.0
            daily_costs[date] += event.cost.total_cost if event.cost else 0.0
        
        # Fill in missing dates
        result = []
        current_date = start_date.date()
        while current_date <= end_date.date():
            cost = daily_costs.get(current_date, 0.0)
            result.append(
                TimeSeriesPoint(
                    timestamp=datetime.combine(current_date, datetime.min.time()),
                    value=round(cost, 4),
                )
            )
            current_date += timedelta(days=1)
        
        return result
