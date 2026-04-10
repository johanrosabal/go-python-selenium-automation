# Detailed Actions Mapping by Class

This document lists all logic methods available in the specialized action classes and their exposure through the `UIElement` facade. After the recent homogenization refactor, almost all methods have a **1:1 mapping** in naming.

---

## 🏗️ ClickActions
*Logic for mouse interactions and low-level click events.*

| Logic Method | UIElement Method | Exposed? | Description |
|:---|:---|:---:|:---|
| `click()` | `click()` | ✅ | Standard Selenium click. |
| `double_click()` | `double_click()` | ✅ | Performs a double-click. |
| `right_click()` | `right_click()` | ✅ | Contextual right-click. |
| `hover()` | `hover()` | ✅ | Moves mouse over element. |
| `js_click()` | `js_click()` | ✅ | Direct click via JS executing. |
| `click_and_hold()` | `click_and_hold()` | ✅ | Maintains click pressure. |
| `release_mouse()` | `release_mouse()` | ✅ | Releases mouse button. |
| `drag_and_drop()` | `drag_and_drop()` | ✅ | Moves element to target locator. |

---

## ⌨️ SendKeysActions
*Logic for keyboard inputs and text manipulation.*

| Logic Method | UIElement Method | Exposed? | Description |
|:---|:---|:---:|:---|
| `type()` | `type()` | ✅ | Clears and types text. |
| `type_encrypted()` | `type_encrypted()` | ✅ | Secure typing (masked in logs). |
| `type_js()` | `type_js()` | ✅ | Set 'value' via JS. |
| `type_by_character()`| `type_by_character()` | ✅ | Slow human-like typing. |
| `get_value()` | `get_value()` | ✅ | Retrieves 'value' attribute. |
| `clear()` | `clear()` | ✅ | Standard `.clear()` call. |
| `physical_clear()` | `physical_clear()` | ✅ | CTRL+A + BACKSPACE (React safe). |
| `press()` | `press()` | ✅ | Generic key stroke. |
| `press_enter()` | `press_enter()` | ✅ | Specific ENTER stroke. |
| `press_tab()` | `press_tab()` | ✅ | Specific TAB stroke. |

---

## 📊 TableActions
*Specialized logic for HTML tables and data grids.*

| Logic Method | UIElement Method | Exposed? | Description |
|:---|:---|:---:|:---|
| `get_cell_text()` | `get_cell_text()` | ✅ | Text at (row, col) coordinates. |
| `get_row_count()` | `get_row_count()` | ✅ | Returns total number of <tr>. |
| `get_table_headers()` | `get_table_headers()` | ✅ | Returns list of <th> texts. |
| `get_table_data()` | `get_table_data()` | ✅ | Entire table as list of dicts. |
| `table_check_all()` | `table_check_all()` | ✅ | Toggles global table checkbox. |
| `table_check_row()` | `table_check_row()` | ✅ | Toggles specific row checkbox. |
| `table_click_button()` | `table_click_button()`| ✅ | Click nested button in cell. |
| `table_click_link()` | `table_click_link()`| ✅ | Click nested link in cell. |
| `table_wait_for_rows()` | `table_wait_for_rows()`| ✅ | Wait for row count to match. |
| `table_wait_not_empty()`| `table_wait_not_empty()`| ✅ | Wait for at least one data row. |

---

## 👁️ ElementsActions
*Logic for state checks, visibility, and explicit waits.*

| Logic Method | UIElement Method | Exposed? | Description |
|:---|:---|:---:|:---|
| `is_visible()` | `is_visible()` | ✅ | Instant check for visibility. |
| `wait_visible()` | `wait_visible()` | ✅ | Explicit Wait for visibility. |
| `wait_clickable()` | `wait_clickable()` | ✅ | Wait for enabled + visible. |
| `wait_disappear()` | `wait_disappear()` | ✅ | Wait for element removal. |
| `wait_present()` | `wait_present()` | ✅ | Check if exists in DOM. |
| `is_enabled()` | `is_enabled()` | ✅ | Check if element is enabled. |
| `is_clickable()` | `is_clickable()` | ✅ | Check if currently clickable. |
| `get_css_value()` | `get_css_value()` | ✅ | Returns specific CSS property. |
| `set_css_value()` | `set_css_value()` | ✅ | Force CSS property via JS. |
| `wait_for_text()` | (In progress) | ❌ | Wait for string inside element. |

---

## ⏺️ Form Actions (Check/Radio/Dropdown)

| Class | Method | UIElement Method | Exposed? |
|:---|:---|:---|:---:|
| **CheckActions** | `check()` | `check()` | ✅ |
| **CheckActions** | `is_checked()` | `is_checked()` | ✅ |
| **RadioActions** | `select_radio()` | `select_radio()` | ✅ |
| **RadioActions** | `is_selected()` | `is_selected()` | ✅ |
| **DropdownActions** | `select_by_text()`| `select_by_text()` | ✅ |
| **DropdownActions** | `select_by_value()`| `select_by_value()` | ✅ |
| **DropdownActions** | `select_by_index()`| `select_by_index()` | ✅ |
| **DropdownActions** | `get_options()` | `get_dropdown_options()`| ✅ |

---

## 🛠️ Utilities (Scroll/Upload/Screenshot)

| Class | Method | UIElement Method | Exposed? |
|:---|:---|:---|:---:|
| **ScrollActions** | `scroll_to()` | `scroll_to()` | ✅ |
| **ScrollActions** | `scroll_to_center()`| `scroll_to_center()` | ✅ |
| **GetTextActions** | `get_text()` | `get_text()` | ✅ |
| **GetTextActions** | `get_trimmed_text()`| `get_trimmed_text()` | ✅ |
| **UploadActions** | `upload_file()` | `upload_file()` | ✅ |
| **ScreenshotActions**| `screenshot()` | `screenshot()` | ✅ |

---
*Documented to ensure 100% coverage between internal components and public API.*
