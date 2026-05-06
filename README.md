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

## 🔌 Recommended VS Code Extensions
- **Python (Microsoft)**: Full language support and IntelliSense.
- **Pylance**: Fast static code analysis.
- **vscode-icons**: Visual folder identification.
- **Allure Support**: In-IDE results visualization.

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
