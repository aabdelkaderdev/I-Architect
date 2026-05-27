import subprocess
import tempfile
import os
from aga.tools.os_detection import get_planturl_binary_path

def encode_plantuml_logic(puml_code: str) -> str:
    tmp_path = None
    try:
        binary_path = get_planturl_binary_path()
        
        fd, tmp_path = tempfile.mkstemp(suffix=".puml")
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(puml_code)
            
        server_url = "http://www.plantuml.com/plantuml"
            
        cmd = [
            binary_path,
            "-s", tmp_path,
            "-u", server_url,
            "-t", "png",
            "-c", "deflate"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    
    except subprocess.CalledProcessError as e:
        return f"Error: planturl binary execution failed with exit code {e.returncode}. stderr: {e.stderr}"
    except Exception as e:
        return f"Error: Failed to encode PlantUML code. Details: {str(e)}"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass

from langchain.tools import tool

@tool
def encode_plantuml(puml_code: str) -> str:
    """
    Encodes PlantUML code into a URL by writing it to a temporary file and invoking the local planturl binary.
    """
    return encode_plantuml_logic(puml_code)
