import os
import sys
import re

def slugify(text):
    # Strip common prefixes like [New Example]
    text = re.sub(r'^\[[^\]]+\]\s*', '', text)
    # Remove non-alphanumeric/non-space/non-hyphen characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\-]', '', text)
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Strip leading/trailing hyphens
    text = text.strip('-')
    return text

def parse_issue_body(body):
    lines = body.splitlines()
    section_lines = []
    in_section = False
    in_code_block = False
    
    # We look for a line starting with "# 提案される追加用例"
    header_pattern = re.compile(r'^#\s*提案される追加用例', re.IGNORECASE)
    
    for line in lines:
        if header_pattern.match(line):
            in_section = True
            continue
        if in_section:
            # Track code block state to avoid breaking on headers inside code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                
            # If we hit another top-level header and we are NOT inside a code block, stop
            if line.startswith('# ') and not in_code_block:
                break
            section_lines.append(line)
            
    if not in_section:
        raise ValueError("Issue body does not contain a '# 提案される追加用例' section.")
        
    content = '\n'.join(section_lines).strip()
    
    # Strip leading/trailing code block markers if present
    if content.startswith('```'):
        first_newline = content.find('\n')
        if first_newline != -1:
            if content.endswith('```'):
                content = content[first_newline+1:-3].strip()
        
    return content

def validate_example_markdown(content):
    if not re.search(r'^#\s+.+', content):
        raise ValueError("Example markdown must start with a title (e.g., '# 例：...').")
        
    if not re.search(r'^##\s+.*(?:エラー|error)', content, re.MULTILINE | re.IGNORECASE):
        raise ValueError("Example markdown must contain an error section (e.g., '## 1. [エラー入力の例]').")
        
    if not re.search(r'^##\s+.*(?:回答|修正|解決|response|solution)', content, re.MULTILINE | re.IGNORECASE):
        raise ValueError("Example markdown must contain an agent response/solution section (e.g., '## 2. [期待されるエージェントの回答・修正手順]').")
        
    return True

def get_target_skill(labels_str, base_skills_dir):
    if not labels_str:
        raise ValueError("No labels found on the Issue. A label matching the target skill directory name is required.")
        
    # Split labels by comma and strip whitespace
    labels = [l.strip().lower() for l in labels_str.split(',') if l.strip()]
    
    if not os.path.exists(base_skills_dir):
        raise ValueError(f"Skills directory not found at: {base_skills_dir}")
        
    available_skills = []
    for item in os.listdir(base_skills_dir):
        if os.path.isdir(os.path.join(base_skills_dir, item)):
            available_skills.append(item.lower())
            
    # Find matching skill folder from issue labels
    matched_skills = [s for s in available_skills if s in labels]
    
    if not matched_skills:
        raise ValueError(
            f"Could not determine target skill from labels.\n"
            f"Issue labels: {labels}\n"
            f"Available skills in repo: {available_skills}\n"
            f"Please ensure the Issue has a label matching the skill directory name."
        )
        
    if len(matched_skills) > 1:
        raise ValueError(
            f"Multiple matching skill labels found: {matched_skills}.\n"
            f"Please ensure only one skill label is applied to the Issue."
        )
        
    # Find and return the original cased folder name
    for item in os.listdir(base_skills_dir):
        if item.lower() == matched_skills[0]:
            return item
            
    raise ValueError(f"Unexpected error matching skill: {matched_skills[0]}")

def main():
    issue_title = os.environ.get('ISSUE_TITLE', '').strip()
    issue_number = os.environ.get('ISSUE_NUMBER', '').strip()
    issue_body = os.environ.get('ISSUE_BODY', '').strip()
    issue_labels = os.environ.get('ISSUE_LABELS', '').strip()
    
    if not issue_body:
        print("Error: ISSUE_BODY environment variable is empty.", file=sys.stderr)
        sys.exit(1)
        
    try:
        # 1. Determine target skill directory dynamically from labels
        base_skills_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'skills'))
        skill_name = get_target_skill(issue_labels, base_skills_dir)
        
        # 2. Extract and validate content
        content = parse_issue_body(issue_body)
        validate_example_markdown(content)
        
        # 3. Generate filename
        slug = slugify(issue_title)
        if not slug:
            slug = f"issue-{issue_number}"
        filename = f"{slug}.md"
        
        # 4. Resolve output path securely
        dest_dir = os.path.abspath(os.path.join(base_skills_dir, skill_name, 'examples'))
        output_path = os.path.abspath(os.path.join(dest_dir, filename))
        
        # Directory traversal prevention
        if not output_path.startswith(dest_dir):
            raise ValueError("Directory traversal detected!")
            
        # 5. Write to file
        os.makedirs(dest_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content + '\n')
            
        relative_file_path = f"skills/{skill_name}/examples/{filename}"
        print(f"Success: Created example file: {relative_file_path}")
        
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"file_path={relative_file_path}\n")
                f.write(f"file_name={filename}\n")
                
    except ValueError as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        # Print error message to stdout for workflow execution capture
        print(f"ERROR: {e}")
        sys.exit(2)

if __name__ == '__main__':
    main()
