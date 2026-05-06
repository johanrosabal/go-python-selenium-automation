import os
import argparse
import re

def to_snake_case(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def create_page(name, app, subfolder):
    snake_name = to_snake_case(name)
    app_path = f"applications/web/{app}"
    
    # Target directory
    target_dir = f"{app_path}/pages"
    if subfolder:
        target_dir = f"{target_dir}/{subfolder}"
    
    os.makedirs(target_dir, exist_ok=True)
    file_path = f"{target_dir}/{snake_name}.py"
    
    if os.path.exists(file_path):
        print(f"Error: File {file_path} already exists.")
        return

    # Read template
    with open("templates/page_object.tmpl", "r") as f:
        template = f.read()
    
    content = template.replace("{{ class_name }}", name)
    
    with open(file_path, "w") as f:
        f.write(content)
    
    print(f"Created Page Object: {file_path}")
    
    # Register in Orchestrator
    register_page(name, app, subfolder, snake_name)

def register_page(name, app, subfolder, snake_name):
    orchestrator_path = f"applications/web/{app}/app/{app}_app.py"
    if not os.path.exists(orchestrator_path):
        print(f"Warning: Orchestrator {orchestrator_path} not found. Skipping registration.")
        return

    with open(orchestrator_path, "r") as f:
        lines = f.readlines()

    # 1. Add Import
    import_path = f"applications.web.{app}.pages."
    if subfolder:
        import_path += f"{subfolder}."
    import_path += f"{snake_name}"
    
    import_line = f"from {import_path} import {name}\n"
    
    if import_line not in lines:
        # Find where to insert (after existing imports)
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("from ") or line.startswith("import "):
                last_import_idx = i
        lines.insert(last_import_idx + 1, import_line)

    # 2. Add Property
    prop_name = snake_name
    if prop_name.endswith("_page"):
        prop_name = prop_name # already has it
    else:
        prop_name = f"{prop_name}_page"

    # Check if property already exists
    if any(f"def {prop_name}(self)" in line for line in lines):
        print(f"Warning: Property {prop_name} already exists in Orchestrator.")
    else:
        # Insert at the end of the class
        new_property = f"\n    @property\n    def {prop_name}(self) -> {name}:\n"
        new_property += f"        \"\"\"Lazy-loaded instance of {name}.\"\"\"\n"
        new_property += f"        if not hasattr(self, \"_{prop_name}\") or self._{prop_name} is None:\n"
        new_property += f"            self._{prop_name} = {name}()\n"
        new_property += f"        return self._{prop_name}\n"
        
        lines.append(new_property)

    with open(orchestrator_path, "w") as f:
        f.writelines(lines)
    
    print(f"Registered {name} in {orchestrator_path}")

def create_test(name, app, test_id, feature):
    snake_name = to_snake_case(name)
    feature_snake = to_snake_case(feature)
    app_path = f"applications/web/{app}"
    
    target_dir = f"{app_path}/tests"
    os.makedirs(target_dir, exist_ok=True)
    
    file_path = f"{target_dir}/test_{feature_snake}.py"
    
    # Read template
    with open("templates/test_case.tmpl", "r") as f:
        template = f.read()
    
    content = template.replace("{{ class_name }}", name)
    content = content.replace("{{ test_id }}", test_id)
    content = content.replace("{{ feature_name }}", feature_snake)
    
    # Determine page property name
    page_property = snake_name
    if not page_property.endswith("_page"):
        page_property = f"{page_property}_page"
    
    content = content.replace("{{ page_property }}", page_property)

    if os.path.exists(file_path):
        # Append test method instead of overwriting? 
        # For simplicity in this tool, we just write if not exists or print warning
        print(f"Warning: Test file {file_path} already exists. You may want to add the test manually.")
        with open(file_path, "a") as f:
            # Simple append (ignoring class structure for now, user can fix)
            # A better tool would parse the AST, but this is a starter.
            f.write("\n    # TODO: Move this manually inside the class if needed\n")
            # We will just write a new class for now or skip
            print("Skipping automatic append to existing test file.")
    else:
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Created Test Case: {file_path}")

if __name__ == "__main__":
    # Ensure templates directory exists
    if not os.path.exists("templates"):
        os.makedirs("templates")
        
    parser = argparse.ArgumentParser(description="Framework Scaffolding Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Command: page
    page_parser = subparsers.add_parser("page", help="Create a new Page Object")
    page_parser.add_argument("--name", required=True, help="PascalCase name (e.g. LoginPage)")
    page_parser.add_argument("--app", required=True, help="App folder name (e.g. go_hotel)")
    page_parser.add_argument("--subfolder", help="Subfolder inside pages/ (optional)")

    # Command: test
    test_parser = subparsers.add_parser("test", help="Create a new Test Case")
    test_parser.add_argument("--name", required=True, help="PascalCase name (e.g. Login)")
    test_parser.add_argument("--app", required=True, help="App folder name (e.g. go_hotel)")
    test_parser.add_argument("--id", required=True, help="Test ID (e.g. HOTEL-001)")
    test_parser.add_argument("--feature", required=True, help="Feature name for the filename")

    args = parser.parse_args()

    if args.command == "page":
        create_page(args.name, args.app, args.subfolder)
    elif args.command == "test":
        create_test(args.name, args.app, args.id, args.feature)
    else:
        parser.print_help()
