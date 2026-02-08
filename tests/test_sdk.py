"""
Test suite for AI Cost Observatory SDK
"""

import pytest
from unittest.mock import Mock, patch
from ai_observer import observe, log_event, configure
from ai_observer.adapters import OpenAIAdapter, AnthropicAdapter


class TestConfiguration:
    """Test configuration management"""
    
    def test_configure(self):
        """Test configuration"""
        configure(
            endpoint="http://test:8000",
            api_key="test-key",
            enabled=True,
        )
        
        from ai_observer.config import get_config
        config = get_config()
        
        assert config.endpoint == "http://test:8000"
        assert config.api_key == "test-key"
        assert config.enabled is True


class TestOpenAIAdapter:
    """Test OpenAI adapter"""
    
    def test_extract_usage(self):
        """Test usage extraction"""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.model = "gpt-4o-mini"
        mock_response.usage = Mock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.usage.total_tokens = 150
        
        adapter = OpenAIAdapter()
        usage = adapter.extract_usage(mock_response)
        
        assert usage["model"] == "gpt-4o-mini"
        assert usage["prompt_tokens"] == 100
        assert usage["completion_tokens"] == 50
        assert usage["total_tokens"] == 150
    
    def test_extract_cost(self):
        """Test cost calculation"""
        adapter = OpenAIAdapter()
        usage = {
            "prompt_tokens": 1000,
            "completion_tokens": 500,
        }
        
        cost = adapter.extract_cost(usage, "gpt-4o-mini")
        
        # gpt-4o-mini: $0.150/1M input, $0.600/1M output
        expected_input = (1000 / 1_000_000) * 0.150
        expected_output = (500 / 1_000_000) * 0.600
        
        assert cost["input_cost"] == round(expected_input, 6)
        assert cost["output_cost"] == round(expected_output, 6)
        assert cost["total_cost"] == round(expected_input + expected_output, 6)
        assert cost["currency"] == "USD"
    
    def test_can_handle(self):
        """Test response detection"""
        mock_response = Mock()
        mock_response.model = "gpt-4o"
        mock_response.usage = Mock()
        
        adapter = OpenAIAdapter()
        assert adapter.can_handle(mock_response) is True
        
        # Test with invalid response
        invalid_response = Mock(spec=[])
        assert adapter.can_handle(invalid_response) is False


class TestAnthropicAdapter:
    """Test Anthropic adapter"""
    
    def test_extract_usage(self):
        """Test usage extraction"""
        mock_response = Mock()
        mock_response.model = "claude-3-5-sonnet"
        mock_response.usage = Mock()
        mock_response.usage.input_tokens = 200
        mock_response.usage.output_tokens = 100
        
        adapter = AnthropicAdapter()
        usage = adapter.extract_usage(mock_response)
        
        assert usage["model"] == "claude-3-5-sonnet"
        assert usage["prompt_tokens"] == 200
        assert usage["completion_tokens"] == 100
        assert usage["total_tokens"] == 300


class TestObservationContext:
    """Test observation context manager"""
    
    @patch('ai_observer.core.requests.post')
    def test_observe_context(self, mock_post):
        """Test observe context manager"""
        mock_post.return_value = Mock(status_code=200)
        
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.model = "gpt-4o-mini"
        mock_response.usage = Mock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.usage.total_tokens = 150
        
        with observe(
            project="test-project",
            agent="test-agent",
            tags={"env": "test"}
        ) as obs:
            obs.track_response(mock_response)
        
        # Verify API call was made
        assert mock_post.called
        call_args = mock_post.call_args
        assert "events" in call_args[0][0]


class TestLogEvent:
    """Test manual event logging"""
    
    @patch('ai_observer.core.requests.post')
    def test_log_event(self, mock_post):
        """Test manual event logging"""
        mock_post.return_value = Mock(status_code=200)
        
        log_event(
            model="gpt-4o",
            prompt_tokens=200,
            completion_tokens=100,
            project="test",
            agent="manual",
        )
        
        assert mock_post.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
