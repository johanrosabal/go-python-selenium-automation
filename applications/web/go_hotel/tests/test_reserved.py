import pytest
from core.ui.common.base_test import BaseTest
from applications.web.go_hotel.config.decorators.app_decorators import go_hotel
from applications.web.go_hotel.app.go_hotel_app import GoHotelApp
from core.utils.decorators import test_case

@go_hotel
class TestReserved(BaseTest):
    """
    Test suite for validating Reservation management.
    Uses persistent_session = True to maintain state across methods.
    """
    persistent_session = True
    app: GoHotelApp

    @pytest.fixture
    def on_reservations_page(self, logged_in):
        """Precondition: Ensure the test starts on the Reservations page and reset after."""
        if "reservations" not in self.app.get_current_url():
            self.app.dashboard_page.click_crear_reservaciones()
        
        yield self.app.reserved_page

        # Clean up: Refresh the page through a page object's navigation component
        self.app.dashboard_page.navigation.refresh()

    @pytest.mark.usefixtures("on_reservations_page")
    @test_case(id="HOTEL-004-A", skip=False)
    def test_01_filtros_y_vistas(self, on_reservations_page):
        """Fase 1: Validar búsqueda, pestañas y tipos de vista."""
        # Extraemos datos dinámicos del JSON (HOTEL-004-A.json)
        test_data = self.get_test_data()
        search_term = test_data.get("search_term", "Juan")

        # Busqueda usando data-driven
        on_reservations_page.enter_search(search_term).clear_search()

        # Filtros
        self.app.reserved_page.click_tab_todos()
        self.app.reserved_page.click_tab_por_ingresar()
        self.app.reserved_page.click_tab_en_habitacion()
        self.app.reserved_page.click_tab_finalizadas()
        self.app.reserved_page.click_tab_canceladas()
        self.app.reserved_page.click_tab_no_se_presento()

        # Vistas
        self.app.reserved_page.click_view_tarjetas()
        self.app.reserved_page.click_view_agenda()
        self.app.reserved_page.click_view_lista()


    @pytest.mark.usefixtures("on_reservations_page")
    @test_case(id="HOTEL-004-B", skip=False, skip_reason="Test case not implemented yet")
    def test_02_modal_nuevo_cliente(self, on_reservations_page):
        """Fase 2: Validar apertura del modal de Nuevo Cliente."""
        self.app.reserved_page.click_new_client()
        self.app.screenshot("Modal Nuevo Cliente")

    @pytest.mark.usefixtures("on_reservations_page")
    @test_case(id="HOTEL-004-C", skip=False, skip_reason="Test case not implemented yet")
    def test_03_modal_nueva_reservacion(self, on_reservations_page):
        """Fase 3: Validar apertura del modal de Nueva Reservación."""
        self.app.reserved_page.click_new_reservation()
        self.app.screenshot("Modal Nueva Reservación")