import re
from typing import List, Dict

def parse_c4_plantuml(puml_string: str) -> List[Dict[str, str]]:
    """
    Parses a PlantUML string to extract C4 macros (System, Container, Component, Person, etc.)
    and their aliases.
    
    Ignores comment lines starting with `'`.
    
    Returns a list of dictionaries with 'type' and 'alias'.
    """
    entities = []
    
    if not puml_string:
        return entities
        
    # Match standard C4 macros, e.g., System(alias, "Label", ...)
    # Group 1: Macro name (e.g., System, Container, Component)
    # Group 2: Alias name
    # Allow optional _Ext suffix like System_Ext
    pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\(\s*([^,]+?)\s*,', re.MULTILINE)
    
    lines = puml_string.splitlines()
    for line in lines:
        line = line.strip()
        # Ignore comments
        if line.startswith("'"):
            continue
            
        # Optional: We could also skip @startuml / @enduml, but the regex won't match them anyway
        match = pattern.search(line)
        if match:
            macro_type = match.group(1)
            alias = match.group(2).strip('"\'') # Remove quotes if any
            
            # We are only interested in entity macros, not Rel or Layout macros
            if macro_type.startswith("Rel_") or macro_type == "Rel" or macro_type.startswith("Layout_") or macro_type in ["SHOW_PERSON_PORTRAIT", "UpdateElementStyle", "AddElementTag", "SHOW_FLOATING_LEGEND", "HIDE_STEREOTYPE"]:
                continue
                
            entities.append({
                "type": macro_type,
                "alias": alias
            })
            
    return entities
