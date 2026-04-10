from selenium.webdriver.common.by import By
from core.ui.common.base_page import BasePage
import allure

class NewClientComponent(BasePage):
    """
    Page Object Model representing the go-hotel New Client Component.
    """

    # Locators (using data-testid for automation)
    MODAL = (By.XPATH, "//div[@role='dialog']")
    TITLE_PAGE = (By.XPATH, "//h2")
    INPUT_CEDULA = (By.XPATH, "//label[text()='Cédula']/..//input")
    BUTTON_VERIFICAR = (By.XPATH, "//button[text()='Verificar']")

    INPUT_NAME = (By.XPATH, "//label[text()='Nombre']/..//input")
    INPUT_LAST_NAME = (By.XPATH, "//label[text()='Primer Apellido']/..//input")
    INPUT_SECOND_LAST_NAME = (By.XPATH, "//label[text()='Segundo Apellido (Opcional)']/..//input")

    INPUT_EMAIL = (By.XPATH, "//label[text()='Correo Electrónico']/..//input")
    INPUT_PHONE = (By.XPATH, "//label[text()='Teléfono']/..//input")

    INPUT_NOTES = (By.XPATH, "//label[text()='Notas Internas']/..//textarea")

    BUTTON_VIP = (By.XPATH, "//label[text()='Cliente VIP / Favorito']/../..//button")
   
    BUTTON_SAVE = (By.XPATH, "//button[text()='Crear Cliente']")
    BUTTON_CANCEL = (By.XPATH, "//button[text()='Cancelar']")

    @allure.step("Waiting for page load")
    def wait_for_page_load(self):
        self.navigation.go(url="clients/new")
        self.elements.wait_for_page_load()
        return self

    def is_visible_modal(self) -> bool:
        """
        Checks if the modal is visible.
        """
        return self.element(self.MODAL).is_visible()

    def is_visible_title(self) -> bool:
        """
        Checks if the page is loaded by verifying the title.
        """
        return self.element(self.TITLE_PAGE).is_visible()
    
    def get_titulo(self) -> str:
        """
        Gets the title of the page.
        """
        return self.element(self.TITLE_PAGE).get_text()

    def enter_cedula(self, cedula: str):
        """
        Enters the cedula in the input field.
        """
        self.element(self.INPUT_CEDULA).type(cedula)
        return self
    
    def click_verificar(self):
        """
        Clicks the verify button.
        """
        self.element(self.BUTTON_VERIFICAR).click()
        return self
    
    def enter_nombre(self, name: str):
        """
        Enters the name in the input field.
        """
        self.element(self.INPUT_NAME).type(name)
        return self
    
    def enter_primer_apellido(self, last_name: str):
        """
        Enters the last name in the input field.
        """
        self.element(self.INPUT_LAST_NAME).type(last_name)
        return self
    
    def enter_segundo_apellido(self, second_last_name: str):
        """
        Enters the second last name in the input field.
        """
        self.element(self.INPUT_SECOND_LAST_NAME).type(second_last_name)
        return self
    
    def enter_email(self, email: str):
        """
        Enters the email in the input field.
        """
        self.element(self.INPUT_EMAIL).type(email)
        return self
    
    def enter_telefono(self, phone: str):
        """
        Enters the phone in the input field.
        """
        self.element(self.INPUT_PHONE).type(phone)
        return self
    
    def enter_notas(self, notes: str):
        """
        Enters the notes in the input field.
        """
        self.element(self.INPUT_NOTES).type(notes)
        return self
    
    def click_vip(self):
        """
        Clicks the vip button.
        """
        self.element(self.BUTTON_VIP).click()
        return self
    
    def click_crear(self):
        """
        Clicks the save button.
        """
        self.element(self.BUTTON_SAVE).click()
        return self
    
    def click_cancelar(self):
        """
        Clicks the cancel button.
        """
        self.element(self.BUTTON_CANCEL).click()
        return self 
    
    def crear_cliente(self, client: dict, verify: bool = False, save: bool = True):
        """
        Creates a new client.
        """
        # Sincronización: Esperar a que el modal sea visible antes de empezar
        self.element(self.MODAL).wait_visible(timeout=5)

        self.enter_cedula(client["cedula"])

        # Verificar si el cliente existe
        if verify:
            self.click_verificar()

        # Completar 
        self.enter_nombre(client["name"])
        self.enter_primer_apellido(client["last_name"])
        self.enter_segundo_apellido(client["second_last_name"])
        self.enter_email(client["email"])
        self.enter_telefono(client["phone"])
        self.enter_notas(client["notes"])
        self.click_vip()
        
        if save:
            self.click_crear()
        else:
            self.click_cancelar()
        
        return self