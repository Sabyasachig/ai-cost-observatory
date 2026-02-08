"""Forecasting service for predicting future costs"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import statistics
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import Event
from models.schemas import ForecastResponse


class ForecastingService:
    """Service for cost forecasting"""
    
    def get_forecast(self, db: Session, project: Optional[str] = None) -> ForecastResponse:
        """
        Get cost forecast based on recent trends
        
        Uses simple moving average and linear projection
        """
        # Get last 30 days of data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        query = db.query(Event).filter(Event.timestamp >= start_date)
        if project:
            query = query.filter(Event.project == project)
        
        events = query.all()
        
        if not events:
            return ForecastResponse(
                monthly_projection=0.0,
                daily_average=0.0,
                trend="stable",
                confidence="low",
            )
        
        # Group by date
        daily_costs = {}
        for event in events:
            date = event.timestamp.date()
            if date not in daily_costs:
                daily_costs[date] = 0.0
            daily_costs[date] += event.cost.total_cost if event.cost else 0.0
        
        # Get daily averages
        sorted_dates = sorted(daily_costs.keys())
        daily_values = [daily_costs[date] for date in sorted_dates]
        
        # Calculate daily average
        daily_average = statistics.mean(daily_values) if daily_values else 0.0
        
        # Calculate trend
        if len(daily_values) >= 7:
            recent_avg = statistics.mean(daily_values[-7:])
            older_avg = statistics.mean(daily_values[:7])
            
            if recent_avg > older_avg * 1.1:
                trend = "increasing"
            elif recent_avg < older_avg * 0.9:
                trend = "decreasing"
            else:
                trend = "stable"
            
            # Calculate confidence based on data consistency
            std_dev = statistics.stdev(daily_values) if len(daily_values) > 1 else 0
            cv = (std_dev / daily_average) if daily_average > 0 else 0
            
            if cv < 0.2:
                confidence = "high"
            elif cv < 0.5:
                confidence = "medium"
            else:
                confidence = "low"
        else:
            trend = "stable"
            confidence = "low"
        
        # Project monthly cost
        # For increasing trend, add 10% buffer
        # For decreasing trend, reduce by 10%
        monthly_base = daily_average * 30
        
        if trend == "increasing":
            monthly_projection = monthly_base * 1.1
        elif trend == "decreasing":
            monthly_projection = monthly_base * 0.9
        else:
            monthly_projection = monthly_base
        
        return ForecastResponse(
            monthly_projection=round(monthly_projection, 2),
            daily_average=round(daily_average, 4),
            trend=trend,
            confidence=confidence,
        )
