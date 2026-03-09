from typing import Union
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from core.ui.actions.base_action import BaseAction
import allure

class TableActions(BaseAction):
    """
    Specialized component for interacting with HTML Table and Grid structures.

    Provides indexed access to cells and row counting, simplifying 
    dynamic table validation.
    """
    def _get_column_index(self, column: Union[int, str]) -> int:
        """
        Resolves a column identifier (index or name) to its 1-based index.

        Args:
            column (Union[int, str]): 1-based index or column header text.

        Returns:
            int: The 1-based column index.
        """
        if isinstance(column, int):
            return column
        
        headers = self.get_headers()
        try:
            # Adding 1 because list index is 0-based and table index is 1-based
            index = headers.index(column) + 1
            self.logger.info(f"Resolved column '{column}' to index {index}")
            return index
        except ValueError:
            self.logger.error(f"Column name '{column}' not found in table headers: {headers}")
            raise ValueError(f"Column '{column}' not found.")

    def get_cell_text(self, row: int, col: Union[int, str]) -> str:
        """
        Retrieves the text from a specific cell within a table.

        Args:
            row (int): The 1-based row index.
            col (Union[int, str]): The 1-based column index or column name.

        Returns:
            str: The visible text of the cell.
        """
        try:
            target_col = self._get_column_index(col)
            xpath = f".//tr[{row}]/td[{target_col}]"
            self._find_element()
            cell = self._element.find_element(By.XPATH, xpath)
            return cell.text
        except Exception as e:
            self._handle_exception(e, "get_cell_text")
    @allure.step("Getting table headers")
    def get_headers(self) -> list[str]:
        """
        Retrieves the visible text of all table headers (<th>).

        Returns:
            list[str]: A list of header names.
        """
        try:
            self._find_element()
            headers = self._element.find_elements(By.TAG_NAME, "th")
            texts = [h.text for h in headers]
            self.logger.info(f"Table headers found: {texts}")
            return texts
        except Exception as e:
            self._handle_exception(e, "get_headers")

    @allure.step("Clicking table header")
    def click_header(self, text: str = None, index: int = None):
        """
        Clicks a table header by text content or 1-based index.

        Args:
            text (str, optional): The exact text of the header.
            index (int, optional): The 1-based index of the header.

        Returns:
            TableActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            headers = self._element.find_elements(By.TAG_NAME, "th")
            target = None

            if text:
                for h in headers:
                    if h.text == text:
                        target = h
                        break
            elif index is not None:
                if 1 <= index <= len(headers):
                    target = headers[index-1]

            if target:
                self.logger.info(f"Clicking header: {target.text}")
                target.click()
            else:
                self.logger.error(f"Header not found (Text: {text}, Index: {index})")
            
            return self
        except Exception as e:
            self._handle_exception(e, "click_header")

    @allure.step("Getting all table data")
    def get_all_data(self) -> list[dict]:
        """
        Extracts all table data into a list of dictionaries.
        Assumes the first row or <th> elements represent the keys.

        Returns:
            list[dict]: List of row data as dictionaries.
        """
        try:
            self._find_element()
            headers = self.get_headers()
            rows = self._element.find_elements(By.TAG_NAME, "tr")
            
            # If no <th> found, use the first <tr> as headers? 
            # For now, let's assume <th> exists as per standard practice or 
            # Fallback to generic Col1, Col2...
            if not headers:
                first_row_cells = rows[0].find_elements(By.TAG_NAME, "td")
                headers = [f"Column{i+1}" for i in range(len(first_row_cells))]

            data = []
            # Skip header row if it's the first <tr>
            start_index = 1 if self._element.find_elements(By.TAG_NAME, "th") else 0
            
            for r in rows[start_index:]:
                cells = r.find_elements(By.TAG_NAME, "td")
                if cells:
                    row_data = {headers[i]: cells[i].text for i in range(min(len(headers), len(cells)))}
                    data.append(row_data)
            
            self.logger.info(f"Extracted {len(data)} rows from table.")
            return data
        except Exception as e:
            self._handle_exception(e, "get_all_data")

    @allure.step("Checking all rows in table (Column {column})")
    def check_all(self, column: Union[int, str] = 1):
        """
        Interacts with the 'Select All' checkbox.

        Args:
            column (Union[int, str]): The 1-based column index or name. 
                                     Defaults to 1.

        Returns:
            TableActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            target_col = self._get_column_index(column)
            # Finds the checkbox in the specified column header or first row cell
            xpath = f"(.//th[{target_col}]|.//tr[1]/td[{target_col}])//input[@type='checkbox']"
            checkbox = self._element.find_element(By.XPATH, xpath)
            if not checkbox.is_selected():
                checkbox.click()
                self.logger.info(f"Checked 'Select All' checkbox in column {column}.")
            return self
        except Exception as e:
            self._handle_exception(e, "check_all")

    @allure.step("Checking row {index} (Column {column})")
    def check_row(self, index: int, column: Union[int, str] = 1):
        """
        Clicks the checkbox for a specific row and column.

        Args:
            index (int): The 1-based row index.
            column (Union[int, str]): The 1-based column index or name. Defaults to 1.

        Returns:
            TableActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            target_col = self._get_column_index(column)
            # Finds the checkbox input within the specific row and column cell
            xpath = f".//tr[{index}]/td[{target_col}]//input[@type='checkbox']"
            checkbox = self._element.find_element(By.XPATH, xpath)
            if not checkbox.is_selected():
                checkbox.click()
                self.logger.info(f"Checked checkbox for row {index}, column {column}.")
            return self
        except Exception as e:
            self._handle_exception(e, "check_row")

    @allure.step("Clicking button in row {row}, col {col} (Filter: {text})")
    def click_button_in_cell(self, row: int, col: Union[int, str], text: str = None):
        """
        Clicks a button inside a specific table cell.

        Args:
            row (int): 1-based row index.
            col (Union[int, str]): 1-based column index or name.
            text (str, optional): Visible text or value to filter if multiple 
                                  buttons exist.

        Returns:
            TableActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            target_col = self._get_column_index(col)
            # Heuristic: Find <button> or <input type='button/submit'>
            if text:
                xpath = f".//tr[{row}]/td[{target_col}]//*[(self::button or (self::input and (@type='button' or @type='submit'))) and (contains(text(), '{text}') or contains(@value, '{text}'))]"
            else:
                xpath = f".//tr[{row}]/td[{target_col}]//*[self::button or (self::input and (@type='button' or @type='submit'))]"
            
            button = self._element.find_element(By.XPATH, xpath)
            self.logger.info(f"Clicking button in cell ({row}, {col}) with filter '{text}'")
            button.click()
            return self
        except Exception as e:
            self._handle_exception(e, "click_button_in_cell")

    @allure.step("Clicking link in row {row}, col {col} (Filter: {text})")
    def click_link_in_cell(self, row: int, col: Union[int, str], text: str = None):
        """
        Clicks a link (<a>) inside a specific table cell.

        Args:
            row (int): 1-based row index.
            col (Union[int, str]): 1-based column index or name.
            text (str, optional): Visible text to filter if multiple links exist.

        Returns:
            TableActions: The current instance for method chaining.
        """
        try:
            self._find_element()
            target_col = self._get_column_index(col)
            if text:
                xpath = f".//tr[{row}]/td[{target_col}]//a[contains(text(), '{text}')]"
            else:
                xpath = f".//tr[{row}]/td[{target_col}]//a"
            
            link = self._element.find_element(By.XPATH, xpath)
            self.logger.info(f"Clicking link in cell ({row}, {col}) with filter '{text}'")
            link.click()
            return self
        except Exception as e:
            self._handle_exception(e, "click_link_in_cell")

    @allure.step("Waiting for table to have {expected_count} rows")
    def wait_for_rows(self, expected_count: int, timeout: int = None):
        """
        Wait until the number of rows in the table matches the expected count.

        Args:
            expected_count (int): The number of rows to wait for.
            timeout (int, optional): Custom timeout for this wait.

        Returns:
            TableActions: The current instance for method chaining.
        """
        wait = self.at(timeout)._get_wait() if timeout else self._get_wait()
        try:
            wait.until(lambda d: self.get_row_count() == expected_count)
            self.logger.info(f"Table now has {expected_count} rows.")
            return self
        except Exception as e:
            self._handle_exception(e, "wait_for_rows")

    @allure.step("Waiting for table to not be empty")
    def wait_not_empty(self, timeout: int = None):
        """
        Wait until the table contains at least one data row.

        Args:
            timeout (int, optional): Custom timeout for this wait.

        Returns:
            TableActions: The current instance for method chaining.
        """
        wait = self.at(timeout)._get_wait() if timeout else self._get_wait()
        try:
            # Assuming row_count > 1 because row 1 is likely header
            # Adjust if table has different structure
            wait.until(lambda d: self.get_row_count() > 1)
            self.logger.info("Table is no longer empty.")
            return self
        except Exception as e:
            self._handle_exception(e, "wait_not_empty")
