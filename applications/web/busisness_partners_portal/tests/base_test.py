from core.ui.common.base_test import BaseTest as GenericBaseTest
from core.utils.test_decorators import project_config
from applications.web.busisness_partners_portal.app.busisness_partners_portal_app import (
    BusisnessPartnersPortalApp,
)


@project_config(
    app_name="busisness_partners_portal", app_class=BusisnessPartnersPortalApp
)
class BaseTest(GenericBaseTest):
    """
    Base test for Busisness Partners Portal tests.
    Inherits setup/teardown and driver management from the core GenericBaseTest.
    """

    app: BusisnessPartnersPortalApp
    pass
