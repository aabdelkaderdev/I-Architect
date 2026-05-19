import json
import sqlite3
from pathlib import Path
import pytest

from raa.state.types import (
    ArchFragment, ArchSystem, ArchContainer, ArchComponent,
    ArchRelationship, ArchPattern, ArchPerson, ArchExternalSystem,
    ArchModel
)

# =============================================================================
# T002 — FakeChatModel conforming to BaseChatModel interface
# =============================================================================

class FakeChatResponse:
    def __init__(self, content):
        self.content = content

try:
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.outputs import ChatResult, ChatGeneration
    from langchain_core.messages import AIMessage

    class FakeChatModel(BaseChatModel):
        responses: dict = {}
        calls: list = []

        def __init__(self, responses=None):
            super().__init__()
            self.responses = responses or {}
            self.calls = []

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            prompt = ""
            if isinstance(messages, str):
                prompt = messages
            elif isinstance(messages, list):
                prompt = "\n".join(m.content if hasattr(m, "content") else str(m) for m in messages)
            else:
                prompt = str(messages)
            self.calls.append(prompt)

            content = "{}"
            for pattern, response in self.responses.items():
                if pattern in prompt:
                    if isinstance(response, dict):
                        content = json.dumps(response)
                    else:
                        content = str(response)
                    break
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

        @property
        def _llm_type(self) -> str:
            return "fake-chat-model"
except ImportError:
    class FakeChatModel:
        def __init__(self, responses=None):
            self.responses = responses or {}
            self.calls = []

        def invoke(self, prompt, **kwargs):
            self.calls.append(str(prompt))
            content = "{}"
            for pattern, response in self.responses.items():
                if pattern in str(prompt):
                    if isinstance(response, dict):
                        content = json.dumps(response)
                    else:
                        content = str(response)
                    break
            return FakeChatResponse(content)


# =============================================================================
# T003 — mock_arlo_output fixture
# =============================================================================

@pytest.fixture
def mock_arlo_output():
    """Returns a valid ARLOOutput dictionary payload."""
    asrs = [
        {"id": 1, "text": "The system must process payments securely."},
        {"id": 2, "text": "The database must handle up to 1000 requests per second."},
        {"id": 3, "text": "Users must receive email notifications upon registration."},
        {"id": 4, "text": "The system must maintain an audit log of all transactions."},
        {"id": 5, "text": "Administrators must be able to revoke user permissions."}
    ]
    non_asrs = [
        {"id": 10, "text": "The logo should be displayed on the top left of the dashboard."},
        {"id": 11, "text": "Exported reports should support CSV format."},
        {"id": 12, "text": "The user interface should load within 2 seconds."},
        {"id": 13, "text": "Standard users must log in via a web portal."},
        {"id": 14, "text": "The system must support dark mode styling."},
        {"id": 15, "text": "Password reset link must expire after 24 hours."},
        {"id": 16, "text": "Help documentation must be accessible from the footer."},
        {"id": 17, "text": "The system must send SMS reminders for appointments."},
        {"id": 18, "text": "User profile pictures must be cropped automatically."},
        {"id": 19, "text": "System health indicators must be visible on the admin console."}
    ]
    condition_groups = [
        {"id": 1, "requirement_ids": [1, 2, 4]},
        {"id": 2, "requirement_ids": [3, 5]}
    ]
    quality_weights = {
        "security": 5,
        "performance": 4,
        "maintainability": 3
    }
    return {
        "asrs": asrs,
        "non_asr": non_asrs,
        "condition_groups": condition_groups,
        "quality_weights": quality_weights
    }


# =============================================================================
# T004 — mock_arch_fragment fixture
# =============================================================================

@pytest.fixture
def mock_arch_fragment():
    """Returns a simulated ArchFragment matching Section 4 schemas."""
    return ArchFragment(
        systems=[
            ArchSystem(id="sys_a", label="System A", description="Primary system under design", source_fragment="raa_a")
        ],
        containers=[
            ArchContainer(id="cont_a", label="Container A", description="Web portal container", parent_system_id="sys_a", source_fragment="raa_a"),
            ArchContainer(id="cont_b", label="Container B", description="Database storage container", parent_system_id="sys_a", source_fragment="raa_a")
        ],
        components=[
            ArchComponent(id="comp_a1", label="Component A1", description="Auth component", parent_container_id="cont_a", source_fragment="raa_a"),
            ArchComponent(id="comp_a2", label="Component A2", description="API component", parent_container_id="cont_a", source_fragment="raa_a"),
            ArchComponent(id="comp_b1", label="Component B1", description="SQL store component", parent_container_id="cont_b", source_fragment="raa_a")
        ],
        persons=[
            ArchPerson(id="user_a", label="User A", description="Standard customer", source_fragment="raa_a")
        ],
        external_systems=[
            ArchExternalSystem(id="ext_payment", label="Payment Gateway", description="Third party service", source_fragment="raa_a")
        ],
        relationships=[
            ArchRelationship(source_id="user_a", target_id="sys_a", interaction_type="interacts with", diagram_scope="context", source_fragment="raa_a"),
            ArchRelationship(source_id="cont_a", target_id="cont_b", interaction_type="reads/writes", diagram_scope="container", source_fragment="raa_a"),
            ArchRelationship(source_id="comp_a2", target_id="comp_b1", interaction_type="queries", diagram_scope="component", source_fragment="raa_a")
        ],
        patterns=[
            ArchPattern(name="Microservices", rationale="Required scalability", quality_attributes=["scalability"])
        ],
        rationale={"overall": "Standard C4 pattern"}
    )


# =============================================================================
# T005 — mock_sqlite_db fixture
# =============================================================================

@pytest.fixture
def mock_sqlite_db(tmp_path):
    """Creates isolated asr_embeddings.db and non_asr_embeddings.db with correct schema."""
    asr_db = tmp_path / "asr_embeddings.db"
    non_asr_db = tmp_path / "non_asr_embeddings.db"
    
    for db_path in (asr_db, non_asr_db):
        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS embeddings ("
            "  requirement_id INTEGER PRIMARY KEY,"
            "  embedding BLOB NOT NULL,"
            "  text_hash TEXT NOT NULL,"
            "  model_name TEXT NOT NULL"
            ")"
        )
        conn.commit()
        conn.close()
    return asr_db, non_asr_db


# =============================================================================
# T007 — assert_c4_structural_integrity helper
# =============================================================================

def assert_c4_structural_integrity(model: ArchModel):
    """Enforces nested hierarchy, no cross-level ID reuse, and matching scopes."""
    from raa.nodes.final_merge import validate_c4_model
    errors = validate_c4_model(model)
    assert not errors, f"C4 structural integrity errors found:\n" + "\n".join(errors)


# =============================================================================
# T008 & T009 — golden_model fixtures
# =============================================================================

@pytest.fixture
def golden_model_data():
    """Loads the static golden model JSON file."""
    fixture_path = Path(__file__).parent / "fixtures" / "golden_model.json"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def golden_arch_model(golden_model_data):
    """Converts golden_model_data dictionary into a typed ArchModel instance."""
    from raa.state.serialization import dict_to_dataclass
    return dict_to_dataclass(golden_model_data, ArchModel)


# =============================================================================
# T007 & T008 — Shared build helpers
# =============================================================================

def build_test_batch(requirements: list[dict], group_id: int = 1, centroid: list[float] | None = None, batch_id: int = 0) -> dict:
    """Constructs a synthetic batch dict from requirements."""
    req_ids = [str(r.get("id")) for r in requirements]
    return {
        "batch_id": batch_id,
        "group_id": group_id,
        "requirement_ids": req_ids,
        "group_centroid": centroid,
        "reduced_confidence": False,
        "requirements": requirements,
        "similarity_scores": {rid: 1.0 for rid in req_ids},
        "non_asr_candidates": [],
        "coherence_score": 1.0,
        "is_split": False,
        "sorting_metadata": {"score": 1.0, "strategy": "default", "tie_breaker": "none"}
    }


def build_running_arch_model(spec: dict) -> ArchModel:
    """Constructs a hierarchical ArchModel from a simplified dict specification."""
    systems = []
    for s_dict in spec.get("systems", []):
        containers = []
        for c_dict in s_dict.get("containers", []):
            components = []
            for comp_dict in c_dict.get("components", []):
                comp = ArchComponent(
                    id=comp_dict["id"],
                    label=comp_dict.get("label", comp_dict["id"]),
                    description=comp_dict.get("description", ""),
                    parent_container_id=c_dict["id"]
                )
                components.append(comp)
            cont = ArchContainer(
                id=c_dict["id"],
                label=c_dict.get("label", c_dict["id"]),
                description=c_dict.get("description", ""),
                parent_system_id=s_dict["id"],
                components=components
            )
            containers.append(cont)
        sys = ArchSystem(
            id=s_dict["id"],
            label=s_dict.get("label", s_dict["id"]),
            description=s_dict.get("description", ""),
            containers=containers
        )
        systems.append(sys)

    persons = [
        ArchPerson(
            id=p_dict["id"],
            label=p_dict.get("label", p_dict["id"]),
            description=p_dict.get("description", "")
        )
        for p_dict in spec.get("persons", [])
    ]

    external_systems = [
        ArchExternalSystem(
            id=e_dict["id"],
            label=e_dict.get("label", e_dict["id"]),
            description=e_dict.get("description", "")
        )
        for e_dict in spec.get("external_systems", [])
    ]

    # Route relationships to correct nesting
    model = ArchModel(
        systems=systems,
        persons=persons,
        external_systems=external_systems
    )

    from raa.nodes.final_merge import _assemble_tree
    # Prepare a flat list of relationships and then assemble
    rels = []
    for r_dict in spec.get("relationships", []):
        rels.append(
            ArchRelationship(
                source_id=r_dict["source_id"],
                target_id=r_dict["target_id"],
                interaction_type=r_dict["interaction_type"],
                technology=r_dict.get("technology"),
                diagram_scope=r_dict.get("diagram_scope", "context")
            )
        )
    # Assemble tree uses a flat ArchFragment style, then distributes relationships
    flat_frag = ArchFragment(
        systems=systems,
        containers=[c for s in systems for c in s.containers],
        components=[comp for s in systems for c in s.containers for comp in c.components],
        persons=persons,
        external_systems=external_systems,
        relationships=rels
    )
    assembled = _assemble_tree(flat_frag)
    model.systems = assembled.systems
    model.persons = assembled.persons
    model.external_systems = assembled.external_systems

    return model

