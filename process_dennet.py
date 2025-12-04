import re
import json
import os

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
            # Fields: Number, Name, Category, Short Description, Practical Exercise, iOS App Possible?
            
            for i in range(data_start, len(lines)):
                line = lines[i].strip()
                if not line:
                    continue
                
                # Check if it's a number (start of new tool)
                # But "iOS App Possible?" values are Y/N/Maybe, so they won't be numbers usually.
                # However, the field_idx should track it.
                
                if field_idx == 0:
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
    
    # Convert to list and sort by number
    tools_list = []
    for k, v in tools.items():
        try:
            v['sort_num'] = int(k)
        except:
            v['sort_num'] = 999
        tools_list.append(v)
    
    tools_list.sort(key=lambda x: x['sort_num'])
    
    with open('tools.json', 'w') as f:
        json.dump(tools_list, f, indent=2)
    
    print(f"Processed {len(tools_list)} tools.")

if __name__ == "__main__":
    main()
