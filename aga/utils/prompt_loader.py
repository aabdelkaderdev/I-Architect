import os
import re
import yaml
import chevron
from .skill_loader import load_skill_content

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

def load_prompt(template_name: str, context: dict, prompts_dir: str = None, skills_dir: str = None) -> str:
    """
    Loads a mustache prompt template, injects skill references, validates context variables, 
    and renders the template using chevron.
    """
    # Set default paths if not provided
    if prompts_dir is None:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompts_dir = os.path.join(base_path, "prompts")
        
    if skills_dir is None:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        skills_dir = os.path.join(base_path, "Skills")

    if not template_name.endswith(".md"):
        template_name += ".md"
        
    template_path = os.path.join(prompts_dir, template_name)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Prompt template not found: {template_path}")
        
    frontmatter, body = parse_markdown_with_frontmatter(template_path)
    
    # Validate context variables against frontmatter
    if "variables" in frontmatter and isinstance(frontmatter["variables"], list):
        expected_vars = [v["name"] for v in frontmatter["variables"] if "name" in v]
        missing_vars = [v for v in expected_vars if v not in context]
        if missing_vars:
            raise ValueError(f"Missing required context variables for {template_name}: {', '.join(missing_vars)}")

    # Make a copy of context to avoid modifying the input
    render_context = dict(context)

    # Process {{! skill: <tag> as <key> }} directives
    skill_pattern = re.compile(r"\{\{!\s*skill:\s*([^\s]+)\s+as\s+([^\s}]+)\s*\}\}")
    
    # Find all matches
    matches = skill_pattern.finditer(body)
    
    for match in matches:
        tag = match.group(1)
        key = match.group(2)
        
        # Load skill content and add to render context
        skill_content = load_skill_content(skills_dir, tag)
        render_context[key] = skill_content
        
    # Remove the directives from the body so they don't appear in the rendered output
    body = skill_pattern.sub("", body)
    
    # Render using chevron
    return chevron.render(body, render_context)
