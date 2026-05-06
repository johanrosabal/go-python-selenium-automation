# 🐍 Python Selenium Automation Framework

A professional-grade, high-performance automation framework built for scalability, robustness, and an exceptional developer experience. Based on the **Page Object Model (POM)** with **Singletons**, it implements a **Fluent API**, **Parallel Execution**, and a **Data-Driven** testing architecture.

---

## 🏆 Project Rating

| Category | Rating | Level |
| :--- | :---: | :--- |
| **Architecture (POM + Fluent)** | ⭐⭐⭐⭐⭐ | **Enterprise** |
| **Performance (Parallel/Skip)** | ⭐⭐⭐⭐⭐ | **High Speed** |
| **Scalability (Orchestrator)** | ⭐⭐⭐⭐⭐ | **Unbeatable** |
| **Maintainability (JSON Data)** | ⭐⭐⭐⭐⭐ | **Simplified** |
| **Infrastructure (Grid/Video/DB)**| ⭐⭐⭐⭐⭐ | **Full Stack** |

**Overall Status: `PROFESSIONAL GRADE / PRODUCTION READY`**

---

## 🛠️ Installation Guide

### 1. Prerequisites
- **Python**: Version 3.10 or higher. [Download](https://www.python.org/downloads/).
- **Git**: For version control.
- **Chrome/Edge/Firefox**: Browser installed.

### 2. Clone and Configure
```bash
git clone https://github.com/your-username/python-selenium-automation.git
cd python-selenium-automation
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 🏢 Corporate Environments (SSL Certificates)
If you are behind a corporate proxy that requires security certificates:

*   **Using a specific certificate:**
    ```bash
    pip install --cert path/to/certificate.pem -r requirements.txt
    ```
*   **Trusted Host (Optional):**
    ```bash
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
    ```

### 4. Verify Installation
```bash
$env:PYTHONPATH = "."; pytest --version
```

---

## 🔌 VS Code Extensions

The project includes a `.vscode/extensions.json` file — VS Code will automatically prompt you to install all recommended extensions when you open the project.

To install them manually: `Ctrl+Shift+P` → **Extensions: Show Recommended Extensions**

### ✅ Required (Core Functionality)

| Extension | ID | Purpose |
| :--- | :--- | :--- |
| **Python** | `ms-python.python` | Language support, IntelliSense, test runner integration |
| **Pylance** | `ms-python.pylance` | Fast type-checking and autocompletion |
| **Debugpy** | `ms-python.debugpy` | Debugger for F5 / launch profiles |

### 🧪 Testing

| Extension | ID | Purpose |
| :--- | :--- | :--- |
| **Python Test Adapter** | `littlefoxteam.vscode-python-test-adapter` | Tree view of all pytest test cases |
| **Test Explorer UI** | `hbenl.vscode-test-explorer` | Base for the Test Explorer sidebar |

### 📊 Reporting

| Extension | ID | Purpose |
| :--- | :--- | :--- |
| **Allure Support** | `yagajs.allure-support` | View Allure reports directly inside VS Code |

### ⚙️ YAML

| Extension | ID | Purpose |
| :--- | :--- | :--- |
| **YAML** | `redhat.vscode-yaml` | Validation and autocomplete for `qa.yaml` / `dev.yaml` |

### 🎥 Media (Video Recordings)

| Extension | ID | Purpose |
| :--- | :--- | :--- |
| **Preview MP4** | `analytic-signal.preview-mp4` | Preview `.avi`/`.mp4` test recordings in VS Code |

### 🛠️ Productivity (Optional but Recommended)

| Extension | ID | Purpose |
| :--- | :--- | :--- |
| **GitLens** | `eamodio.gitlens` | Inline Git blame and history |
| **vscode-icons** | `vscode-icons-team.vscode-icons` | Visual folder/file icon theme |
| **Markdown All in One** | `yzhang.markdown-all-in-one` | Preview + shortcuts for README editing |
| **GitHub Markdown Preview** | `bierner.markdown-preview-github-styles` | GitHub-style README preview |
| **Black Formatter** | `ms-python.black-formatter` | Auto-format Python code on save |
| **autoDocstring** | `njpwerner.autodocstring` | Auto-generate Python docstrings |

> [!WARNING]
> **Avoid installing Pyrefly** (`facebook.pyrefly`). It generates false parse errors on decorator lines. The project already has `"pyrefly.enable": false` in `settings.json`, but it's safer not to install it at all.

---

## 📁 Project Architecture

The system strictly separates the infrastructure (`core`) from individual projects (`applications`):

```text
├── .github/workflows/      # 🔄 CI/CD (GitHub Actions Pipeline)
├── applications/web/       # 📂 Application Layer (Real projects)
│   └── demo/               # 🍏 SauceDemo Project
│       ├── app/            # 📦 App Orchestrator (Entry Point)
│       ├── config/         # ⚙️ YAML Config per Environment
│       ├── data/json/      # 📊 Data by ID (CT-XXX.json)
│       ├── pages/          # 🏗️ Page Objects (POM)
│       └── tests/          # 🧪 Test Cases (Scripts)
├── core/                   # 🧠 Framework Core (Immutable)
│   ├── ui/actions/         # 🕹️ UI Action Components (Stateful Pattern)
│   ├── ui/common/          # 🧱 Singleton, BasePage, BaseTest UI
│   ├── api/actions/        # 🌐 API Action Components (GET, POST, etc.)
│   ├── api/common/         # 🏛️ BaseEndpoint, BaseAPITest, APIResponse
│   └── utils/              # 🧰 Logger, Config, Loader, Decorators
├── logs/                   # 🔎 Traceability (automation.log)
├── reports/                # 📊 Allure Results
└── pytest.ini              # ⚙️ Execution Orchestrator
```

---

## 📏 Code Conventions & Standards

### 1. Naming
| Element | Format | Example |
| :--- | :--- | :--- |
| **Page Classes** | `PascalCase` | `LoginPage`, `InventoryPage` |
| **Action Methods** | `snake_case` (Verb) | `login_as()`, `add_product()` |
| **Locators** | `CAPS_SNAKE` (Prefix) | `INP_USERNAME`, `BTN_LOGIN` |

### 2. Locator Prefix Standard
| Prefix | Element | Example |
| :--- | :--- | :--- |
| `btn` | Buttons | `btn_login`, `btn_submit` |
| `inp` | Inputs / Fields | `inp_username`, `inp_search` |
| `txt` | Labels / Text | `txt_error_msg`, `txt_title` |
| `sel` | Dropdowns / Select | `sel_country`, `sel_size` |
| `chk` | Checkboxes | `chk_terms`, `chk_remember` |

---

## ⚙️ Configuration System (YAML)

The framework uses YAML files to manage environment-specific parameters (QA, DEV, PROD), decoupling sensitive data and URLs from the source code.

### 1. File Location
`applications/web/demo/config/environments/{env}.yaml`

### 2. Typical Structure (`qa.yaml`)

#### 📝 Metadata & Management
*   **`name`**: Descriptive project name (e.g. "SauceDemo - Swag Labs").
*   **`tms`**: Base URL of your Test Management System.

#### 🌐 Web & Navigation
*   **`web.base_url`**: The main URL where tests start. Used by `.open()` without arguments.

#### 🖥️ Browser (Local Overrides)
*   **`browser.edge_path`**: (Optional) Absolute path to driver executable.
*   **`default.browser`**: Default browser if none is specified via command line.

#### 📹 Video Recording (OpenCV)
*   **`video.enable_local`**: Enable/Disable screen capture (`true`/`false`).
*   **`video.fps`**: Capture speed. `10` is ideal for automation.
*   **`video.monitor_index`**: Which monitor to record (`0` = all, `1` = primary).

#### 👥 User Data & Validation
*   **`user`**: Credentials for the Happy Path.
*   **`locked_user`**: Locked user to test error messages.
*   **`messages`**: Expected texts for assertions (e.g. `error_locked`, `error_invalid`).

### 3. How to use `ConfigManager`

```python
from core.utils.config_manager import ConfigManager

url     = ConfigManager.get("web.base_url")
user    = ConfigManager.get("user.username")
timeout = ConfigManager.get("web.timeout", 30)
```

> [!NOTE]
> The active environment is set via the `$env:ENV` environment variable. If not set, the framework loads `qa.yaml` by default.

---

## 🚀 Developer Guide (Productivity)

### ⚡ Option A: Automated Scaffolding (Recommended)

#### 1. From VS Code (Visual Interface)
1. Press `Ctrl + Shift + P` and search **`Tasks: Run Task`**.
2. Select a smart task:
   - **`🚀 Scaffold: New Page Object`**: Creates the page and registers it in the Orchestrator.
   - **`🧪 Scaffold: New Test Case`**: Generates a test file with ready-to-use decorators.
   - **`🖥️ Runner: Launch UI`**: Launches the Flask-based Test Runner GUI.
   - **`📊 Allure: Open Report Server`**: Generates and opens the Allure report server.

#### 2. From Terminal (CLI)
```powershell
python tools/scaffold.py page --name ProfilePage --app go_hotel
python tools/scaffold.py test --name Profile --app go_hotel --id HOTEL-001 --feature Profile
```

---

### 🛠️ Option B: Manual Creation (Step by Step)

Create a file in `applications/web/demo/pages/name_page.py`. Inherit from `BasePage` and use the **Fluent API**:

```python
from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By

class DashboardPage(BasePage):
    BTN_PROFILE = (By.ID, "user-profile")

    def go_to_profile(self):
        self.element(self.BTN_PROFILE).click()
        return self
```

### 2. Register in the Orchestrator (App)

The **App Orchestrator** centralizes all Pages in one place, making tests cleaner and easier to write.

#### 💡 Why use an Orchestrator?
1. **Single Entry Point**: Tests only use `self.app` — no manual class instantiation.
2. **Lazy Loading**: Pages are created in memory only when the test actually needs them.
3. **Full IntelliSense**: Python typing (`-> LoginPage`) gives auto-suggestions in the editor.

#### 🛠️ How to register a new Page
In `applications/web/demo/app/demo_app.py`:

```python
from applications.web.demo.pages.profile_page import ProfilePage

@property
def profile_page(self) -> ProfilePage:
    if not hasattr(self, "_profile_page") or self._profile_page is None:
        self._profile_page = ProfilePage()
    return self._profile_page
```

### 3. Prepare Test Data (JSON)

#### 📁 Location & Naming
`applications/web/{app_name}/data/environments/{env_name}/{test_id}.json`

> [!IMPORTANT]
> **Naming Convention**: The filename must match the `id` used in `@test_case(id="...")`. E.g. if the ID is `CT-LOGIN-001`, the file must be `CT-LOGIN-001.json`.

#### 🏗️ JSON Standard Structure (UI & API)
All JSON files — both UI and API — follow the **same mandatory structure**:

##### 🖥️ UI Test JSON
```json
{
  "tests": {
    "id": "CT-LOGIN-001",
    "title": "Login with valid credentials",
    "description": "Validates the happy path login with a standard user.",
    "feature": "Authentication",
    "story": "Login",
    "severity": "CRITICAL",
    "tag": ["smoke", "p1"],
    "data": {
      "user": "standard_user",
      "pass": "secret_sauce",
      "expected_url": "/dashboard"
    }
  }
}
```

##### 🌐 API Test JSON
For APIs, `data` contains a `payload` representing the request body:
```json
{
  "tests": {
    "id": "SEARCH-001",
    "title": "Complete Search Flow (POST + GET Results)",
    "description": "End-to-end: POST to initiate search → GET results by GUID.",
    "feature": "Policy Search",
    "story": "Search Policies",
    "severity": "CRITICAL",
    "tag": ["smoke", "p1", "e2e"],
    "data": {
      "payload": {
        "firstName": "John",
        "lastName": "Doe",
        "policyState": "TX"
      }
    }
  }
}
```

> [!IMPORTANT]
> **The JSON is the single source of truth.** The `@test_case` decorator reads `title`, `description`, `severity`, `feature`, `story` and `tag` directly from the JSON. **Do not repeat them in the decorator.**

#### 🛠️ Accessing data in the test

##### UI Tests (`BaseTest`)
```python
@test_case(id="CT-LOGIN-001")
def test_valid_login(self):
    data = self.get_data_for_test()          # returns tests.data {}
    self.app.login_page.open().login(data.get("user"), data.get("pass"))
```

##### API Tests (`BaseAPITest`)
```python
@test_case(id="SEARCH-001")
def test_search_flow(self):
    data = self.get_test_data("SEARCH-001")  # returns full tests {} block
    payload = data["data"]["payload"]
    self.app.search_and_get_results(payload).assert_status_code(200)
```

### 4. Create the Test Case

```python
from core.ui.common.base_test import BaseTest
from core.utils.decorators import test_case

class TestDashboard(BaseTest):
    @test_case(id="CT-DASH-001")
    def test_access_profile(self):
        data = self.get_data_for_test()
        self.app.login_page.open().login()
        self.app.dashboard_page.go_to_profile()
        assert "profile" in self.get_url()
```

### 5. Run Tests
```powershell
$env:PYTHONPATH = "."; pytest applications/web/demo/tests
pytest applications/web/demo/tests/test_feature.py --alluredir=reports
```

### 6. Preconditions (Fixtures)
```python
@pytest.fixture
def logged_in(app):
    app.login_page.open().login("user", "pass")
    return app

def test_my_flow(self, logged_in):
    self.app.inventory_page.do_something()
```

### 7. Share Data Between Tests (SessionContext)
```python
from core.utils.session_context import SessionContext

def test_a_create_order(self):
    order_id = self.app.order_page.create()
    SessionContext.set("last_order", order_id)

def test_b_validate_order(self):
    order_id = SessionContext.get("last_order")
    self.app.order_page.search(order_id)
```

---

## 🚀 Test Architecture & Advanced Patterns

### 1. Persistent Sessions (`persistent_session = True`)
By default, the framework opens and closes the browser for each test method (total isolation). For long flows or regression suites, enable persistence at class level:

```python
class TestReserved(BaseTest):
    persistent_session = True
```
*   **Benefit**: Reduces total execution time by up to 40% by avoiding browser cold starts.

### 2. Typing & Autocomplete (`app: GoHotelApp`)
```python
class TestReserved(BaseTest):
    app: GoHotelApp
```
*   **Result**: When you type `self.app.`, the editor auto-suggests all available pages and their methods.

### 3. Application Decorator (`@go_hotel`)
```python
@go_hotel
class TestLogin(BaseTest):
    ...
```
*   **What it does**: Sets the default values for `app_name`, `profile` (dev/qa), and `browser`. Allows running the test directly from the IDE Run button without setting environment variables.

### 4. Test Case Decorator (`@test_case`)
**You only need to pass the `id`** — all other metadata is read automatically from the JSON:

```python
@test_case(id="HOTEL-001")
def test_successful_login(self):
    ...
```

*   **Automatic Metadata Injection**: The framework loads `HOTEL-001.json` during `setup` and extracts `title`, `description`, `severity`, `feature`, `story` and `tag` from the `tests` block. No need to repeat them in the decorator.
*   **Resolution Priority**: `JSON → Decorator argument → Function name`. If you define `title=` in the decorator, it overrides the JSON.
*   **Allure Reports**: Automatically syncs all JSON metadata with the report (title, severity, tags, TMS link).
*   **TMS Integration**: If you use Jira/TestRail, the `id` creates a direct link in the Allure report.

> [!TIP]
> **Golden rule**: the decorator only needs the `id`. Everything else lives in the JSON, which is the single source of truth.

---

## 🕹️ Methods Catalog

### 1. Navigation & Context (BasePage)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.open(url)` | `this` | Navigate to the specified URL (or `base_url`). |
| `.open_relative(path)` | `this` | Navigate to a relative path (e.g. `/inventory`). |
| `.get_url()` | `string` | Returns the current browser URL. |
| `.wait_for_url(url)` | `this` | Waits until the URL contains the text. |
| `.navigation.back()` | `this` | Goes back to the previous page. |
| `.navigation.forward()` | `this` | Goes forward in browser history. |
| `.navigation.refresh()` | `this` | Reloads the current page. |
| `.navigation.get_current_url()` | `string` | Returns current URL (via component). |

### 2. Windows & Frames (BasePage)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.window.open_new()` | `this` | Opens a new blank tab/window. |
| `.window.switch_to_new()` | `this` | Switches focus to the last opened tab. |
| `.window.switch_to_main()` | `this` | Returns to the initial tab (index 0). |
| `.window.to_tab(index)` | `this` | Switches to a tab by numeric index. |
| `.window.close_current()` | `this` | Closes current tab and returns to previous. |
| `.window.get_handles()` | `list` | Returns all window IDs from the driver. |
| `.frame.switch_to(loc)` | `this` | Switches focus to a specific iframe. |
| `.frame.switch_to_parent()` | `this` | Goes up one level to the parent frame. |
| `.frame.switch_to_default()` | `this` | Returns to the main browser document. |
| `.alert.wait_presence()` | `this` | Waits for an alert/confirm/prompt to appear. |
| `.alert.accept()` | `this` | Accepts the alert (OK). |
| `.alert.dismiss()` | `this` | Cancels the alert (Cancel). |
| `.alert.type(text)` | `this` | Types in a JavaScript prompt. |
| `.alert.get_text()` | `string` | Returns the dialog text. |

### 3. Mouse Interactions (UIElement)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.click()` | `this` | Left click with clickability wait. |
| `.js_click()` | `this` | Forced click via JavaScript. |
| `.double_click()` | `this` | Double click (ActionChains). |
| `.right_click()` | `this` | Right click (Context Click). |
| `.hover()` | `this` | Move mouse over the element. |
| `.drag_and_drop(loc)` | `this` | Drags element to another target. |
| `.click_and_hold()` | `this` | Holds the click pressed. |
| `.release_mouse()` | `this` | Releases mouse button. |
| `.release()` | `this` | Alias for `.release_mouse()`. |

### 4. Keyboard & Data (UIElement)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.type(text)` | `this` | Types text (clears the field first). |
| `.type_encrypted(key)` | `this` | Types text hiding it from logs. |
| `.type_by_character(v)` | `this` | Simulates human typing (char by char). |
| `.press(key)` | `this` | Sends a special key (e.g. `Keys.ENTER`). |
| `.press_enter()` | `this` | Shortcut for ENTER key. |
| `.press_tab()` | `this` | Shortcut for TAB key. |
| `.press_return()` | `this` | Shortcut for RETURN key. |
| `.press_escape()` | `this` | Shortcut for ESCAPE key. |
| `.clear()` | `this` | Clears an input field. |

### 5. Scroll & Visibility (UIElement)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.scroll_to(offset)` | `this` | Scrolls viewport to element with optional offset. |
| `.scroll_to_center()` | `this` | Centers the element exactly on screen. |
| `.scroll_to_top()` | `this` | Scrolls to the top of the page. |
| `.scroll_to_bottom()` | `this` | Scrolls to the bottom of the page. |

### 6. Dropdowns & Lists (UIElement)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.select_by_text(val)` | `this` | Selects by exact visible text. |
| `.select_by_value(val)` | `this` | Selects by the `value` attribute. |
| `.select_by_index(i)` | `this` | Selects by index (0-based). |
| `.select_by_partial_text` | `this` | Selects if text contains the value. |
| `.deselect_all()` | `this` | Removes all selections (multi-select). |
| `.get_dropdown_options()` | `list` | Returns all option texts. |

### 7. States & Waits (UIElement)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.wait_visible()` | `bool` | Waits until element is visible. |
| `.wait_present()` | `bool` | Waits until element is in the DOM. |
| `.wait_clickable()` | `this` | Waits until element is interactable. |
| `.wait_disappear()` | `this` | Waits until element hides/is removed. |
| `.wait_text_contains(v)` | `this` | Waits until text contains a value. |
| `.is_visible()` | `bool` | Returns whether currently visible. |
| `.is_present()` | `bool` | Returns whether present in the DOM. |
| `.is_enabled()` | `bool` | Returns whether element is enabled. |
| `.is_enabled_js()` | `bool` | Checks enabled state via JS. |
| `.is_clickable()` | `bool` | Checks if visible and enabled. |
| `.get_css_value(p)` | `string` | Returns a CSS property value. |
| `.set_css_value(p, v)` | `this` | Sets a CSS property via JS. |

### 8. Tables & Grids (UIElement)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.get_cell_text(r, c)` | `string` | Returns text of a cell (Row, Col). |
| `.get_row_count()` | `int` | Returns total number of rows. |
| `.get_table_headers()` | `list` | Returns all column names. |
| `.get_table_data()` | `list[dict]` | Extracts entire table as list of dicts. |
| `.click_table_header(t)` | `this` | Clicks header by text or index. |
| `.table_check_row(r)` | `this` | Checks the checkbox of a specific row. |
| `.table_click_button(r, c, t)` | `this` | Clicks button inside a cell. |
| `.table_click_link(r, c, t)` | `this` | Clicks link inside a cell. |
| `.table_wait_for_rows(n)` | `this` | Waits until table has N rows. |
| `.table_wait_not_empty()` | `this` | Waits until table has data. |

### 9. Screenshots & Global Sync (BasePage)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.scroll_to_top()` | `this` | Scrolls to top of page (Global). |
| `.scroll_to_bottom()` | `this` | Scrolls to bottom of page (Global). |
| `.screenshot.capture(n)` | `this` | Captures current viewport. |
| `.screenshot.full_page` | `this` | Captures full page (scroll). |
| `.wait_for_page_load()` | `this` | Waits until DOM is `complete`. |
| `.wait_for_js_completion` | `this` | Waits until JS/jQuery activity ends. |

### 10. Data Extraction & Attributes (UIElement)
| Method | Returns | Description |
| :--- | :--- | :--- |
| `.get_text()` | `string` | Returns the visible text of the element. |
| `.get_trimmed_text()` | `string` | Returns text without leading/trailing spaces. |
| `.get_value()` | `string` | Returns the `value` attribute. |
| `.get_int()` | `int` | Extracts the first integer from the text. |
| `.get_float()` | `float` | Extracts the first decimal number from the text. |
| `.all_texts()` | `list[str]` | Returns texts of all child elements. |
| `.get_inner_html()` | `string` | Captures inner HTML code. |
| `.get_outer_html()` | `string` | Captures the full HTML of the tag. |
| `.get_text_content()` | `string` | Captures text even if hidden. |
| `.get_attribute(n)` | `string` | Returns the value of a specific attribute. |
| `.contains_text(t)` | `bool` | Checks if element contains the given text. |
| `.matches_regex(p)` | `bool` | Validates text against a Regex pattern. |
| `.is_empty()` | `bool` | Checks if the element has no text content. |
| `.wait_until_text_is(t)` | `this` | Waits until text is identical to the value. |
| `.at(seconds)` | `this` | Sets timeout for the next action only. |
| `.upload_file(path)` | `this` | Uploads a file. |

---

## 💡 Practical Usage Examples

### 1. Navigation & Window Management
```python
def login_and_new_tab(self):
    self.open_relative("/dashboard")
    self.window.open_new()
    self.window.switch_to_new()
    self.wait_for_page_load()
    self.navigation.wait_url_contains("google.com", timeout=5)
    self.window.close_current()
    self.window.switch_to_main()
```

### 2. Forms & Advanced Keyboard
```python
def complete_profile(self):
    self.element(BIO).type_by_character("I love automation...")
    self.element(SEARCH).type("Playwright").press_enter().press_escape()
    self.element(PWD).type_encrypted("SuperSecret123")
```

### 3. Dropdowns & Selection
```python
def configure_preferences(self):
    self.element(COUNTRY).select_by_text("Spain")
    self.element(CURRENCY).select_by_value("EUR")
    self.element(LANGUAGE).select_by_index(0)
    self.element(INTERESTS).deselect_all()
    options = self.element(MODULE).get_dropdown_options()
    if "Admin" in options:
        self.element(MODULE).select_by_partial_text("Admin")
```

### 4. Dynamic Tables & Grids
```python
def manage_users(self):
    self.element(USERS_TABLE).table_wait_not_empty()
    self.element(USERS_TABLE).table_wait_for_rows(5)
    data    = self.element(USERS_TABLE).get_table_data()
    headers = self.element(USERS_TABLE).get_table_headers()
    self.element(USERS_TABLE).table_click_button(row=2, col="Actions", text="Delete")
    self.element(USERS_TABLE).table_check_row(row=4, column=1)
```

### 5. IFrames & Contexts
```python
def interact_with_frame(self):
    self.frame.switch_to(self.PAYMENT_IFRAME_LOCATOR)
    self.element(CARD_NUMBER).type("4242...")
    self.frame.switch_to_default()
```

### 6. Scroll & Visibility
```python
def validate_footer(self):
    self.scroll_to_bottom()
    self.element(FOOTER).scroll_to(offset=100)
    self.element(LOGO).scroll_to_center().screenshot("logo_centered")
```

### 7. Assertions & Data Extraction
```python
def validate_totals(self):
    total  = self.element(TOTAL_LBL).get_float()
    count  = self.element(BADGE).get_int()
    if self.element(DATE).matches_regex(r"\d{2}/\d{2}/\d{4}"):
        print("Correct date format")
    css_class = self.element(BTN).get_attribute("class")
```

### 8. Critical Timing (`at()`)
```python
def heavy_flow(self):
    self.element(EXPORT_BTN).at(60).click()
    self.element(STATUS).at(120).wait_until_text_is("Completed")
```

### 9. Alerts & Prompts
```python
def handle_alerts(self):
    self.alert.wait_presence().type("Antigravity").accept()
    if "Are you sure?" in self.alert.get_text():
        self.alert.dismiss()
```

### 10. File Upload
```python
self.element(UPLOAD_INP).upload_file("C:/temp/manual.pdf")
```

---

> [!TIP]
> **✨ The Power of the Fluent Interface (Method Chaining)**
>
> You can chain multiple precise actions on a single element in one line:
>
> ```python
> self.app.dashboard_page.element(BTN_ADVANCED_CONFIG) \
>     .at(30) \
>     .scroll_to_center() \
>     .hover() \
>     .screenshot("btn_hover_state") \
>     .wait_clickable() \
>     .click()
> ```

---

## 🌐 API Testing (Endpoints Object Model - EOM)

Following the same philosophy as POM for UI, the framework implements the **Endpoints Object Model (EOM)** for robust, scalable API tests with fluent assertions.

### 1. EOM Architecture
*   **`BaseEndpoint`**: Centralizes HTTP actions (`get`, `post`, `put`, `delete`).
*   **`BaseAPITest`**: Manages `requests` sessions, authentication and environment config.
*   **`APIResponse`**: Response wrapper that enables chained validations (Fluent Assertions).

### 2. Endpoint Object Example
```python
from core.api.common.base_endpoint import BaseEndpoint

class UserEndpoint(BaseEndpoint):
    def __init__(self, session):
        super().__init__(session)
        self.url = f"{self.base_url}/users"

    def get_users(self):
        return self.get.call(self.url)

    def create_user(self, name, job):
        return self.post.call(self.url, json={"name": name, "job": job})
```

### 3. API Test Example
```python
from core.api.common.base_api_test import BaseAPITest

class TestUserAPI(BaseAPITest):
    app_name = "demo"

    def test_create_user(self):
        users_api = UserEndpoint(self.session)
        users_api.create_user("Johan", "QA") \
            .assert_status_code(201) \
            .assert_json_path("name", "Johan")
```

### 4. App Client Orchestrator (API)
Just as UI has `DemoApp`, the API layer uses a **Client Orchestrator** to encapsulate multi-endpoint flows with Lazy Loading:

```python
# applications/api/nico_search/client.py
class NicoSearchClient:
    def __init__(self, session, config: dict):
        self._session = session
        self._search  = None

    @property
    def search(self) -> SearchEndpoint:
        if self._search is None:
            self._search = SearchEndpoint(self._session, self._config)
        return self._search

    def search_and_get_results(self, payload: dict):
        """Composed flow: POST → get GUID → GET results."""
        search_response = self.search.search_policies(payload)
        search_response.assert_status_code(201)
        search_id = search_response.body.strip()
        return search_id, self.search.get_results(search_id)
```

`BaseAPITest` auto-discovers and loads the Client by naming convention (`client.py`). In tests you simply use `self.app`:

```python
class TestNicoSearch(BaseAPITest):
    app_name = "nico_search"   # ← auto-loads NicoSearchClient as self.app

    @test_case(id="SEARCH-001")
    def test_complete_search_flow(self):
        data = self.get_test_data("SEARCH-001")
        search_id, results = self.app.search_and_get_results(data["data"]["payload"])
        results.assert_status_code(200)
```

### 5. EOM Advantages
- **Automatic Logging**: All requests and responses are logged with visual icons in the console and Allure.
- **Fluent Assertions**: Validates status codes and JSON content in a single line.
- **Maintainability**: API contract changes are reflected in one place (the Endpoint Object).
- **Client Orchestrator**: Encapsulates multi-step flows — the test does not know which internal endpoints are called.

---

## 📊 Data-Driven & Allure Integration

### 1. Standard JSON Structure (UI & API)
All JSON files in the framework — both UI and API — follow the **same mandatory structure**. The filename must match the `id` used in the `@test_case` decorator.

#### 🖥️ UI Test JSON (`data/{env}/{TEST-ID}.json`)
```json
{
  "tests": {
    "id": "CT-LOGIN-001",
    "title": "Login with valid credentials",
    "description": "Validates the happy path login with a standard user.",
    "feature": "Authentication",
    "story": "Login",
    "severity": "CRITICAL",
    "tag": ["smoke", "p1"],
    "data": {
      "user": "standard_user",
      "pass": "secret_sauce",
      "expected_url": "/dashboard"
    }
  }
}
```

#### 🌐 API Test JSON (`data/{env}/{TEST-ID}.json`)
For APIs, `data` contains a `payload` representing the request body:
```json
{
  "tests": {
    "id": "SEARCH-001",
    "title": "Complete Search Flow (POST + GET Results)",
    "description": "End-to-end: POST to initiate search → GET results by GUID.",
    "feature": "Policy Search",
    "story": "Search Policies",
    "severity": "CRITICAL",
    "tag": ["smoke", "p1", "e2e"],
    "data": {
      "payload": {
        "firstName": "John",
        "lastName": "Doe",
        "policyState": "TX"
      }
    }
  }
}
```

> [!IMPORTANT]
> **The JSON is the single source of truth.** The `@test_case` decorator reads `title`, `description`, `severity`, `feature`, `story` and `tag` directly from the JSON. **Do not repeat them in the decorator.**

### 2. How to Access Data in the Test

#### UI Tests (`BaseTest`)
```python
@test_case(id="CT-LOGIN-001")
def test_valid_login(self):
    data = self.get_data_for_test()           # returns tests.data {}
    self.app.login_page.open().login(data.get("user"), data.get("pass"))
```

#### API Tests (`BaseAPITest`)
```python
@test_case(id="SEARCH-001")
def test_search_flow(self):
    data    = self.get_test_data("SEARCH-001")  # returns full tests {} block
    payload = data["data"]["payload"]
    self.app.search_and_get_results(payload).assert_status_code(200)
```

### 3. Using the `@test_case` Decorator (Recommended)
With the **App Orchestrator** pattern, tests stay clean and focused:

```python
@test_case(id="CT-LOGIN-001")
def test_valid_login(self):
    data = self.get_data_for_test()
    self.app.login_page.open().login(data.get("user"), data.get("pass"))
    self.app.inventory_page.add_backpack_to_cart()
```

### 4. Benefits of this Approach
1. **Maintainability**: If credentials or expected values change, only edit the JSON.
2. **Enriched Reports**: The ID is automatically linked in Allure reports.
3. **Traceability**: Easily maps each automation script to its test case in TMS tools (Jira/TestRail).

---

## 📹 Video Recording & Cleanup

### 1. Video Configuration (`qa.yaml`)
```yaml
video:
  enable_local: true   # true to record, false to disable
  fps: 10              # Frames per second (recommended: 10-15)
  monitor_index: 0     # 0 = all monitors, 1 = primary monitor
```

> [!WARNING]
> **Privacy**: Local recording captures your **entire screen**. Make sure no sensitive information is visible during tests.

### 2. Storage & Viewing
*   **Path**: Videos are saved in `reports/videos/` as `.avi` files.
*   **VS Code**: The **"Media Preview"** extension is recommended for viewing videos directly in the editor.

### 3. Automatic Cleanup
The framework automatically **deletes** the `reports/` folder (including past videos) at the start of each new test session, ensuring you only see results from the current run.

---

## 🗄️ Database Integration (SQLAlchemy)

Supports connections to multiple database engines (PostgreSQL, SQL Server, MySQL, SQLite) via **SQLAlchemy**.

### 1. Configuration (`qa.yaml`)
```yaml
database:
  url: "postgresql://user:pass@localhost:5432/dbname"
  # For local SQLite: "sqlite:///resources/data/test.db"
```

### 2. Layer Structure
*   **`core/utils/db_client.py`**: Generic engine. Manages connection pools and sessions.
*   **`applications/web/demo/app/db_manager.py`**: Business layer. Write your specific SQL queries here.

### 3. Usage in Tests
```python
def test_validate_db_record(self):
    user = self.app.db.get_user_by_username("test_user")
    assert user["email"] == "test@example.com"
    self.app.db.client.execute_query("DELETE FROM logs WHERE user_id = :id", {"id": 123})
```

---

## 🚀 "God Tier" Advanced Features

### 1. Visual Regression Testing
Pixel-perfect UI comparisons against baseline images.
- **Usage**: `self.app.login_page.assert_visual_match("unique_test_id")`
- **Result**: Diffs are saved in `reports/visual/diffs/` when the test fails.

### 2. Accessibility Testing (A11y)
Automated WCAG compliance scans powered by **Axe-Core**.
- **Usage**: `self.app.login_page.assert_no_accessibility_violations(impact_level="critical")`
- **Result**: Detailed violation reports in `reports/accessibility/`.

### 3. Browser Performance Monitoring

#### 📊 Captured Metrics (Navigation Timing API)
*   **`dns_lookup_time`**: Time to resolve the domain name.
*   **`connection_time`**: Time to establish TCP connection and SSL/TLS handshake.
*   **`response_time`** (TTFB): Time from request sent to first byte received.
*   **`dom_interactive_time`**: When the browser finishes parsing HTML.
*   **`dom_content_loaded_time`**: When DOM is ready and initial scripts have run.
*   **`page_load_time`**: Total time until the `load` event fires.

```python
def test_performance_dashboard(self):
    self.app.login_page.open().login()
    metrics = self.app.dashboard_page.capture_performance_metrics()
    assert metrics["page_load_time"] < 3000, "Page takes more than 3 seconds to load"
```

Reports are saved to `reports/performance/{PageName}_performance.json`.

> [!TIP]
> **CI/CD Integration**: These JSON files can be collected by data visualization tools to create performance trend dashboards over time.

### 4. Auto-Healing (Locator Self-Recovery)
**Intelligent resilience** that prevents tests from failing due to minor DOM changes.

#### 💡 How it works
When an action fails because the element is not found (`TimeoutException`), the framework activates **Auto-healing**:

1. **Failure Detection**: Driver raises `TimeoutException`.
2. **Strategy Activation**: Alternative search algorithms run based on the original locator.
3. **Fuzzy Matching**:
   - **Strategy A (Partial Attributes)**: Searches for elements whose attribute *contains* part of the value (e.g. searches `login` if original was `login-button`).
   - **Strategy B (Text Recovery)**: Finds any element that *contains* the target text.
4. **Recovery**: If a unique candidate is found, the action runs on it and a warning is logged.

```bash
[WARNING] BaseAction - [AUTO-HEALING] Primary locator ('id', 'login') failed. Attempting recovery...
[WARNING] BaseAction - [AUTO-HEALING] Successfully recovered element using fuzzy matching!
```

> [!IMPORTANT]
> Auto-healing is designed to **keep your tests alive** during unexpected changes, but does not replace code maintenance. Many auto-recovery warnings signal that locators need updating.

### 5. Proactive Notifications

#### 🛠️ Configuration (Slack / MS Teams)
```yaml
notifications:
  webhook_url: "https://hooks.slack.com/services/T000/B000/XXXX"
```

#### 🚀 Extending to Other Systems
```python
# core/utils/notifier.py
def send_telegram(self, message):
    pass  # Add Telegram API logic here

# conftest.py
def pytest_sessionfinish(session, exitstatus):
    notifier.send_telegram("Execution summary...")
```

> [!NOTE]
> Notifications are only sent if `webhook_url` is present in the config file, avoiding spam during local development.

### 6. Test Runner GUI (Web Interface)

#### 🌟 Key Features
*   **Test Tree Visualization**: Browse all `pytest` test cases hierarchically with their IDs and descriptions.
*   **Real-Time Logs**: Launch individual cases or Test Plans and watch the live execution console (SSE).
*   **Test Plans**: Select multiple test cases, combine configurations (Browser, Environment, Headless) and save as reusable plans.
*   **Media Gallery**: View all videos and screenshots generated by failed tests directly from the UI.
*   **Allure Report Management**: Generate and view your official Allure HTML report with one click.
*   **Copy Logs to Clipboard**: Easily extract console output to share with your team.

```bash
$env:PYTHONPATH = "."; python tools/test_runner/app.py
```
Open your browser at `http://localhost:5000`.

---

## 🚀 Execution & CI/CD

### 1. Basic Commands (PowerShell)
```powershell
$env:PYTHONPATH = "."; pytest
pytest --alluredir=reports
```

### 2. Dynamic Configuration (Environment Variables)

| Variable | Options | Description | Example |
| :--- | :--- | :--- | :--- |
| `ENV` | `qa`, `dev`, `uat`, `prod` | Execution environment (YAML). | `$env:ENV="dev"` |
| `BROWSER` | `chrome`, `firefox`, `edge` | Browser to use. | `$env:BROWSER="firefox"` |
| `HEADLESS` | `true`, `false` | Run without graphical interface. | `$env:HEADLESS="true"` |

```powershell
$env:ENV="qa"; $env:BROWSER="firefox"; $env:HEADLESS="true"; pytest
$env:ENV="dev"; $env:BROWSER="chrome"; $env:HEADLESS="false"; pytest
```

### 3. Local Configuration with Decorators
```python
from applications.web.demo.utils.decorators import demo

@demo   # Sets: Browser="edge", Env="qa" by default
class TestLogin(BaseTest):
    ...
```

**Resolution Priority:**
1. **Environment Variables** (Terminal): `$env:BROWSER="chrome"` (Highest priority)
2. **Class Decorator**: `@demo` sets the local default.
3. **YAML Config / Base**: Global framework values.

---

## 📊 Execution Reports (Allure)

### 1. Automatic Generation
Every `pytest` run automatically saves raw results in `/reports`.

> [!TIP]
> The framework is configured to automatically clean previous results before each new run (`--clean-alluredir`).

### 2. Report Visualization

#### Option A: Quick Script (Recommended)
```powershell
.\serve-report.bat
```

#### Option B: Using NPX (Node.js)
```bash
npx allure-commandline serve reports
```

### 3. Visual Evidence (Screenshots)
```python
self.app.screenshot("Final Evidence")
self.app.screenshot("Visible Error", full_page=False)
```

---

## 🧭 Test Lifecycle: Isolation vs. Persistence

### 1. Isolation Mode (Default)
**Each test opens and closes a new browser**. The safest mode — guarantees each test starts from scratch.

*   **Ideal for**: Independent tests, quick validations, critical regressions.
*   **Behavior**: Browser → Test 1 → Close → Browser → Test 2 → Close.

### 2. Persistent Mode (Shared Session)
Keeps **the same browser open** across all methods within the same test class. Ideal for long flows where you log in once and perform multiple sequential validations.

*   **Ideal for**: Complex dashboards, process flows (e.g. Create invoice → View report → Delete invoice).
*   **Behavior**: Browser → Test 1 → Test 2 → Test 3 → Close (at end of class).

```python
@go_hotel
class TestDashboard(BaseTest):
    persistent_session = True

    @test_case(id="HOTEL-003")
    def test_login_flow(self):
        self.app.login_page.wait_for_page_load().login()

    @test_case(id="HOTEL-004")
    def test_verify_menu(self):
        self.app.dashboard_page.click_kitchen_queue()
```

> [!IMPORTANT]
> In **Persistent Mode**, if a method fails and leaves the system in a blocked state (e.g. an open modal covering the screen), subsequent methods will likely also fail. Use wisely.

---

## 💻 VS Code Integration

### 1. Required Extensions
*   **Python (Microsoft)**: Language support, debugging and testing.
*   **Pylance**: Fast IntelliSense and typing.
*   **Allure Support**: (Optional) For visualizing Allure reports.

### 2. Initial Setup
1. **Select Interpreter**: `Ctrl+Shift+P` → `Python: Select Interpreter` → choose `.venv`.
2. **Enable Testing**: `.vscode/settings.json` already activates `pytest`. If tests are not visible, restart VS Code or click "Refresh" in the Testing tab.

### 3. How to Run (Testing Sidebar)
1. Click the **Flask (Testing)** icon in the left sidebar.
2. Navigate to `applications/web/demo/tests`.
3. **Run**: Click the **Play** button next to the test or folder.
4. **Debug**: Right-click the test and select **Debug Test**.

### 4. Advanced Debugging (F5 / Launch Profiles)
*   **Debug: Current Test**: Uses Chrome in UI mode on the open file.
*   **Run: QA - Chrome (Headless)**: Fast run without opening a browser.
*   **Run: QA - Edge (UI)**: Run on Edge for visual validation.

> [!NOTE]
> All profiles automatically inject the required `PYTHONPATH` to prevent import errors during debugging.

### 5. Native Parallelism (pytest-xdist)

```powershell
pytest applications/web/demo/tests -n auto
pytest applications/web/demo/tests -n 3
```

> [!WARNING]
> **Data Caution**: In parallel mode, tests do not run sequentially. Ensure your tests are **fully isolated and independent** to avoid database collisions.

---

### 6. GitHub Actions Pipeline (CI/CD)

#### 📁 Configuration File
`.github/workflows/python-app.yml`

#### 🛠️ Pipeline Features
1. **Automatic Execution**: Triggers on every `push` or Pull Request to `main`.
2. **Controlled Environment**: Installs Python, dependencies and configures the environment.
3. **Headless Mode**: Runs tests headlessly since GitHub servers have no graphical interface.
4. **Allure Report Generation**: Compiles raw results into an interactive web report.
5. **GitHub Pages / Artifacts**: Uploads the compiled report as a downloadable artifact or deploys to GitHub Pages.

```bash
$env:ENV="qa"; $env:HEADLESS="true"; pytest applications/web/demo/tests --alluredir=reports
```

---
*Designed by Johan Rosabal for excellence in automation.*

---

## ⚡ Quick Start Reference

### 🖥️ Test Runner GUI

The visual interface lets you browse, run and monitor tests from the browser without touching the terminal.

**Step 1 — Start the server:**
```powershell
$env:PYTHONPATH = "."; python tools/test_runner/app.py
```

**Step 2 — Open your browser:**
```
http://localhost:5000
```

**What you can do from the GUI:**

| Feature | Description |
| :--- | :--- |
| 🌲 **Test Tree** | Browse all test cases by app/feature with their IDs |
| ▶️ **Run Test** | Click Play on any test or folder to execute it |
| 📋 **Test Plans** | Group tests + choose Browser/Env/Headless and save as a plan |
| 📺 **Live Logs** | Watch real-time console output as tests run (SSE stream) |
| 🎥 **Media Gallery** | Review videos and screenshots of failed tests |
| 📊 **Allure Report** | Generate and open the full Allure report with one click |

> [!TIP]
> You can also launch the GUI from VS Code: `Ctrl+Shift+P` → `Tasks: Run Task` → **`🖥️ Runner: Launch UI`**

---

### 🖱️ Terminal Cheat Sheet

#### UI Tests
```powershell
# Run all UI tests
$env:PYTHONPATH = "."; pytest applications/web/demo/tests

# Run a specific test file
$env:PYTHONPATH = "."; pytest applications/web/demo/tests/test_login.py

# Run a specific test method
$env:PYTHONPATH = "."; pytest applications/web/demo/tests/test_login.py::TestLogin::test_valid_login

# Run with environment + browser
$env:PYTHONPATH = "."; $env:ENV="qa"; $env:BROWSER="chrome"; pytest applications/web/demo/tests

# Run headless (no browser window)
$env:PYTHONPATH = "."; $env:HEADLESS="true"; pytest applications/web/demo/tests

# Run in parallel (all CPU cores)
$env:PYTHONPATH = "."; pytest applications/web/demo/tests -n auto

# Run by tag / marker
$env:PYTHONPATH = "."; pytest applications/web/demo/tests -m smoke
```

#### API Tests
```powershell
# Run all API tests for nico_search
$env:PYTHONPATH = "."; pytest applications/api/nico_search/tests

# Run a single API test
$env:PYTHONPATH = "."; pytest applications/api/nico_search/tests/test_search.py::TestNicoSearch::test_search_by_policy_number

# Run with a specific environment
$env:PYTHONPATH = "."; $env:ENV="qa"; pytest applications/api/nico_search/tests
```

#### Reports
```powershell
# Run tests and generate Allure results
$env:PYTHONPATH = "."; pytest --alluredir=reports

# Open Allure report (Windows)
.\serve-report.bat

# Open Allure report (Node.js)
npx allure-commandline serve reports
```

#### Useful Flags
| Flag | Effect |
| :--- | :--- |
| `-v` | Verbose output — shows each test name |
| `-s` | Show `print()` output in console |
| `--tb=short` | Shorter traceback on failures |
| `-x` | Stop on first failure |
| `-k "keyword"` | Run only tests whose name contains the keyword |
| `--alluredir=reports` | Save Allure raw results to `/reports` |
| `-n auto` | Run in parallel using all CPU cores |

```powershell
# Example: verbose + stop on first failure + Allure
$env:PYTHONPATH = "."; pytest applications/web/demo/tests -v -x --alluredir=reports
```
