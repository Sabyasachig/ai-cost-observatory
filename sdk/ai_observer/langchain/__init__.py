"""LangChain integration for AI Cost Observatory"""

from typing import Any, Dict, Optional, List
import time

try:
    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import LLMResult
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseCallbackHandler = object

from ..core import log_event


class CostCallback(BaseCallbackHandler):
    """LangChain callback for tracking costs"""
    
    def __init__(
        self,
        project: str,
        agent: Optional[str] = None,
        step: Optional[str] = None,
        user_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        endpoint: Optional[str] = None,
    ):
        """
        Initialize the cost callback
        
        Args:
            project: Project name
            agent: Agent name
            step: Step name
            user_id: User ID
            tags: Additional tags
            endpoint: Custom endpoint
            
        Example:
            from ai_observer.langchain import CostCallback
            from langchain.chat_models import ChatOpenAI
            
            callback = CostCallback(project="rag-app", agent="planner")
            llm = ChatOpenAI(callbacks=[callback])
            llm.invoke("Explain vector databases")
        """
        super().__init__()
        self.project = project
        self.agent = agent
        self.step = step
        self.user_id = user_id
        self.tags = tags or {}
        self.endpoint = endpoint
        self.start_time = None
        
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running"""
        self.start_time = time.time()
        
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running"""
        if not self.start_time:
            return
            
        latency_ms = int((time.time() - self.start_time) * 1000)
        
        # Extract usage from LangChain response
        for generation in response.generations:
            if generation and len(generation) > 0:
                gen = generation[0]
                
                # Try to get token usage from generation info
                if hasattr(gen, 'generation_info') and gen.generation_info:
                    usage = gen.generation_info.get('token_usage', {})
                    model = gen.generation_info.get('model_name', 'unknown')
                    
                    prompt_tokens = usage.get('prompt_tokens', 0)
                    completion_tokens = usage.get('completion_tokens', 0)
                    
                    if prompt_tokens > 0 or completion_tokens > 0:
                        log_event(
                            model=model,
                            prompt_tokens=prompt_tokens,
                            completion_tokens=completion_tokens,
                            latency_ms=latency_ms,
                            project=self.project,
                            agent=self.agent,
                            step=self.step,
                            user_id=self.user_id,
                            tags=self.tags,
                            endpoint=self.endpoint,
                        )
        
        # Also check llm_output for aggregate usage
        if hasattr(response, 'llm_output') and response.llm_output:
            usage = response.llm_output.get('token_usage', {})
            model = response.llm_output.get('model_name', 'unknown')
            
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            
            if prompt_tokens > 0 or completion_tokens > 0:
                log_event(
                    model=model,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    latency_ms=latency_ms,
                    project=self.project,
                    agent=self.agent,
                    step=self.step,
                    user_id=self.user_id,
                    tags=self.tags,
                    endpoint=self.endpoint,
                )


if not LANGCHAIN_AVAILABLE:
    class CostCallback:
        """Dummy class when LangChain is not available"""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain is not installed. Install it with: "
                "pip install ai-cost-observatory[langchain]"
            )
