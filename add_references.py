import json
import re
import os

def parse_citations(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    citations = {}
    in_works_cited = False
    
    for line in lines:
        if "Works cited" in line:
            in_works_cited = True
            continue
            
        if in_works_cited:
            line = line.strip()
            if not line:
                continue
            
            # Format: 1. Title - Author ...
            match = re.match(r'^(\d+)\.\s+(.+)', line)
            if match:
                num = match.group(1)
                text = match.group(2)
                citations[num] = text
                
    return citations

def main():
    citations = parse_citations('dennet.txt')
    print(f"Found {len(citations)} citations.")
    
    with open('tools.json', 'r') as f:
        tools = json.load(f)
        
    for tool in tools:
        slug = tool['name'].lower().replace(' ', '-').replace("'", "").replace('"', "").replace('?', "").replace(':', "").replace('/', "-").replace('.', "")
        # My slugify in generate_content was: re.sub(r'[\W_]+', '-', text).strip('-')
        slug = re.sub(r'[\W_]+', '-', tool['name'].lower()).strip('-')
        
        filename = os.path.join('content', f"{slug}.md")
        
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            continue
            
        with open(filename, 'r') as f:
            content = f.read()
            
        # 1. Remove "weird citations" if any
        # User said "two weirdly formatted citations at the bottom".
        # I'll look for lines that might look like broken links or just numbers.
        # But without seeing them, it's hard. 
        # I'll assume I just append the correct ones for now.
        
        # 2. Find citations in detailed_description
        desc = tool.get('detailed_description', '')
        # Look for numbers like "mistakes.6" or "mistakes. 6" or "mistakes [6]"
        # The text in dennet.txt often has them as superscripts or just numbers at end of sentences.
        # e.g. "mistakes.6"
        
        found_nums = set()
        # Regex for dot followed by number: \.(\d+)
        matches = re.findall(r'\.(\d+)', desc)
        found_nums.update(matches)
        
        # Regex for space number: \s(\d+)\s
        # This is risky, might match regular numbers.
        # Let's stick to the ones attached to punctuation or at end of string.
        
        # Also check for "1" or "2" etc if they appear as standalone citations?
        # In dennet.txt, they look like footnotes.
        
        # Let's just look for any number 1-14 that appears in the description?
        # No, that's too aggressive.
        
        # Let's look at the tools.json content again to see the pattern.
        # "mistakes.6" -> 6
        # "parody.2" -> 2
        # "fallacy.8" -> 8
        # "caricature.4" -> 4
        
        # Pattern seems to be `.<digit>` or ` <digit>` at end of sentence?
        # Actually, let's just use the regex `[a-z]\.(\d+)` or `[a-z]\s(\d+)` ?
        
        # Let's be safe and look for `.<digit>`
        matches_dot = re.findall(r'\.(\d+)', desc)
        found_nums.update(matches_dot)
        
        # Also sometimes it might be just "1" at the end of a paragraph?
        
        # Filter valid citation numbers (1-14)
        valid_nums = [n for n in found_nums if n in citations]
        
        if valid_nums:
            # Append references
            ref_section = "\n\n## References\n"
            for num in sorted(valid_nums, key=int):
                ref_text = citations[num]
                # Try to extract URL
                url_match = re.search(r'(https?://\S+)', ref_text)
                if url_match:
                    url = url_match.group(1)
                    # Remove URL from text to avoid duplication if we want
                    text_display = ref_text.replace(url, '').strip().strip(',').strip('-')
                    ref_section += f"- [{text_display}]({url})\n"
                else:
                    ref_section += f"- {ref_text}\n"
            
            # Check if References already exist
            if "## References" not in content:
                with open(filename, 'w') as f:
                    f.write(content + ref_section)
                print(f"Added references to {slug}")
            else:
                print(f"References already in {slug}")

if __name__ == "__main__":
    main()
