from fastmcp import FastMCP
from aga.tools.encode_plantuml import encode_plantuml_logic
from aga.tools.fetch_plantuml_png import fetch_plantuml_png_logic

mcp = FastMCP("ArchitectureTools")

@mcp.tool()
def encode_plantuml(puml_code: str) -> str:
    """
    Encodes PlantUML code into a URL by writing it to a temporary file and invoking the local planturl binary.
    """
    return encode_plantuml_logic(puml_code)

@mcp.tool()
def fetch_plantuml_png(encoded_url: str) -> dict:
    """
    Fetches the PNG image from the encoded PlantUML URL.
    Performs a HEAD request pre-check and handles transient network errors with retries.
    """
    return fetch_plantuml_png_logic(encoded_url)

if __name__ == "__main__":
    mcp.run(transport="stdio")
