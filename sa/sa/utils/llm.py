from typing import Optional
import os
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from sa.state.models import LLMEvaluationResult, SAAMEvaluationResult, ExecutiveSummaryResult

def evaluate_with_llm(prompt_text: str, model_name: str = "gpt-4o", provider: str = "openai") -> LLMEvaluationResult:
    try:
        # Respect environment variables if present
        env_model = os.environ.get("SA_EVAL_MODEL", model_name)
        env_provider = os.environ.get("SA_EVAL_PROVIDER", provider)
        
        model = init_chat_model(env_model, model_provider=env_provider, temperature=0.0)
        structured_model = model.with_structured_output(LLMEvaluationResult)
        
        result = structured_model.invoke([HumanMessage(content=prompt_text)])
        return result
    except Exception as e:
        return LLMEvaluationResult(
            score=0,
            reasoning=f"LLM evaluation failed: {str(e)}"
        )

def evaluate_saam_with_llm(prompt_text: str, model_name: str = "gpt-4o", provider: str = "openai") -> SAAMEvaluationResult:
    try:
        # Respect environment variables if present
        env_model = os.environ.get("SA_EVAL_MODEL", model_name)
        env_provider = os.environ.get("SA_EVAL_PROVIDER", provider)
        
        model = init_chat_model(env_model, model_provider=env_provider, temperature=0.0)
        # Using auto-strategy selection by passing the Pydantic model directly
        structured_model = model.with_structured_output(SAAMEvaluationResult)
        
        result = structured_model.invoke([HumanMessage(content=prompt_text)])
        return result
    except Exception as e:
        return SAAMEvaluationResult(
            score=0,
            reasoning=f"LLM evaluation failed: {str(e)}",
            attribute_assessments=[]
        )

def generate_executive_summary_with_llm(prompt_text: str, grade: str, model_name: str = "gpt-4o", provider: str = "openai") -> ExecutiveSummaryResult:
    try:
        env_model = os.environ.get("SA_EVAL_MODEL", model_name)
        env_provider = os.environ.get("SA_EVAL_PROVIDER", provider)
        
        model = init_chat_model(env_model, model_provider=env_provider, temperature=0.0)
        structured_model = model.with_structured_output(ExecutiveSummaryResult)
        
        result = structured_model.invoke([HumanMessage(content=prompt_text)])
        return result
    except Exception as e:
        return ExecutiveSummaryResult(
            markdown=f"## Executive Summary\n\nExecutive summary generation failed.\n\nError details: {str(e)}",
            key_findings=[
                "Executive summary generation failed.",
                "See scoring_report.json for full data.",
                "Please check LLM connectivity or credentials."
            ],
            overall_grade=grade
        )
