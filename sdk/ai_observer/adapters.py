"""Provider adapters for extracting usage and cost from different LLM providers"""

from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class ProviderAdapter(ABC):
    """Base class for provider adapters"""
    
    @abstractmethod
    def extract_usage(self, response: Any) -> Dict[str, Any]:
        """Extract usage information from provider response"""
        pass
    
    @abstractmethod
    def extract_cost(self, usage: Dict[str, Any], model: str) -> Dict[str, float]:
        """Calculate cost from usage information"""
        pass
    
    @abstractmethod
    def can_handle(self, response: Any) -> bool:
        """Check if this adapter can handle the response"""
        pass


class OpenAIAdapter(ProviderAdapter):
    """Adapter for OpenAI API responses"""
    
    # Pricing per 1M tokens (as of Feb 2026)
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.150, "output": 0.600},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        "o1-preview": {"input": 15.00, "output": 60.00},
        "o1-mini": {"input": 3.00, "output": 12.00},
    }
    
    def can_handle(self, response: Any) -> bool:
        """Check if response is from OpenAI"""
        return hasattr(response, 'usage') and hasattr(response, 'model')
    
    def extract_usage(self, response: Any) -> Dict[str, Any]:
        """Extract usage from OpenAI response"""
        usage = response.usage
        return {
            "model": response.model,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        }
    
    def extract_cost(self, usage: Dict[str, Any], model: str) -> Dict[str, float]:
        """Calculate cost from OpenAI usage"""
        model_key = model
        
        # Handle model versions
        for key in self.PRICING.keys():
            if model.startswith(key):
                model_key = key
                break
        
        pricing = self.PRICING.get(model_key, {"input": 0.0, "output": 0.0})
        
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        
        # Cost per million tokens
        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]
        
        return {
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(input_cost + output_cost, 6),
            "currency": "USD",
        }


class AnthropicAdapter(ProviderAdapter):
    """Adapter for Anthropic API responses"""
    
    # Pricing per 1M tokens
    PRICING = {
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
        "claude-3-opus": {"input": 15.00, "output": 75.00},
        "claude-3-sonnet": {"input": 3.00, "output": 15.00},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "claude-2.1": {"input": 8.00, "output": 24.00},
        "claude-2": {"input": 8.00, "output": 24.00},
    }
    
    def can_handle(self, response: Any) -> bool:
        """Check if response is from Anthropic"""
        return hasattr(response, 'usage') and hasattr(response, 'model') and 'claude' in str(response.model).lower()
    
    def extract_usage(self, response: Any) -> Dict[str, Any]:
        """Extract usage from Anthropic response"""
        usage = response.usage
        return {
            "model": response.model,
            "prompt_tokens": usage.input_tokens,
            "completion_tokens": usage.output_tokens,
            "total_tokens": usage.input_tokens + usage.output_tokens,
        }
    
    def extract_cost(self, usage: Dict[str, Any], model: str) -> Dict[str, float]:
        """Calculate cost from Anthropic usage"""
        model_key = model
        
        for key in self.PRICING.keys():
            if model.startswith(key):
                model_key = key
                break
        
        pricing = self.PRICING.get(model_key, {"input": 0.0, "output": 0.0})
        
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        
        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]
        
        return {
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(input_cost + output_cost, 6),
            "currency": "USD",
        }


class AdapterRegistry:
    """Registry for managing provider adapters"""
    
    def __init__(self):
        self.adapters = [
            OpenAIAdapter(),
            AnthropicAdapter(),
        ]
    
    def get_adapter(self, response: Any) -> Optional[ProviderAdapter]:
        """Get the appropriate adapter for a response"""
        for adapter in self.adapters:
            if adapter.can_handle(response):
                return adapter
        return None
    
    def register_adapter(self, adapter: ProviderAdapter):
        """Register a custom adapter"""
        self.adapters.insert(0, adapter)  # Custom adapters take priority


# Global adapter registry
_registry = AdapterRegistry()


def get_adapter_registry() -> AdapterRegistry:
    """Get the global adapter registry"""
    return _registry
