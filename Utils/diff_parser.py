import re
from collections import defaultdict

def parse_diff(diff_text):
    """
    Parses a unified diff and summarizes changes per file.
    Replaces '+' with 'Code Added' and '-' with 'Code Removed' for code lines.
    Returns a dict: {filename: [summarized_changes]}
    """
    file_changes = defaultdict(list)
    current_file = None
    for line in diff_text.splitlines():
        if line.startswith('diff --git'):
            match = re.match(r'diff --git a/(.*?) b/(.*?)$', line)
            if match:
                current_file = match.group(2)
        elif current_file and line.startswith('+++'):
            continue  
        elif current_file and line.startswith('---'):
            continue  
        elif current_file and line.startswith('+') and not line.startswith('+++'):
            file_changes[current_file].append(f"Code Added: {line[1:].strip()}")
        elif current_file and line.startswith('-') and not line.startswith('---'):
            file_changes[current_file].append(f"Code Removed: {line[1:].strip()}")
    return dict(file_changes) 