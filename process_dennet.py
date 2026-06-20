import re
import json
import os

from slugify import slugify


def parse_dennet(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tools = {}
    
    # 1. Parse the Master List (at the end)
    # Find where the table starts
    table_start = -1
    for i, line in enumerate(lines):
        if "Table 1: Master List for CSV Export" in line:
            table_start = i
            break
    
    if table_start != -1:
        # Skip header rows
        # The data seems to start after "iOS App Possible?"
        data_start = -1
        for i in range(table_start, len(lines)):
            if "iOS App Possible?" in lines[i]:
                data_start = i + 1
                break
        
        if data_start != -1:
            current_tool = {}
            field_idx = 0
            # NOTE: This parser is positional and tightly coupled to the exact
            # current layout of dennet.txt: it assumes each tool is exactly six
            # consecutive non-empty lines in this order:
            #   Number, Name, Category, Short Description,
            #   Practical Exercise, iOS App Possible?
            # A single stray blank line or a field that wraps onto multiple
            # lines will shift every subsequent tool by one. If you edit the
            # source text, re-verify the output count (should be 77).
            
            for i in range(data_start, len(lines)):
                line = lines[i].strip()
                if not line:
                    continue

                # The master-list table ends before the bibliography. Without
                # this guard the positional loop keeps consuming lines and
                # mis-parses "Works cited" entries (e.g. "1. ...", "7. ...")
                # as bogus tools. Stop as soon as we leave the table.
                if field_idx == 0:
                    if line.startswith("Works cited"):
                        break
                    # A real tool number is a small integer. Citation lines
                    # look like "1. Intuition Pumps ..."; bail if we see one.
                    if not re.fullmatch(r"\d{1,3}", line):
                        break
                    current_tool['number'] = line
                elif field_idx == 1:
                    current_tool['name'] = line
                elif field_idx == 2:
                    current_tool['category'] = line
                elif field_idx == 3:
                    current_tool['short_description'] = line
                elif field_idx == 4:
                    current_tool['practical_exercise'] = line
                elif field_idx == 5:
                    current_tool['ios_app'] = line
                    # End of tool
                    tools[current_tool['number']] = current_tool
                    current_tool = {}
                    field_idx = -1
                
                field_idx += 1

    # 2. Parse the Detailed Content (the main text)
    # We look for "Tool X: Name"
    # And capture text until the next tool or separator
    
    content_text = "".join(lines[:table_start])
    
    # Regex to find tools
    # Pattern: Tool \d+: .+\n
    tool_pattern = re.compile(r'Tool (\d+):\s*(.+?)\n', re.IGNORECASE)
    
    matches = list(tool_pattern.finditer(content_text))
    
    for i in range(len(matches)):
        match = matches[i]
        tool_num = match.group(1)
        tool_name = match.group(2).strip()
        
        start_pos = match.end()
        if i < len(matches) - 1:
            end_pos = matches[i+1].start()
        else:
            # End of content text
            end_pos = len(content_text)
            
        tool_body = content_text[start_pos:end_pos].strip()
        
        # Extract "Digital Implementation Strategy"
        strategy_split = tool_body.split("Digital Implementation Strategy:")
        
        description = strategy_split[0].strip()
        implementation = ""
        if len(strategy_split) > 1:
            implementation = strategy_split[1].strip()
            # Remove underscores if present at the end
            implementation = implementation.split("________")[0].strip()
        
        if tool_num in tools:
            tools[tool_num]['detailed_description'] = description
            tools[tool_num]['implementation_strategy'] = implementation
        else:
            print(f"Warning: Tool {tool_num} found in text but not in master list?")
            tools[tool_num] = {
                'number': tool_num,
                'name': tool_name,
                'detailed_description': description,
                'implementation_strategy': implementation
            }

    return tools

def main():
    tools = parse_dennet('dennet.txt')

    # Drop any record that never got a detailed description from the main
    # text. A real tool always has one; entries lacking it are parsing
    # artifacts (e.g. stray bibliography lines).
    cleaned = {}
    for k, v in tools.items():
        if not v.get('detailed_description'):
            print(f"Dropping incomplete entry (no detailed description): number={k!r}")
            continue
        cleaned[k] = v
    tools = cleaned

    # Convert to list and sort by number
    tools_list = []
    for k, v in tools.items():
        try:
            v['sort_num'] = int(k)
        except (ValueError, TypeError):
            v['sort_num'] = 999
        tools_list.append(v)
    
    tools_list.sort(key=lambda x: x['sort_num'])

    # Compute the canonical slug once, here, so every downstream consumer
    # (content generation, references, the Next.js site) agrees on it.
    seen_slugs = {}
    for tool in tools_list:
        slug = slugify(tool['name'])
        if slug in seen_slugs:
            print(
                f"Warning: duplicate slug '{slug}' for "
                f"'{tool['name']}' and '{seen_slugs[slug]}'"
            )
        seen_slugs[slug] = tool['name']
        tool['slug'] = slug

    with open('tools.json', 'w') as f:
        json.dump(tools_list, f, indent=2)

    print(f"Processed {len(tools_list)} tools.")

if __name__ == "__main__":
    main()
