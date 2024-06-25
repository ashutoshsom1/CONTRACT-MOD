from difflib import ndiff

def highlight_changes(original, updated):
    diff = ndiff(original.splitlines(keepends=True), updated.splitlines(keepends=True))
    html_diff = ''
    for line in diff:
        if line.startswith('+ '):
            html_diff += f'<span style="color:green;">{line[2:]}</span>'
        elif line.startswith('- '):
            html_diff += f'<span style="color:red;">{line[2:]}</span>'
        else:
            html_diff += line[2:]
    return f'<pre>{html_diff}</pre>'
