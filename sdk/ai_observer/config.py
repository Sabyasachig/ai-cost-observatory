"""Configuration management for AI Observer SDK"""

import os
from typing import Optional

class Config:
    """Global configuration for AI Observer SDK"""
    
    def __init__(self):
        self.endpoint = os.getenv("AI_OBSERVER_ENDPOINT", "http://localhost:8000")
        self.api_key = os.getenv("AI_OBSERVER_API_KEY", "")
        self.enabled = os.getenv("AI_OBSERVER_ENABLED", "true").lower() == "true"
        self.timeout = int(os.getenv("AI_OBSERVER_TIMEOUT", "5"))
        self.batch_size = int(os.getenv("AI_OBSERVER_BATCH_SIZE", "10"))
        
    def update(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        enabled: Optional[bool] = None,
        timeout: Optional[int] = None,
    ):
        """Update configuration values"""
        if endpoint is not None:
            self.endpoint = endpoint
        if api_key is not None:
            self.api_key = api_key
        if enabled is not None:
            self.enabled = enabled
        if timeout is not None:
            self.timeout = timeout


# Global configuration instance
_config = Config()


def configure(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    enabled: Optional[bool] = None,
    timeout: Optional[int] = None,
):
    """
    Configure AI Observer SDK globally
    
    Args:
        endpoint: Collector API endpoint URL
        api_key: Optional API key for authentication
        enabled: Enable/disable tracking
        timeout: HTTP request timeout in seconds
        
    Example:
        configure(
            endpoint="http://localhost:8000",
            api_key="your-api-key",
            enabled=True
        )
    """
    _config.update(endpoint, api_key, enabled, timeout)


def get_config() -> Config:
    """Get the global configuration instance"""
    return _config
