## 1. Schema & Model Setup

- [x] 1.1 Add `ExecutiveSummaryResult` Pydantic `BaseModel` to `sa/state/models.py` with fields: `markdown` (str, Field description), `key_findings` (list[str], Field description + constraints), `overall_grade` (str, Field description)
- [x] 1.2 Create `sa/prompts/executive_summary.md` template with `str.format()` placeholders (`{total_score}`, `{grade}`, `{axis1_summary}`, `{axis2_summary}`, `{axis3_summary}`, `{orphaned_requirements}`, `{diagram_issues}`) — matching the format pattern in `saam_validation.md`

## 2. LLM Integration

- [x] 2.1 Add `generate_executive_summary_with_llm(prompt_text)` to `sa/utils/llm.py` following the existing pattern: `init_chat_model` → `model.with_structured_output(ExecutiveSummaryResult)` → `structured_model.invoke([HumanMessage(content=prompt_text)])`
- [x] 2.2 Add fallback return in the except block: `ExecutiveSummaryResult(markdown="..stub..", key_findings=["Executive summary generation failed..."], overall_grade=grade)`

## 3. Node 5 Integration

- [x] 3.1 Update `sa/nodes/report.py` to read and format `sa/prompts/executive_summary.md` with actual score data
- [x] 3.2 Call `generate_executive_summary_with_llm()` and populate the `executive_summary` dict in `ScoringReport` from the result
- [x] 3.3 Replace `os.makedirs(output_path, exist_ok=True)` with directory existence/writability validation (raise `FileNotFoundError` / `PermissionError`)
- [x] 3.4 Compose full `scoring_report.md` content (executive summary + score breakdown table + key findings + gap analysis highlights)

## 4. Testing & Validation

- [x] 4.1 Test happy path end-to-end (all nodes through Node 5 output)
- [x] 4.2 Test error handling for missing/unwritable output directories
- [x] 4.3 Test LLM fallback behavior (e.g., by simulating an exception in the LLM call)
- [x] 4.4 Verify grade boundaries match the scoring rubric exactly (59.9→F, 60.0→D, etc.)
- [x] 4.5 Verify `scoring_report.json` schema and `scoring_report.md` content are well-formed
