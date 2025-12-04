import os
import re

def clean_content(content):
    # 1. Remove "## References" section and everything after it
    if "## References" in content:
        content = content.split("## References")[0].strip()
        
    # 2. Remove lines that look like the "junk" user reported
    # Examples:
    # #Works cited
    # 2. IntuitionPumpsAndOtherToolsfor...
    # #6. Intuition Pumps...
    
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Check for specific junk patterns
        if line.strip().startswith('#Works cited'):
            continue
        if "IntuitionPumpsAndOtherToolsfor" in line:
            continue
        if "accessed November 28, 2025" in line:
            continue
        if re.match(r'^#?\d+\.\s+Intuition', line.strip()):
            continue
        if re.match(r'^#?\d+\.\s+Daniel Dennett', line.strip()):
            continue
            
        cleaned_lines.append(line)
        
    return '\n'.join(cleaned_lines).strip() + '\n'

def main():
    content_dir = 'content'
    for filename in os.listdir(content_dir):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(content_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            
        new_content = clean_content(content)
        
        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Cleaned {filename}")

if __name__ == "__main__":
    main()
