# Page Object Creation Standards

To ensure consistency, readability, and high maintainability across the enterprise automation framework, all Page Objects must follow these strict rules:

## 1. Granular Methods for Locators
Every locator defined in a Page Object **MUST** have its own dedicated interaction method. 

**Rule:** One Locator = One Method.

*   **Property Methods:** Methods for inputs should be named like `enter_[field_name]`.
*   **Action Methods:** Methods for buttons/links should be named like `click_[element_name]`.
*   **Verification Methods:** Methods for checking visibility or text should be named like `is_[element]_visible` or `get_[element]_text`.

## 2. Method Chaining (Fluent Interface)
All interaction methods **MUST** return `self` to maintain the fluent interface pattern.

## 3. Composite Methods
High-level interactions (like `login`, `search_product`, `complete_checkout`) **MUST** be built by reusing the granular methods. This ensures that changes to a single element's interaction only need to be updated in one place.

## Example Pattern

```python
class ExamplePage(BasePage):
    # Locators
    SEARCH_INPUT = (By.ID, "search")
    SEARCH_BUTTON = (By.ID, "submit")

    # Granular Methods
    def enter_search_term(self, term):
        self.send_keys.text(self.SEARCH_INPUT, term)
        return self

    def click_search(self):
        self.click.element(self.SEARCH_BUTTON)
        return self

    # Composite Method
    def perform_search(self, term):
        return self.enter_search_term(term).click_search()
```
