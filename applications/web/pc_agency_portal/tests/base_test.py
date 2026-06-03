from core.ui.common.base_test import BaseTest as GenericBaseTest
from core.utils.test_decorators import project_config
from applications.web.pc_agency_portal.app.pc_agency_portal_app import PcAgencyPortalApp

@project_config(app_name="pc_agency_portal", app_class=PcAgencyPortalApp)
class BaseTest(GenericBaseTest):
    """
    Base test for PC Agency Portal tests.
    Inherits setup/teardown and driver management from the core GenericBaseTest.
    """
    pass
