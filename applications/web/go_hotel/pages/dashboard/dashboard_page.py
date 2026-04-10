from selenium.webdriver.common.by import By
from core.ui.common.base_page import BasePage
import allure

class DashboardPage(BasePage):
    """
    Page Object Model representing the go-hotel Dashboard Page.
    """
    
    # Locators (using data-testid for automation)
    BUTTON_BACK = (By.XPATH, "//a[@data-testid='topnav-back-link']")
    DIV_USER_MENU = (By.XPATH, "//button[@data-testid='usermenu-action-button']")
    DIV_LOGOUT = (By.XPATH, "//span[text()='Cerrar Sesión']/..")
    # ---------------------------------------------------------------------------------
    # Centros de Preparación 
    # ---------------------------------------------------------------------------------
    DIV_COLA_COCINA = (By.XPATH, "//h3[text()='Cola de Cocina']/../..")
    DIV_COLA_BAR = (By.XPATH, "//h3[text()='Cola de Bar']/../..")

    # ---------------------------------------------------------------------------------
    # Operaciones Principales 
    # ---------------------------------------------------------------------------------
    DIV_VENTA_DIRECTA_POS = (By.XPATH, "//h3[text()='Venta Directa (POS)']/../..")
    DIV_CREAR_RESERVACIONES = (By.XPATH, "//h3[text()='Crear Reservaciones']/../..")
    DIV_PANEL_HABITACIONES = (By.XPATH, "//h3[text()='Panel de Habitaciones']/../..")
    DIV_COLA_LIMPIEZA = (By.XPATH, "//h3[text()='Cola de Limpieza']/../..")
    DIV_GESTION_CLIENTES = (By.XPATH, "//h3[text()='Gestión de Clientes']/../..")
    DIV_GESTION_INVENTARIO = (By.XPATH, "//h3[text()='Gestión de Inventario']/../..")

    # ---------------------------------------------------------------------------------
    # Marketing y Visualización
    # ---------------------------------------------------------------------------------
    DIV_MENU_DIGITAL_TV = (By.XPATH, "//h3[text()='Menú Digital (TV)']/../..")
    DIV_AUTO_PEDIDO_MOVIL = (By.XPATH, "//h3[text()='Auto-Pedido (Móvil)']/../..")
    DIV_CENTRO_MARKETING = (By.XPATH, "//h3[text()='Centro de Marketing']/../..")
    DIV_SITIO_WEB_PUBLICO = (By.XPATH, "//h3[text()='Sitio Web Público']/../..")

    # ---------------------------------------------------------------------------------
    # Finanzas y Contabilidad
    # ---------------------------------------------------------------------------------
    DIV_FACTURACION = (By.XPATH, "//h3[text()='Facturación']/../..")
    DIV_REGISTRAR_COMPRAS = (By.XPATH, "//h3[text()='Registrar Compras']/../..")
    DIV_REPORTES_ESTADISTICAS = (By.XPATH, "//h3[text()='Reportes y Estadísticas']/../..")
    DIV_REGISTRO_ESTANCIAS = (By.XPATH, "//h3[text()='Registro de Estancias']/../..")
    DIV_GESTION_SINPE = (By.XPATH, "//h3[text()='Gestión de SINPE']/../..")
    DIV_GESTION_PROVEEDORES = (By.XPATH, "//h3[text()='Gestión de Proveedores']/../..")

    # ---------------------------------------------------------------------------------
    # Administración y Seguridad
    # ---------------------------------------------------------------------------------
    DIV_AJUSTES_SISTEMA = (By.XPATH, "//h3[text()='Ajustes del Sistema']/../..")
    DIV_GESTION_USUARIOS = (By.XPATH, "//h3[text()='Gestión de Usuarios']/../..")
    DIV_GESTION_TUTORIALES = (By.XPATH, "//h3[text()='Gestión de Tutoriales']/../..")

    # ---------------------------------------------------------------------------------
    # Ayuda y Recursos
    # ---------------------------------------------------------------------------------
    DIV_MANUAL_OPERATIVO = (By.XPATH, "//h3[text()='Manual Operativo']/../..")
    DIV_DOCUMENTACION_TECNICA = (By.XPATH, "//h3[text()='Documentación Técnica']/../..")
    DIV_CENTRO_AYUDA = (By.XPATH, "//h3[text()='Centro de Ayuda']/../..")
    DIV_TUTORIALES_APRENDIZAJE = (By.XPATH, "//h3[text()='Tutoriales y Aprendizaje']/../..")

    @allure.step("Waiting for page load")
    def wait_for_page_load(self):
        self.navigation.go(url="dashboard")
        self.elements.wait_for_page_load()
        self.window.set_zoom_level(100)
        return self

    @allure.step("Validating URL contains: {url}")
    def assert_pos_url(self, url: str):
        self.navigation.wait_url_contains(url)
        current_url = self.navigation.get_current_url()
        assert url in current_url, f"URL actual: {current_url} no contiene {url}"
        return self

    # ---------------------------------------------------------------------------------
    # Centros de Preparación 
    # ---------------------------------------------------------------------------------
    @allure.step("Clicking on Cola de Cocina")
    def click_cola_cocina(self):
        self.element(self.DIV_COLA_COCINA).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("kitchen")
        return self

    @allure.step("Clicking on Cola de Bar")
    def click_cola_bar(self):
        self.element(self.DIV_COLA_BAR).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("bar")
        return self

    # ---------------------------------------------------------------------------------
    # Operaciones Principales 
    # ---------------------------------------------------------------------------------
    @allure.step("Clicking on Venta Directa (POS)")
    def click_venta_directa_pos(self):
        self.element(self.DIV_VENTA_DIRECTA_POS).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("pos")
        return self

    @allure.step("Clicking on Crear Reservaciones")
    def click_crear_reservaciones(self):
        self.element(self.DIV_CREAR_RESERVACIONES).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("reservations")
        return self

    @allure.step("Clicking on Panel de Habitaciones")
    def click_panel_habitaciones(self):
        self.element(self.DIV_PANEL_HABITACIONES).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("rooms")
        return self

    @allure.step("Clicking on Cola de Limpieza")
    def click_cola_limpieza(self):
        self.element(self.DIV_COLA_LIMPIEZA).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("cleaning")
        return self

    @allure.step("Clicking on Gestión de Clientes")
    def click_gestion_clientes(self):
        self.element(self.DIV_GESTION_CLIENTES).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("clients")
        return self

    # ---------------------------------------------------------------------------------
    # Marketing y Visualización
    # ---------------------------------------------------------------------------------
    @allure.step("Clicking on Gestión de Inventario")
    def click_gestion_inventario(self):
        self.element(self.DIV_GESTION_INVENTARIO).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("inventory")
        return self

    @allure.step("Clicking on Menú Digital (TV)")
    def click_menu_digital_tv(self):
        self.element(self.DIV_MENU_DIGITAL_TV).click()
        self.elements.wait_for_page_load()
        self.window.to_tab(index=1)
        self.assert_pos_url("public/menu")
        self.window.switch_to_main()
        return self

    @allure.step("Clicking on Auto-Pedido (Móvil)")
    def click_auto_pedido_movil(self):
        self.element(self.DIV_AUTO_PEDIDO_MOVIL).click()
        self.elements.wait_for_page_load()
        self.window.to_tab(index=2)
        self.assert_pos_url("/public/order")
        self.window.switch_to_main()
        return self

    @allure.step("Clicking on Centro de Marketing")
    def click_centro_marketing(self):
        self.element(self.DIV_CENTRO_MARKETING).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("marketing")
        return self

    @allure.step("Clicking on Sitio Web Público")
    def click_sitio_web_publico(self):
        self.element(self.DIV_SITIO_WEB_PUBLICO).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url(self.base_url)
        return self

    # ---------------------------------------------------------------------------------
    # Finanzas y Contabilidad
    # ---------------------------------------------------------------------------------
    @allure.step("Clicking on Facturación")
    def click_facturacion(self):
        self.element(self.DIV_FACTURACION).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("billing/invoices")
        return self

    @allure.step("Clicking on Registrar Compras")
    def click_registrar_compras(self):
        self.element(self.DIV_REGISTRAR_COMPRAS).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("purchases")
        return self

    @allure.step("Clicking on Reportes y Estadísticas")
    def click_reportes_estadisticas(self):
        self.element(self.DIV_REPORTES_ESTADISTICAS).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("reports")
        return self

    @allure.step("Clicking on Registro de Estancias")
    def click_registro_estancias(self):
        self.element(self.DIV_REGISTRO_ESTANCIAS).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("reports/stays")
        return self

    @allure.step("Clicking on Gestión de SINPE")
    def click_gestion_sinpe(self):
        self.element(self.DIV_GESTION_SINPE).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("settings/sinpe-accounts")
        return self

    @allure.step("Clicking on Gestión de Proveedores")
    def click_gestion_proveedores(self):
        self.element(self.DIV_GESTION_PROVEEDORES).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("suppliers")
        return self

    # ---------------------------------------------------------------------------------
    # Administración y Seguridad
    # ---------------------------------------------------------------------------------
    @allure.step("Clicking on Ajustes del Sistema")
    def click_ajustes_sistema(self):
        self.element(self.DIV_AJUSTES_SISTEMA).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("settings")
        return self

    @allure.step("Clicking on Gestión de Usuarios")
    def click_gestion_usuarios(self):
        self.element(self.DIV_GESTION_USUARIOS).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("users")
        return self

    @allure.step("Clicking on Gestión de Tutoriales")
    def click_gestion_tutoriales(self):
        self.element(self.DIV_GESTION_TUTORIALES).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("dashboard/tutorials/manage")
        return self

    # ---------------------------------------------------------------------------------
    # Ayuda y Recursos
    # ---------------------------------------------------------------------------------
    @allure.step("Clicking on Manual Operativo")
    def click_manual_operativo(self):
        self.element(self.DIV_MANUAL_OPERATIVO).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("manual/operations")
        return self

    @allure.step("Clicking on Documentación Técnica")
    def click_documentacion_tecnica(self):
        self.element(self.DIV_DOCUMENTACION_TECNICA).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("manual/project-docs")
        return self

    @allure.step("Clicking on Centro de Ayuda")
    def click_centro_ayuda(self):
        self.element(self.DIV_CENTRO_AYUDA).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("help-center")
        return self

    @allure.step("Clicking on Tutoriales y Aprendizaje")
    def click_tutoriales_aprendizaje(self):
        self.element(self.DIV_TUTORIALES_APRENDIZAJE).click()
        self.elements.wait_for_page_load()
        self.assert_pos_url("manual/tutorials")
        return self

    
    # ---------------------------------------------------------------------------------
    # Botones de Navegación
    # ---------------------------------------------------------------------------------    
    @allure.step("Clicking on Botón de Retroceso")
    def click_boton_retroceso(self):
        self.element(self.BUTTON_BACK).click()
        return self

    @allure.step("Clicking on User Menu")
    def click_user_menu(self):
        self.element(self.DIV_USER_MENU).click()
        return self

    @allure.step("Clicking on Logout")
    def click_logout(self):
        self.element(self.DIV_LOGOUT).click()
        return self

    @allure.step("Closing session")
    def click_cerrar_sesion(self):
        self.click_user_menu().click_logout()
        return self    

