from dataclasses import dataclass

@dataclass
class AGAConfig:
    """Runtime configuration for the Architecture Generation Agent."""
    checkpoint_db_path: str
    output_dir_png: str
    output_dir_puml: str
    output_dir_diagrams: str
    max_retries: int = 5
    plantuml_server_url: str = "http://www.plantuml.com/plantuml"
    read_timeout_seconds: int = 30
