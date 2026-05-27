import os
import re
import yaml

def parse_markdown_with_frontmatter(file_path: str):
    """Parses a markdown file with YAML frontmatter."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract frontmatter
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_yaml = match.group(1)
    body = match.group(2)
    try:
        frontmatter = yaml.safe_load(frontmatter_yaml)
    except yaml.YAMLError:
        frontmatter = {}
        
    return frontmatter, body

def parse_skill_manifest(skill_dir: str):
    """Parses SKILL.md to extract the tag registry."""
    skill_file = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_file):
        raise FileNotFoundError(f"Skill manifest not found at {skill_file}")

    frontmatter, body = parse_markdown_with_frontmatter(skill_file)
    
    # We expect a markdown table for the tag registry
    # | Tag | Reference File | Section | Description |
    # | `c4:rules` | `references/c4.md` | Rules | ...
    
    registry = {}
    
    # Parse markdown table
    lines = body.split("\n")
    in_table = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("|") and "Tag" in line and "Reference File" in line:
            in_table = True
            continue
        if in_table and line.startswith("|") and "---" in line:
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")][1:-1]
            if len(parts) >= 3:
                tag = parts[0].replace("`", "").strip()
                ref_file = parts[1].replace("`", "").strip()
                section = parts[2].replace("`", "").strip()
                registry[tag] = {
                    "file": ref_file,
                    "section": section
                }
        elif in_table and not line.startswith("|"):
            in_table = False
            
    return registry

def extract_section(file_path: str, section_name: str) -> str:
    """Extracts a specific heading section from a markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find heading matching section_name (e.g. # Rules or ## Rules)
    heading_pattern = re.compile(r"^(#+)\s+" + re.escape(section_name) + r"\s*$", re.MULTILINE)
    match = heading_pattern.search(content)
    
    if not match:
        raise KeyError(f"Section '{section_name}' not found in {file_path}")
        
    start_pos = match.end()
    heading_level = len(match.group(1))
    
    # Find next heading of same or higher level (fewer #s)
    next_heading_pattern = re.compile(r"^#{1," + str(heading_level) + r"}\s+.*$", re.MULTILINE)
    next_match = next_heading_pattern.search(content, start_pos)
    
    if next_match:
        end_pos = next_match.start()
        return content[start_pos:end_pos].strip()
    else:
        return content[start_pos:].strip()

def load_skill_content(skill_dir: str, tag: str) -> str:
    """
    Resolves a skill tag to its reference file section content.
    Raises KeyError if tag is not found in manifest or section is not found.
    """
    registry = parse_skill_manifest(skill_dir)
    
    if tag not in registry:
        raise KeyError(f"Skill tag '{tag}' not found in skill manifest at {skill_dir}")
        
    tag_info = registry[tag]
    ref_file_path = os.path.join(skill_dir, tag_info["file"])
    
    if not os.path.exists(ref_file_path):
        raise FileNotFoundError(f"Reference file not found: {ref_file_path}")
        
    return extract_section(ref_file_path, tag_info["section"])
