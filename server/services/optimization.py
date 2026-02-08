"""Optimization service for suggesting cost savings"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from collections import defaultdict
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import Event
from models.schemas import OptimizationSuggestion


class OptimizationService:
    """Service for generating optimization suggestions"""
    
    # Model alternatives (cheaper alternatives)
    MODEL_ALTERNATIVES = {
        "gpt-4": "gpt-4o-mini",
        "gpt-4-turbo": "gpt-4o",
        "gpt-4o": "gpt-4o-mini",
        "claude-3-opus": "claude-3-sonnet",
        "claude-3-5-sonnet": "claude-3-haiku",
    }
    
    # Approximate cost savings percentages
    COST_SAVINGS = {
        ("gpt-4", "gpt-4o-mini"): 95.0,
        ("gpt-4-turbo", "gpt-4o"): 75.0,
        ("gpt-4o", "gpt-4o-mini"): 94.0,
        ("claude-3-opus", "claude-3-sonnet"): 80.0,
        ("claude-3-5-sonnet", "claude-3-haiku"): 92.0,
    }
    
    def get_suggestions(
        self,
        db: Session,
        project: Optional[str] = None,
    ) -> List[OptimizationSuggestion]:
        """
        Generate optimization suggestions based on usage patterns
        """
        suggestions = []
        
        # Get last 30 days of data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        query = db.query(Event).filter(Event.timestamp >= start_date)
        if project:
            query = query.filter(Event.project == project)
        
        events = query.all()
        
        if not events:
            return suggestions
        
        # Analyze model usage
        model_suggestions = self._analyze_model_usage(events)
        suggestions.extend(model_suggestions)
        
        # Analyze prompt size
        prompt_suggestions = self._analyze_prompt_size(events)
        suggestions.extend(prompt_suggestions)
        
        # Analyze caching opportunities
        caching_suggestions = self._analyze_caching_opportunities(events)
        suggestions.extend(caching_suggestions)
        
        return suggestions
    
    def _analyze_model_usage(self, events: List[Event]) -> List[OptimizationSuggestion]:
        """Suggest cheaper model alternatives"""
        suggestions = []
        
        # Group by model
        model_stats = defaultdict(lambda: {"count": 0, "cost": 0.0})
        for event in events:
            model_stats[event.model]["count"] += 1
            model_stats[event.model]["cost"] += event.cost.total_cost if event.cost else 0.0
        
        # Check for expensive models with cheaper alternatives
        for model, stats in model_stats.items():
            # Check if model has an alternative
            alternative = None
            for expensive_model in self.MODEL_ALTERNATIVES:
                if model.startswith(expensive_model):
                    alternative = self.MODEL_ALTERNATIVES[expensive_model]
                    break
            
            if alternative and stats["cost"] > 1.0:  # Only suggest if significant cost
                # Calculate savings
                savings_key = None
                for key in self.COST_SAVINGS:
                    if model.startswith(key[0]):
                        savings_key = key
                        break
                
                if savings_key:
                    savings_percent = self.COST_SAVINGS[savings_key]
                    estimated_savings = stats["cost"] * (savings_percent / 100)
                    
                    suggestions.append(
                        OptimizationSuggestion(
                            type="model",
                            current=model,
                            suggested=alternative,
                            estimated_savings=round(estimated_savings, 4),
                            estimated_savings_percent=savings_percent,
                            reason=f"Switch to {alternative} for {savings_percent}% cost reduction. "
                                   f"Current monthly cost: ${stats['cost']:.2f} ({stats['count']} requests)",
                        )
                    )
        
        return suggestions
    
    def _analyze_prompt_size(self, events: List[Event]) -> List[OptimizationSuggestion]:
        """Suggest prompt optimization based on token usage"""
        suggestions = []
        
        # Find events with unusually large prompts
        large_prompt_events = [e for e in events if e.prompt_tokens > 4000]
        
        if large_prompt_events:
            total_large_cost = sum(e.cost.total_cost if e.cost else 0.0 for e in large_prompt_events)
            
            # Estimate 30% reduction from prompt optimization
            estimated_savings = total_large_cost * 0.3
            
            if estimated_savings > 1.0:
                suggestions.append(
                    OptimizationSuggestion(
                        type="prompt",
                        current=f"{len(large_prompt_events)} requests with >4000 prompt tokens",
                        suggested="Optimize prompts: reduce context, use summarization",
                        estimated_savings=round(estimated_savings, 4),
                        estimated_savings_percent=30.0,
                        reason=f"Large prompts detected in {len(large_prompt_events)} requests. "
                               f"Consider reducing context or using prompt compression techniques.",
                    )
                )
        
        return suggestions
    
    def _analyze_caching_opportunities(self, events: List[Event]) -> List[OptimizationSuggestion]:
        """Suggest caching for repeated patterns"""
        suggestions = []
        
        # Group by project/agent to find repeated patterns
        project_agent_stats = defaultdict(lambda: {"count": 0, "cost": 0.0})
        
        for event in events:
            if event.project and event.agent:
                key = f"{event.project}/{event.agent}"
                project_agent_stats[key]["count"] += 1
                project_agent_stats[key]["cost"] += event.cost.total_cost if event.cost else 0.0
        
        # Look for high-frequency patterns
        for key, stats in project_agent_stats.items():
            if stats["count"] > 100:  # High frequency
                # Estimate 20% savings from caching
                estimated_savings = stats["cost"] * 0.2
                
                if estimated_savings > 1.0:
                    suggestions.append(
                        OptimizationSuggestion(
                            type="caching",
                            current=f"{key}: {stats['count']} requests",
                            suggested="Implement response caching for repeated queries",
                            estimated_savings=round(estimated_savings, 4),
                            estimated_savings_percent=20.0,
                            reason=f"High-frequency pattern detected ({stats['count']} requests). "
                                   f"Caching could reduce costs by ~20%.",
                        )
                    )
        
        return suggestions
