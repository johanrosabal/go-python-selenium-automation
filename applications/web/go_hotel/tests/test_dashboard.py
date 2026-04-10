from core.ui.common.base_test import BaseTest
from applications.web.go_hotel.config.decorators.app_decorators import go_hotel
from applications.web.go_hotel.app.go_hotel_app import GoHotelApp
from core.utils.decorators import test_case

@go_hotel
class TestDashboard(BaseTest):
    """
    Test suite for validating Dashboard navigation and modules.
    Uses persistent_session = True to maintain login across all methods.
    """
    persistent_session = True
    app: GoHotelApp

    @test_case(id="HOTEL-003")
    def test_01_login_and_preparation_centers(self, logged_in):
        """Step 1: Check Preparation Centers (Kitchen & Bar)."""
        # Login ya manejado por el fixture
        self.app.dashboard_page.click_cola_cocina().click_boton_retroceso()
        self.app.dashboard_page.click_cola_bar().click_boton_retroceso()

    @test_case(id="HOTEL-003-B")
    def test_02_main_operations(self):
        """Step 2: Verify Main Operations (POS, Reservations, Rooms, etc)."""
        # Note: We are already logged in here!
        self.app.dashboard_page.click_venta_directa_pos().click_boton_retroceso()
        self.app.dashboard_page.click_crear_reservaciones().click_boton_retroceso()
        self.app.dashboard_page.click_panel_habitaciones().click_boton_retroceso()
        self.app.dashboard_page.click_cola_limpieza().click_boton_retroceso()
        self.app.dashboard_page.click_gestion_clientes().click_boton_retroceso()
        self.app.dashboard_page.click_gestion_inventario().click_boton_retroceso()

    @test_case(id="HOTEL-003-C")
    def test_03_finance_and_admin(self):
        """Step 3: Verify Finance, Admin, and Help modules."""
        self.app.dashboard_page.click_centro_marketing().click_boton_retroceso()
        self.app.dashboard_page.click_facturacion().click_boton_retroceso()
        self.app.dashboard_page.click_registrar_compras().click_boton_retroceso()
        self.app.dashboard_page.click_reportes_estadisticas().click_boton_retroceso()
        self.app.dashboard_page.click_registro_estancias().click_boton_retroceso()
        self.app.dashboard_page.click_gestion_sinpe().click_boton_retroceso()
        self.app.dashboard_page.click_gestion_proveedores().click_boton_retroceso()
        self.app.dashboard_page.click_ajustes_sistema().click_boton_retroceso()
        self.app.dashboard_page.click_gestion_usuarios().click_boton_retroceso()
        self.app.dashboard_page.click_gestion_tutoriales().click_boton_retroceso()
        self.app.dashboard_page.click_manual_operativo().click_boton_retroceso()
        self.app.dashboard_page.click_documentacion_tecnica().click_boton_retroceso()
        self.app.dashboard_page.click_centro_ayuda().click_boton_retroceso()
        self.app.dashboard_page.click_tutoriales_aprendizaje().click_boton_retroceso()
        
    @test_case(id="HOTEL-003-EXIT")
    def test_04_logout(self):
        """Step 4: Close session properly."""
        self.app.dashboard_page.click_cerrar_sesion()