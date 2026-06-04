import os
import re

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "core", "ui", "actions")
files = [f for f in os.listdir(directory) if f.endswith(".py")]

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    class_name_match = re.search(r"class\s+([A-Za-z0-9_]+)\b", content)
    if not class_name_match:
        continue
    
    class_name = class_name_match.group(1)

    # We want to find method definitions that do NOT have a return type hint, 
    # but where the method eventually does "return self" (we'll look for "def func(self...):" and if the body has "return self" before the next def)
    
    methods = re.finditer(r"^[ \t]*def\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)\s*:(.*?)(?=^[ \t]*def|\Z)", content, flags=re.MULTILINE | re.DOTALL)
    
    new_content = content
    modifications = 0
    
    for match in methods:
        method_name = match.group(1)
        args = match.group(2)
        body = match.group(3)
        
        # If it already has a type hint, or doesn't return self, skip
        if "return self" in body and not re.search(r"def\s+" + method_name + r"\s*\([^)]*\)\s*->", new_content):
            # Replace the signature
            # We must be careful to only replace this specific signature.
            old_sig = match.group(0).split(':\n', 1)[0] + ':'
            if old_sig.endswith("):"):
                new_sig = old_sig[:-2] + f") -> \"{class_name}\":"
                new_content = new_content.replace(old_sig, new_sig, 1)
                modifications += 1
            elif old_sig.endswith(')'): # if it had a space before :
                pass # usually it's "):" or ") :"
            
    if modifications > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {modifications} methods in {filename}")
