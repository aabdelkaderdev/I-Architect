import urllib.request
import urllib.error
import time

def fetch_plantuml_png_logic(encoded_url: str) -> dict:
    base_url = encoded_url.split("/png/")[0] if "/png/" in encoded_url else "http://www.plantuml.com/plantuml"
    
    try:
        req = urllib.request.Request(base_url, method="HEAD")
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status >= 400:
                return {"error": f"PlantUML server base URL returned status {response.status}"}
    except Exception as e:
        return {"error": f"PlantUML server base URL HEAD request failed: {str(e)}"}
        
    max_retries = 2
    retry_delay = 1.0
    
    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(encoded_url)
            with urllib.request.urlopen(req, timeout=30) as response:
                image_bytes = response.read()
                
                if "/png/" in encoded_url:
                    svg_url = encoded_url.replace("/png/", "/svg/")
                    try:
                        svg_req = urllib.request.Request(svg_url)
                        with urllib.request.urlopen(svg_req, timeout=10) as svg_resp:
                            svg_content = svg_resp.read().decode('utf-8', errors='ignore')
                            if "Syntax Error?" in svg_content or "class=\"error\"" in svg_content or "<text" in svg_content and "error" in svg_content.lower():
                                return {
                                    "error": "PlantUML Syntax Error",
                                    "details": "The generated SVG indicates a syntax error in the PlantUML code.",
                                    "svg_content": svg_content[:500]
                                }
                    except Exception:
                        pass
                        
                return {"image_bytes": image_bytes}
                
        except urllib.error.URLError as e:
            if attempt == max_retries:
                return {"error": f"Failed to fetch PlantUML PNG after {max_retries} retries. {str(e)}"}
            time.sleep(retry_delay)
            retry_delay *= 2
        except Exception as e:
            return {"error": f"Unexpected failure during GET request: {str(e)}"}
    
    return {"error": "Unknown failure in fetch_plantuml_png"}

from langchain.tools import tool

@tool
def fetch_plantuml_png(encoded_url: str) -> dict:
    """
    Fetches the PNG image from the encoded PlantUML URL.
    Performs a HEAD request pre-check and handles transient network errors with retries.
    """
    return fetch_plantuml_png_logic(encoded_url)
