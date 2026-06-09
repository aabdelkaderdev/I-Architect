from pydantic import BaseModel, ConfigDict, Field
from langchain_core.language_models.chat_models import BaseChatModel


class AGAConfig(BaseModel):
    """Runtime configuration for the AGA subgraph.

    The Orchestrator constructs one AGAConfig and passes it to build_graph.
    All nodes receive configuration exclusively through this object.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    llm: BaseChatModel = Field(
        description=(
            "Pre-constructed LangChain BaseChatModel instance. "
            "The Orchestrator owns model construction, provider selection, "
            "and all provider-specific options (temperature, timeout, etc.)."
        ),
    )

    max_retries: int = Field(
        default=5,
        ge=1,
        description=(
            "Maximum render attempts per diagram. Once this many "
            "render_plantuml_tool calls have occurred for a diagram, "
            "it is recorded as failed and the queue advances."
        ),
    )

    plantuml_base_url: str = Field(
        default="https://www.plantuml.com/plantuml",
        min_length=1,
        description="Base URL of the PlantUML rendering server.",
    )

    output_dir: str = Field(
        default="aga/output",
        min_length=1,
        description=(
            "Filesystem directory for rendered PNGs and metadata sidecars. "
            "Created at startup if it does not exist (deferred to Phase 6)."
        ),
    )
