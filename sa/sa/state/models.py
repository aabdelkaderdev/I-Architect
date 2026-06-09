from typing import TypedDict, Optional, List, Dict
from pydantic import BaseModel, Field

class LLMEvaluationResult(BaseModel):
    score: int = Field(ge=0, le=10, description="Evaluation score from 0 to 10")
    reasoning: str = Field(description="Explanation of the evaluation")

class AttributeAssessment(TypedDict):
    attribute: str
    scenario: str
    mechanistic_justification: str
    points_awarded: int

class SAAMEvaluationResult(BaseModel):
    score: int = Field(ge=0, le=30, description="Total evaluation score from 0 to 30")
    reasoning: str = Field(description="Overall explanation of the SAAM evaluation")
    attribute_assessments: List[Dict] = Field(description="Detailed assessments of each quality attribute")

class ExecutiveSummaryResult(BaseModel):
    markdown: str = Field(description="Full executive summary narrative in Markdown format. Must reference actual scores and percentages.")
    key_findings: List[str] = Field(description="List of exactly 3-5 concise findings, each under 25 words.", min_length=3, max_length=5)
    overall_grade: str = Field(description="The overall letter grade (A, B, C, D, or F).")

class Penalty(TypedDict):
    reason: str
    points: float
    requirement_id: Optional[str]

class AxisScore(TypedDict):
    awarded: float
    possible: int
    sub_scores: Dict[str, float]
    llm_reasoning: Optional[str]
    penalties_applied: List[Penalty]

class ReportSummary(TypedDict):
    total_score: float
    grade: str
    requirements_total: int
    requirements_asr: int
    requirements_functional: int
    requirements_orphaned: int
    diagrams_present: int

class OrphanedRequirement(TypedDict):
    req_id: str
    is_asr: bool
    text_snippet: str

class DiagramIssue(TypedDict):
    diagram_type: str
    issue_type: str
    entity_id: Optional[str]
    description: str

class GapAnalysis(TypedDict):
    orphaned_requirements: List[OrphanedRequirement]
    diagram_issues: List[DiagramIssue]

class ExecutiveSummary(TypedDict):
    markdown: str
    key_findings: List[str]
    overall_grade: str

class AxisBreakdown(TypedDict):
    functional: AxisScore
    asr_coverage: AxisScore
    saam_diagrams: AxisScore

class ScoringReport(TypedDict):
    schema_version: str
    report_id: str
    generated_at: str
    pipeline_run_id: str
    summary: ReportSummary
    axis_scores: AxisBreakdown
    gap_analysis: GapAnalysis
    executive_summary: ExecutiveSummary
