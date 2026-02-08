"""Core SDK functionality for tracking LLM usage"""

import time
import uuid
import requests
import functools
from typing import Any, Dict, Optional, Callable
from contextlib import contextmanager
from datetime import datetime

from .config import get_config
from .adapters import get_adapter_registry


class ObservationContext:
    """Context manager for observing LLM calls"""
    
    def __init__(
        self,
        project: str,
        agent: Optional[str] = None,
        step: Optional[str] = None,
        user_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        endpoint: Optional[str] = None,
    ):
        self.project = project
        self.agent = agent
        self.step = step
        self.user_id = user_id
        self.tags = tags or {}
        self.endpoint = endpoint
        self.start_time = None
        self.event_id = str(uuid.uuid4())
        
    def __enter__(self):
        """Start timing"""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End timing and send event if possible"""
        if exc_type is None:
            # No automatic event sending here - let user handle response
            pass
        return False
    
    def track_response(self, response: Any):
        """Track an LLM response"""
        if not get_config().enabled:
            return
        
        latency_ms = int((time.time() - self.start_time) * 1000) if self.start_time else 0
        
        # Get appropriate adapter
        registry = get_adapter_registry()
        adapter = registry.get_adapter(response)
        
        if not adapter:
            # Unknown provider - try to extract basic info
            log_event(
                model="unknown",
                prompt_tokens=0,
                completion_tokens=0,
                latency_ms=latency_ms,
                project=self.project,
                agent=self.agent,
                step=self.step,
                user_id=self.user_id,
                tags=self.tags,
                endpoint=self.endpoint,
            )
            return
        
        # Extract usage and cost
        usage = adapter.extract_usage(response)
        cost_info = adapter.extract_cost(usage, usage["model"])
        
        # Send event
        _send_event(
            event_id=self.event_id,
            model=usage["model"],
            prompt_tokens=usage["prompt_tokens"],
            completion_tokens=usage["completion_tokens"],
            total_tokens=usage["total_tokens"],
            latency_ms=latency_ms,
            input_cost=cost_info["input_cost"],
            output_cost=cost_info["output_cost"],
            total_cost=cost_info["total_cost"],
            currency=cost_info["currency"],
            project=self.project,
            agent=self.agent,
            step=self.step,
            user_id=self.user_id,
            tags=self.tags,
            endpoint=self.endpoint,
        )


@contextmanager
def observe(
    project: str,
    agent: Optional[str] = None,
    step: Optional[str] = None,
    user_id: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None,
    endpoint: Optional[str] = None,
):
    """
    Context manager for observing LLM calls
    
    Args:
        project: Project name
        agent: Agent name (optional)
        step: Step name (optional)
        user_id: User ID (optional)
        tags: Additional tags (optional)
        endpoint: Custom endpoint (optional)
        
    Example:
        with observe(project="rag-app", agent="planner") as obs:
            response = client.chat.completions.create(...)
            obs.track_response(response)
    """
    ctx = ObservationContext(
        project=project,
        agent=agent,
        step=step,
        user_id=user_id,
        tags=tags,
        endpoint=endpoint,
    )
    
    with ctx:
        yield ctx


def log_event(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    latency_ms: int = 0,
    project: Optional[str] = None,
    agent: Optional[str] = None,
    step: Optional[str] = None,
    user_id: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None,
    endpoint: Optional[str] = None,
    input_cost: float = 0.0,
    output_cost: float = 0.0,
    total_cost: float = 0.0,
    currency: str = "USD",
):
    """
    Manually log an event
    
    Args:
        model: Model name
        prompt_tokens: Number of prompt tokens
        completion_tokens: Number of completion tokens
        latency_ms: Latency in milliseconds
        project: Project name
        agent: Agent name
        step: Step name
        user_id: User ID
        tags: Additional tags
        endpoint: Custom endpoint
        input_cost: Input cost
        output_cost: Output cost
        total_cost: Total cost
        currency: Currency code
        
    Example:
        log_event(
            model="gpt-4o",
            prompt_tokens=200,
            completion_tokens=90,
            project="support-bot",
            tags={"feature": "search"}
        )
    """
    if not get_config().enabled:
        return
    
    _send_event(
        event_id=str(uuid.uuid4()),
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens,
        latency_ms=latency_ms,
        input_cost=input_cost,
        output_cost=output_cost,
        total_cost=total_cost,
        currency=currency,
        project=project,
        agent=agent,
        step=step,
        user_id=user_id,
        tags=tags,
        endpoint=endpoint,
    )


def track_retrieval(
    chunks: int,
    context_tokens: int,
    source: Optional[str] = None,
    project: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None,
    endpoint: Optional[str] = None,
):
    """
    Track RAG retrieval metrics
    
    Args:
        chunks: Number of chunks retrieved
        context_tokens: Total context tokens
        source: Source name (e.g., "knowledge_base")
        project: Project name
        tags: Additional tags
        endpoint: Custom endpoint
        
    Example:
        track_retrieval(
            chunks=6,
            context_tokens=1800,
            source="knowledge_base",
            project="rag-app"
        )
    """
    if not get_config().enabled:
        return
    
    config = get_config()
    endpoint_url = endpoint or config.endpoint
    
    payload = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "retrieval",
        "chunks": chunks,
        "context_tokens": context_tokens,
        "source": source,
        "project": project,
        "tags": tags or {},
    }
    
    try:
        requests.post(
            f"{endpoint_url}/events",
            json=payload,
            headers={"Authorization": f"Bearer {config.api_key}"} if config.api_key else {},
            timeout=config.timeout,
        )
    except Exception as e:
        # Silent failure - don't break user's code
        pass


def traced(
    project: Optional[str] = None,
    agent: Optional[str] = None,
    step: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None,
):
    """
    Decorator for tracing functions
    
    Args:
        project: Project name
        agent: Agent name
        step: Step name
        tags: Additional tags
        
    Example:
        @traced(project="rag-app", agent="executor")
        def run_agent():
            return client.chat.completions.create(...)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with observe(
                project=project or func.__name__,
                agent=agent,
                step=step,
                tags=tags,
            ) as obs:
                result = func(*args, **kwargs)
                
                # Try to track if result looks like an LLM response
                registry = get_adapter_registry()
                adapter = registry.get_adapter(result)
                if adapter:
                    obs.track_response(result)
                
                return result
        return wrapper
    return decorator


def _send_event(
    event_id: str,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
    latency_ms: int,
    input_cost: float,
    output_cost: float,
    total_cost: float,
    currency: str,
    project: Optional[str],
    agent: Optional[str],
    step: Optional[str],
    user_id: Optional[str],
    tags: Optional[Dict[str, Any]],
    endpoint: Optional[str],
):
    """Internal function to send event to collector"""
    config = get_config()
    endpoint_url = endpoint or config.endpoint
    
    payload = {
        "event_id": event_id,
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "llm_call",
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "latency_ms": latency_ms,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "currency": currency,
        "project": project,
        "agent": agent,
        "step": step,
        "user_id": user_id,
        "tags": tags or {},
    }
    
    try:
        requests.post(
            f"{endpoint_url}/events",
            json=payload,
            headers={"Authorization": f"Bearer {config.api_key}"} if config.api_key else {},
            timeout=config.timeout,
        )
    except Exception as e:
        # Silent failure - don't break user's code
        pass
