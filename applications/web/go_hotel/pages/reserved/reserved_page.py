from selenium.webdriver.common.by import By
from core.ui.common.base_page import BasePage
import allure

class ReservedPage(BasePage):
    """
    Page Object Model representing the go-hotel Reserved Page.
    """
    
    # Locators (using data-testid for automation)
    INPUT_SEARCH = (By.XPATH, "//input[contains(@data-testid,'search')]")
    BUTTON_NEW_CLIENT = (By.XPATH, "//button[contains(@data-testid,'add-client')]")
    BUTTON_NEW_RESERVATION = (By.XPATH, "//button[contains(@data-testid,'add-reservation')]")
    TAB_TODOS = (By.XPATH, "//button[text()='Todas']")
    TAB_POR_INGRESAR = (By.XPATH, "//button[text()='Por Ingresar']")
    TAB_EN_HABITACION = (By.XPATH, "//button[text()='En Habitación']")
    TAB_FINALIZADAS = (By.XPATH, "//button[text()='Finalizadas']")
    TAB_CANCELADAS = (By.XPATH, "//button[text()='Canceladas']")
    TAB_NO_SE_PRESENTO = (By.XPATH, "//button[text()='No se presentó']")

    VIEW_TARJETAS = (By.XPATH, "//button[text()='Tarjetas']")
    VIEW_AGENDA = (By.XPATH, "//button[text()='Agenda']")
    VIEW_LISTA = (By.XPATH, "//button[text()='Lista']")

    DIV_NO_FOUND_RECORDS = (By.XPATH, "//div[text()='No se encontraron reservaciones con los filtros actuales.']")

    @allure.step("Waiting for page load")
    def wait_for_page_load(self):
        self.navigation.go(url="reservations")
        self.elements.wait_for_page_load()
        self.window.set_zoom_level(100)
        return self
    
    def enter_search(self, search: str):
        self.element(self.INPUT_SEARCH).clear().type(search)
        return self

    def clear_search(self):
        self.element(self.INPUT_SEARCH).physical_clear()
        return self

    def click_new_client(self):
        self.element(self.BUTTON_NEW_CLIENT).click()
        return self

    def click_new_reservation(self):
        self.element(self.BUTTON_NEW_RESERVATION).click()
        return self

    def click_tab_todos(self):
        self.element(self.TAB_TODOS).click().pause(seconds=3)
        return self

    def click_tab_por_ingresar(self):
        self.element(self.TAB_POR_INGRESAR).click().pause(seconds=3)
        return self

    def click_tab_en_habitacion(self):
        self.element(self.TAB_EN_HABITACION).click().pause(seconds=3)
        return self

    def click_tab_finalizadas(self):
        self.element(self.TAB_FINALIZADAS).click().pause(seconds=3)
        return self

    def click_tab_canceladas(self):
        self.element(self.TAB_CANCELADAS).click().pause(seconds=3)
        return self

    def click_tab_no_se_presento(self):
        self.element(self.TAB_NO_SE_PRESENTO).click().pause(seconds=3)
        return self

    def click_view_tarjetas(self):
        self.element(self.VIEW_TARJETAS).click().pause(seconds=3)
        return self

    def click_view_agenda(self):
        self.element(self.VIEW_AGENDA).click().pause(seconds=3)
        return self

    def click_view_lista(self):
        self.element(self.VIEW_LISTA).click().pause(seconds=3)
        return self 