import json
import os
import re
import time
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:latest"
CONTENT_DIR = "content"

def slugify(text):
    text = text.lower()
    return re.sub(r'[\W_]+', '-', text).strip('-')

def generate_content(tool):
    prompt = f"""
    You are an expert on Daniel Dennett's philosophy and his book "Intuition Pumps and Other Tools for Thinking".
    
    Your task is to write a detailed guide for the thinking tool: "{tool['name']}".
    
    Here is the base information provided:
    
    Category: {tool['category']}
    Short Description: {tool['short_description']}
    Base Description: {tool['detailed_description']}
    Base Exercise/App Idea: {tool['implementation_strategy']}
    
    Please expand on this to create a comprehensive guide (around 500 words).
    Consult your internal knowledge about this tool and Dennett's work.
    
    The output must be in Markdown format with the following sections:
    
    # {tool['name']}
    
    ## Brief Description
    (A concise summary, based on the short description but slightly expanded)
    
    ## Detailed Description
    (Elaborate on the base description. Explain the philosophical concept, the problem it solves, and why it is important. Use examples.)
    
    ## Exercise / How to Apply
    (Describe how a user can practice this tool. Use the "Base Exercise" provided as a starting point but make it a practical, actionable exercise for a human, not just an app feature.)
    
    ## Suggestion for Creating an App
    (Elaborate on the "Base App Idea". Describe how this could be built as a web or mobile app, what the features would be, and how it would gamify the concept.)
    
    Note: Do not include a "References" section unless you have specific citations.
    """
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get('response', '')
    except Exception as e:
        print(f"Error generating content for {tool['name']}: {e}")
        return None

def main():
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)
        
    with open('tools.json', 'r') as f:
        tools = json.load(f)
        
    print(f"Found {len(tools)} tools. Starting generation...")
    
    for i, tool in enumerate(tools):
        slug = slugify(tool['name'])
        filename = os.path.join(CONTENT_DIR, f"{slug}.md")
        
        if os.path.exists(filename):
            print(f"[{i+1}/{len(tools)}] Skipping {tool['name']} (already exists)")
            continue
            
        print(f"[{i+1}/{len(tools)}] Generating {tool['name']}...")
        content = generate_content(tool)
        
        if content:
            with open(filename, 'w') as f:
                f.write(content)
            print(f"  - Saved to {filename}")
        else:
            print(f"  - Failed to generate.")
            
        # small delay
        time.sleep(0.1)

if __name__ == "__main__":
    main()
