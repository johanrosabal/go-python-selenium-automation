import os
import subprocess
import json
import ast
import re
import cv2
from datetime import datetime
from flask import Flask, render_template, request, Response, jsonify, send_from_directory

app = Flask(__name__)

# Absolute path to the root of the automation framework
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
PLANS_DIR = os.path.join(PROJECT_ROOT, "tools", "test_runner", "plans")

if not os.path.exists(PLANS_DIR):
    os.makedirs(PLANS_DIR)

def extract_metadata(file_path, test_method_name):
    """
    Extracts metadata (id, title, description) from a test method using AST.
    Prioritizes @test_case decorators and falls back to docstrings.
    """
    metadata = {
        "id": None,
        "title": test_method_name,
        "description": ""
    }
    
    try:
        abs_path = os.path.join(PROJECT_ROOT, file_path)
        if not os.path.exists(abs_path):
            return metadata
            
        with open(abs_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == test_method_name:
                # 1. Check for @test_case decorator
                for decorator in node.decorator_list:
                    # Case: @test_case(id="...")
                    if isinstance(decorator, ast.Call) and getattr(decorator.func, 'id', '') == 'test_case':
                        for kw in decorator.keywords:
                            if kw.arg == 'id' and isinstance(kw.value, ast.Constant):
                                test_id = kw.value.value
                                metadata["id"] = test_id
                                # Try to load JSON metadata for this ID
                                # Structure: applications/<layer>/<app>/data/json/<id>.json
                                path_parts = file_path.replace("\\", "/").split("/")
                                if "applications" in path_parts:
                                    idx = path_parts.index("applications")
                                    app_base = os.path.join(PROJECT_ROOT, *path_parts[:idx+3]) # applications/layer/app
                                    json_path = os.path.join(app_base, "data", "json", f"{test_id}.json")
                                    
                                    if os.path.exists(json_path):
                                        with open(json_path, "r", encoding="utf-8") as jf:
                                            data = json.load(jf).get("tests", {})
                                            metadata["title"] = data.get("title", metadata["title"])
                                            metadata["description"] = data.get("description", "")
                                break
                    # Case: Simple name @test_case (unlikely but possible)
                    elif isinstance(decorator, ast.Name) and decorator.id == 'test_case':
                        pass # Need ID argument to load JSON

                # 2. Docstring Fallback (if title/description still default)
                docstring = ast.get_docstring(node)
                if docstring:
                    lines = [l.strip() for l in docstring.split("\n") if l.strip()]
                    if metadata["title"] == test_method_name and lines:
                        metadata["title"] = lines[0]
                    if not metadata["description"]:
                        metadata["description"] = docstring.strip()
                break
    except Exception as e:
        print(f"Error extracting metadata for {test_method_name}: {e}")
        
    return metadata

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reports/<path:filename>")
def serve_reports(filename):
    """Serve media files (videos, screenshots) directly to the web UI."""
    return send_from_directory(REPORTS_DIR, filename)

@app.route("/api/report/generate", methods=["POST"])
def generate_report():
    """Generate Allure Report and serve it via an ad-hoc local server if needed, or just generate the HTML."""
    try:
        # Generate the report into reports/allure-report
        allure_results = os.path.join(REPORTS_DIR, "allure-results")
        allure_report = os.path.join(REPORTS_DIR, "allure-report")
        
        if not os.path.exists(allure_results):
            return jsonify({"status": "error", "message": "No allure results found. Run tests first."}), 400

        cmd = ["npx", "allure-commandline", "generate", allure_results, "-o", allure_report, "--clean"]
        
        # We use shell=True on Windows because 'allure' is usually a .bat or .cmd script
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            error_msg = result.stderr or "Allure CLI failure."
            if "not recognized" in error_msg or "not found" in error_msg.lower():
                error_msg = "Allure CLI is not recognized. Please install it with 'choco install allure' as Administrator."
            return jsonify({"status": "error", "message": f"Failed to generate Allure report: {error_msg}"}), 500

        return jsonify({"status": "success", "message": "Allure report generated successfully.", "url": "/reports/allure-report/index.html"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/apps")
def get_apps():
    """Discover available applications in the applications/ directory."""
    apps = []
    apps_dir = os.path.join(PROJECT_ROOT, "applications")
    if os.path.exists(apps_dir):
        # We expect applications/layer/app_name
        for layer in os.listdir(apps_dir):
            layer_path = os.path.join(apps_dir, layer)
            if os.path.isdir(layer_path) and not layer.startswith("__"):
                for app_name in os.listdir(layer_path):
                    app_path = os.path.join(layer_path, app_name)
                    if os.path.isdir(app_path) and not app_name.startswith("__"):
                        # Check if it has a tests directory
                        if os.path.isdir(os.path.join(app_path, "tests")):
                            apps.append({
                                "id": f"{layer}/{app_name}",
                                "name": f"({layer.upper()}) {app_name.capitalize()}",
                                "path": f"applications/{layer}/{app_name}/tests"
                            })
    return jsonify({"status": "success", "apps": apps})

@app.route("/api/tests")
def get_tests():
    """Run pytest --setup-plan to get all available tests."""
    app_path = request.args.get('app_path', 'applications/web/demo/tests')
    try:
        # Run pytest setup-plan which reliably prints node IDs even with allure/xdist
        cmd = ["pytest", app_path, "--setup-plan"]
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
        
        output_lines = result.stdout.split('\n')
        tests = []
        
        for line in output_lines:
            line = line.strip()
            # Pytest --setup-plan outputs node IDs like:
            # applications/web/demo/tests/test_login.py::TestLogin::test_valid_login (fixtures used: request, setup)
            if "::" in line and "(fixtures used:" in line:
                # Extract just the node ID before the space
                node_id = line.split(" (fixtures used:")[0].strip()
                if node_id not in tests:
                    tests.append(node_id)
                
        # Group tests by file
        grouped_tests = {}
        for test_path in tests:
            parts = test_path.split("::")
            if len(parts) >= 3:
                file_path, class_name, test_name = parts[0], parts[1], parts[2]
                file_name = os.path.basename(file_path)
                
                if file_name not in grouped_tests:
                    grouped_tests[file_name] = []
                
                # Extract metadata for this test
                meta = extract_metadata(file_path, test_name)
                    
                grouped_tests[file_name].append({
                    "id": test_path,
                    "name": test_name,
                    "class": class_name,
                    "title": meta["title"],
                    "test_id": meta["id"],
                    "description": meta["description"]
                })
        
        return jsonify({"status": "success", "files": grouped_tests})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/reports/list", methods=["GET"])
def list_reports():
    """List all existing screenshots and videos."""
    media = []
    
    # Scan videos
    video_dir = os.path.join(REPORTS_DIR, "videos")
    if os.path.exists(video_dir):
        for f in os.listdir(video_dir):
            if f.endswith(".mp4") or f.endswith(".avi"):
                file_path = os.path.join(video_dir, f)
                timestamp = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%I:%M:%S %p")
                
                # Get video duration
                duration_str = "00:00"
                try:
                    cap = cv2.VideoCapture(file_path)
                    if cap.isOpened():
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                        if fps > 0:
                            duration_sec = frame_count / fps
                            mins = int(duration_sec // 60)
                            secs = int(duration_sec % 60)
                            duration_str = f"{mins:02d}:{secs:02d}"
                        cap.release()
                except:
                    pass

                # Try to guess test name and ID from filename
                # Filename format: test_name_ID_YYYYMMDD_HHMMSS.mp4 or test_name_YYYYMMDD_HHMMSS.mp4
                name_parts = f.split("_20")[0] # Removes timestamp
                test_name = name_parts
                test_id = ""
                
                # Check if there is an ID (e.g. test_case_TC001)
                if "_TC" in name_parts:
                    test_name_raw = name_parts.split("_TC")[0]
                    test_id = "TC" + name_parts.split("_TC")[1] # Reconstruct TC001
                    test_name = test_name_raw.replace("_", " ").title()
                else:
                    test_name = test_name.replace("_", " ").title()

                media.append({
                    "type": "video",
                    "path": f"reports/videos/{f}",
                    "name": f,
                    "testName": test_name,
                    "testId": test_id,
                    "timestamp": timestamp,
                    "duration": duration_str
                })
    
    # Scan screenshots
    screenshot_dir = os.path.join(REPORTS_DIR, "screenshots")
    if os.path.exists(screenshot_dir):
        for f in os.listdir(screenshot_dir):
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(screenshot_dir, f)
                timestamp = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%I:%M:%S %p")
                
                name_parts = f.split("_20")[0]
                test_name = name_parts
                test_id = ""
                
                if "_TC" in name_parts:
                    test_name_raw = name_parts.split("_TC")[0]
                    test_id = "TC" + name_parts.split("_TC")[1]
                    test_name = test_name_raw.replace("_", " ").title()
                else:
                    test_name = test_name.replace("_", " ").title()

                media.append({
                    "type": "screenshot",
                    "path": f"reports/screenshots/{f}",
                    "name": f,
                    "testName": test_name,
                    "testId": test_id,
                    "timestamp": timestamp
                })
    
    # Sort by timestamp (newest first)
    media.sort(key=lambda x: os.path.getmtime(os.path.join(PROJECT_ROOT, x["path"])), reverse=True)
    return jsonify({"status": "success", "media": media})

@app.route("/api/media", methods=["DELETE"])
def delete_media():
    """Delete a media file."""
    file_path = request.args.get("path")
    if not file_path:
        return jsonify({"status": "error", "message": "Path required"}), 400
    
    # Security: Ensure we only delete from reports directory
    if ".." in file_path or not file_path.startswith("reports"):
        return jsonify({"status": "error", "message": "Access denied"}), 403
    
    full_path = os.path.join(PROJECT_ROOT, file_path)
    if os.path.exists(full_path):
        try:
            os.remove(full_path)
            return jsonify({"status": "success", "message": "File deleted"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "File not found"}), 404

@app.route("/api/plans", methods=["GET", "POST", "DELETE"])
def manage_plans():
    """List, save or delete test plans."""
    if request.method == "POST":
        data = request.json
        name = data.get("name")
        if not name:
            return jsonify({"status": "error", "message": "Plan name required"}), 400
        
        # Clean filename: remove special characters
        safe_name = "".join([c for c in name if c.isalnum() or c in (' ', '_', '-')]).rstrip()
        filename = f"{safe_name}.json"
        path = os.path.join(PLANS_DIR, filename)
        
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
            
        return jsonify({"status": "success", "message": f"Plan '{name}' saved successfully."})
    
    if request.method == "DELETE":
        name = request.args.get("name")
        if not name:
            return jsonify({"status": "error", "message": "Plan name required"}), 400
        
        safe_name = "".join([c for c in name if c.isalnum() or c in (' ', '_', '-')]).rstrip()
        filename = f"{safe_name}.json"
        path = os.path.join(PLANS_DIR, filename)
        
        if os.path.exists(path):
            os.remove(path)
            return jsonify({"status": "success", "message": f"Plan '{name}' deleted."})
        return jsonify({"status": "error", "message": "Plan not found"}), 404

    # GET: List all plans
    plans = []
    if os.path.exists(PLANS_DIR):
        for f in os.listdir(PLANS_DIR):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(PLANS_DIR, f), "r") as json_file:
                        plans.append(json.load(json_file))
                except Exception:
                    continue
    return jsonify({"status": "success", "plans": plans})


@app.route("/api/run", methods=["POST"])
def run_test():
    """Run specific test(s) and stream the output back to the client."""
    data = request.json
    # test_id can now be a string or a list of strings
    test_ids = data.get("test_id", "applications/web/demo/tests")
    browser = data.get("browser", "chrome")
    env_name = data.get("env", "qa")
    headless = data.get("headless", True)
    video = data.get("video", False)
    
    def generate_output():
        env_vars = os.environ.copy()
        env_vars["BROWSER"] = browser
        env_vars["ENV"] = env_name
        env_vars["HEADLESS"] = "true" if headless else "false"
        env_vars["VIDEO_ENABLED"] = "true" if video else "false"
        env_vars["PYTHONPATH"] = PROJECT_ROOT
        env_vars["PYTHONIOENCODING"] = "utf-8"

        
        # Prepare the pytest command
        cmd = [
            "pytest", 
            "-v", 
            "--no-header",
            "--alluredir=reports/allure-results",
            "--clean-alluredir",
            "-o", "log_cli=true",
            "-o", "log_cli_level=INFO"
        ]
        
        if isinstance(test_ids, list):
            cmd.extend(test_ids)
        else:
            cmd.append(test_ids)
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=PROJECT_ROOT,
            env=env_vars,
            text=True,
            encoding="utf-8",
            bufsize=1
        )

        
        display_cmd = f"pytest {' '.join(test_ids) if isinstance(test_ids, list) else test_ids}"
        yield f"data: {json.dumps({'type': 'start', 'message': f'Running: {display_cmd}'})}\n\n"
        yield f"data: {json.dumps({'type': 'env', 'message': f'Environment: {env_name.upper()} | Browser: {browser.upper()} | Headless: {headless}'})}\n\n"
        
        # Stream the output line by line
        for line in iter(process.stdout.readline, ""):
            if line:
                yield f"data: {json.dumps({'type': 'log', 'message': line.strip()})}\n\n"
                
        process.stdout.close()
        return_code = process.wait()
        
        status = "PASSED" if return_code == 0 else "FAILED"
        yield f"data: {json.dumps({'type': 'end', 'status': status, 'code': return_code})}\n\n"

    return Response(generate_output(), mimetype="text/event-stream")

if __name__ == "__main__":
    print(f"🚀 Starting Test Runner GUI at http://localhost:5000")
    print(f"📂 Project Root: {PROJECT_ROOT}")
    app.run(host="0.0.0.0", port=5000, debug=True)
